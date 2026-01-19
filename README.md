(The file `/Users/ttg/Code/map-poster-app/README.md` exists, but is empty)
# Map Poster App — Web Frontend for City Map Poster Generator

**Note:** This app is a web front for the [City Map Poster Generator](https://github.com/originalankur/maptoposter) by [OriginaAnkur](https://github.com/originalankur).

It provides a lightweight Flask web frontend that generates poster-quality city maps using OSMnx and Matplotlib.

**Features**
- **Simple REST API**: Generate posters via `GET /generate` with query parameters.
- **Customizable styling**: Background, roads and water color options.
- **Compact web UI**: `index.html` provides a minimal interface for testing.
- **Cached fetches**: `cache/` stores fetched data to speed repeated renders.

-**Prerequisites**
- Python >= 3.13 (as specified in `pyproject.toml`)
- uv
- System geospatial libraries for `osmnx` (on macOS you may need `geos`, `gdal`, `proj` from Homebrew). If you hit installation issues, see OSMnx docs for platform-specific guidance or consider using a conda environment.

**Quick Start**
1. Clone the repo:
```
	git clone https://your-repo-url.git
	cd map-poster-app
```
2. Create and activate a virtual environment:
```
  uv init
```
3. Install the package (this will install dependencies from `pyproject.toml`):
```
  uv install -e .
```
4. Run the app:
```
  uv start app.py
```
5. Open the UI in your browser: http://localhost:5000/

**API Usage**
GET /generate

Query parameters:
- `location` — place name or address (default: "New York, USA")
- `bg` — background color (hex, default `#000000`)
- `roads` — road color (hex, default `#ffffff`)
- `water` — water color (hex, default `#2a4365`)

Response: JSON with a base64-encoded PNG image:

{
  "image": "<base64-png-data>"
}

Example using `curl` + `jq` to save the poster as `poster.png`:

  curl "http://localhost:5000/generate?location=Amsterdam&bg=%23000000&roads=%23ffffff&water=%23007bff" \
	 -s | jq -r '.image' | base64 --decode > poster.png

If you don't have `jq`, you can decode the JSON using Python:

  curl "http://localhost:5000/generate?location=Amsterdam" -s | python -c "import sys, json, base64; print(base64.b64decode(json.load(sys.stdin)['image']))" > poster.png

**Cache**
- The `cache/` directory contains cached JSON responses used to speed up repeated renders. You can clear or inspect this directory if you need fresh fetches.

**Development notes**
- The main server is `app.py`. The route `/generate` does the heavy lifting: it fetches OSM data with OSMnx, layers water and roads with Matplotlib, then returns a base64 PNG.
- To change default rendering parameters or figure size, edit `app.py` in the `generate()` function.
- The web UI is `index.html` at the repo root — feel free to improve the UI or add preset styles.

**Troubleshooting**
- OSMnx can require platform-specific dependencies (geospatial libraries). If you see errors during `uv install osmnx` or at runtime, install the geospatial libraries via Homebrew on macOS: `brew install geos gdal proj`.
- If plotting fails or images are blank, ensure Matplotlib uses a non-interactive backend; `app.py` sets `matplotlib.use('Agg')` explicitly.

**Credits & License**
- This project is a web app front for the City Map Poster Generator by Ankur (https://github.com/originalankur/maptoposter). Check that repository for original implementation details and license.
- LICENSE file reflects MIT license from the original repository, and extends it to this one.
