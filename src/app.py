from flask import Flask, render_template, jsonify, request
from map_generator import create_interactive_map, process_click
from data_loader import load_country_data, load_region_data

app = Flask(__name__)

# Load data
country_data = load_country_data("data/countries.csv")
region_data = load_region_data("data/regions.csv")

@app.route("/")
def index():
    """Renders the interactive map."""
    map_object = create_interactive_map(country_data, region_data)
    map_object.save("templates/map.html")
    return render_template("map.html")

@app.route("/click", methods=["POST"])
def handle_click():
    """
    Handles click events on the map, returning the appropriate information
    for the clicked location (country or region).
    """
    data = request.json  # Expected JSON: { "latitude": float, "longitude": float }
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    clicked_info = process_click(latitude, longitude, country_data, region_data)
    return jsonify(clicked_info)

if __name__ == "__main__":
    app.run(debug=True)