import matplotlib
matplotlib.use('Agg') # MUST BE FIRST
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, send_from_directory
import osmnx as ox
from io import BytesIO
import base64

app = Flask(__name__, static_folder='static', template_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/generate', methods=['GET'])
def generate():
    location = request.args.get('location', 'New York, USA')
    bg_color = request.args.get('bg', '#000000')
    road_color = request.args.get('roads', '#ffffff')
    water_color = request.args.get('water', '#2a4365')

    plt.close('all')
    plt.clf()

    try:
        # 1. Fetch Road Data
        # Using dist=2000 to keep it fast
        G = ox.graph_from_address(location, dist=2000, network_type="all")

        # 2. Setup the Figure manually so we can layer it
        fig, ax = plt.subplots(figsize=(10, 15), facecolor=bg_color)
        ax.set_facecolor(bg_color)

        # 3. Layer 1: WATER (Plot this first so it's on the bottom)
        try:
            water = ox.features_from_address(location, tags={"natural": "water", "waterway": True}, dist=2000)
            if not water.empty:
                water.plot(ax=ax, color=water_color, edgecolor='none')
        except Exception as e:
            print(f"Water fetch skipped or failed: {e}")

        # 4. Layer 2: ROADS (Plot this second so it's on top)
        # Note: We removed 'zorder' to avoid the error you saw.
        ox.plot_graph(
            G,
            ax=ax,
            node_size=0,
            edge_color=road_color,
            edge_linewidth=0.8,
            bgcolor=bg_color,
            show=False,
            close=False
        )

        # 5. Final Styling
        ax.axis('off')

        # 6. Save to Buffer
        buffer = BytesIO()
        plt.savefig(buffer, format="png", dpi=300, bbox_inches='tight', pad_inches=0, facecolor=bg_color)
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode()

        return jsonify({"image": img_str})

    except Exception as e:
        print(f"RENDER ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

def run_server():
    app.run(port=5000, debug=True)

if __name__ == '__main__':
    run_server()
