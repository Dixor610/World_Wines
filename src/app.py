import folium
import json
from data_loader import load_csv_data
from flask import Flask, render_template

app = Flask(__name__)

def generate_map(country_data, region_data):
    """
    Generate an interactive world map with markers for countries and regions.
    Clicking a marker highlights its region or area dynamically.

    Parameters:
    country_data (pd.DataFrame): DataFrame containing country information.
                                 Columns: ['name', 'latitude', 'longitude', 'info']
    region_data (pd.DataFrame): DataFrame containing region information.
                                Columns: ['name', 'latitude', 'longitude', 'info']

    Returns:
    folium.Map: A folium map object with interactive highlighting.
    """
    # Initialize the map with no default tiles
    m = folium.Map(location=[20, 0], zoom_start=2, control_scale=True, tiles=None)

    # Add Street View (OpenStreetMap)
    folium.TileLayer(
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        name="Street View",
        attr="© OpenStreetMap contributors"
    ).add_to(m)

    # Add Satellite View (Esri)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        name="Satellite View",
        attr="Tiles © Esri — Source: Esri, DeLorme, NAVTEQ"
    ).add_to(m)

    # Load GeoJSON data
    with open("data/areas.geojson", "r") as f:
        geojson_data = json.load(f)

    # Create a dictionary of GeoJSON features by name for easy lookup
    features_by_name = {
        feature["properties"]["name"]: feature for feature in geojson_data["features"]
    }

    # Add markers for each country
    for _, row in country_data.iterrows():
        name, lat, lon, info = row['name'], row['latitude'], row['longitude'], row['info']
        folium.Marker(
            location=[lat, lon],
            popup=f"<b>{name}</b><br>{info}",
            tooltip=name,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    # Add markers for each region
    for _, row in region_data.iterrows():
        name, lat, lon, info = row['name'], row['latitude'], row['longitude'], row['info']
        folium.Marker(
            location=[lat, lon],
            popup=f"<b>{name}</b><br>{info}",
            tooltip=name,
            icon=folium.Icon(color="green", icon="info-sign")
        ).add_to(m)

    # Add Layer Control
    folium.LayerControl().add_to(m)

    return m

@app.route("/")
def index():
    """
    Render the main page with the world map.

    Returns:
    str: Rendered HTML template with the embedded map.
    """
    # Load data
    country_data = load_csv_data('data/countries.csv')
    region_data = load_csv_data('data/regions.csv')

    # Generate map
    map_object = generate_map(country_data, region_data)

    # Save map to an HTML file
    map_object.save('templates/map.html')

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)