import folium
import os
import json
from data_processing import process_grapes
from data_loader import load_csv_data
from flask import Flask, render_template, request

app = Flask(__name__)

def generate_map(country_data=None, region_data=None, DO_data=None, white_grapes_data=None, red_grapes_data=None, include_regions=True):
    """
    Generate an interactive world map with markers for countries and regions or grapes.
    Includes toggleable layers for GeoJSON files in the data directory.
    """
    # Initialize the map with no default tiles
    m = folium.Map(location=[40.4168, -3.7038], zoom_start=6, control_scale=True, tiles=None)

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
        attr="Tiles © Esri, DeLorme, NAVTEQ"
    ).add_to(m)

    if include_regions:
        # Create FeatureGroups for countries and regions
        country_group = folium.FeatureGroup(name="Countries", show=True)
        region_group = folium.FeatureGroup(name="Regions", show=True)
        DO_group = folium.FeatureGroup(name="DOs", show=True)

        # Add markers for each country
        for _, row in country_data.dropna(subset=['latitude', 'longitude']).iterrows():
            pais = str(row['país'])
            lat = row['latitude']
            lon = row['longitude']

            # Construct the image path
            image_path_country = f"/static/images_countries/{pais}.png"

            # Add marker with only an image in the pop-up
            popup_html_country = f"""
                <div style='text-align:center;'>
                    <img src="{image_path_country}" alt="Image of {pais}" 
                         style='height:65vh; width:auto; cursor:pointer;' 
                         onclick="openModal('{image_path_country}')">
                </div>
            """
            
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html_country, max_width=None),  # Let the image determine width
                tooltip=pais,
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(country_group)

        # Add markers for each region
        for _, row in region_data.dropna(subset=['latitude', 'longitude']).iterrows():
            region = str(row['regio'])
            lat = row['latitude']
            lon = row['longitude']

            # Construct the image path
            image_path_region = f"/static/images_regions/{region}.png"

            # Add marker with only an image in the pop-up
            popup_html_region = f"""
                <div style='text-align:center;'>
                    <img src="{image_path_region}" alt="Image of {region}" 
                         style='height:65vh; width:auto; cursor:pointer;' 
                         onclick="openModal('{image_path_region}')">
                </div>
            """
            
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html_region, max_width=None),  # Let the image determine width
                tooltip=region,
                icon=folium.Icon(color="orange", icon="info-sign")
            ).add_to(region_group)

        # Add markers for each DO
        for _, row in DO_data.dropna(subset=['latitude', 'longitude']).iterrows():
            DO = str(row['DO'])
            lat = row['latitude']
            lon = row['longitude']
            raims_blancs = str(row['raims_blancs'])
            raims_negres = str(row['raims_negres'])
            extra = str(row['extra'])

            # Add marker with dynamic pop-up (text + image)
            popup_html_DO = f"""
                <div style='text-align:center;'>
                    <!-- Text Content -->
                    <div style='margin-top:10px; text-align:left;'>
                        <b>{DO}</b><br>
                        <b></b><br>
                        <b>Raims Blancs:</b> {raims_blancs}<br>
                        <b>Raims Negres:</b> {raims_negres}<br>
                        <b>Extra:</b> {extra}
                    </div>
                </div>
            """

            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html_DO, max_width=None),
                tooltip=DO,
                icon=folium.Icon(color="green", icon="info-sign")
            ).add_to(DO_group)

        # Add FeatureGroups to the map
        country_group.add_to(m)
        region_group.add_to(m)
        DO_group.add_to(m)

    else:
        # Create FeatureGroups for white and red grapes
        white_grape_group = folium.FeatureGroup(name="White Grapes", show=True)
        red_grape_group = folium.FeatureGroup(name="Red Grapes", show=True)

        for _, row in country_data.dropna(subset=['latitude', 'longitude']).iterrows():
            pais = str(row['país'])
            lat = row['latitude']
            lon = row['longitude']

            # White grapes
            white_grapes = white_grapes_data[white_grapes_data['pais_origen'] == pais]
            if not white_grapes.empty:
                varieties = white_grapes['varietats'].tolist()
                regions_used = white_grapes['regions_utilitzen'].tolist()
                regions_names = white_grapes['regions_noms'].tolist()

                popup_html_white = "<div style='text-align:left;'>"
                for variety, used, names in zip(varieties, regions_used, regions_names):
                    popup_html_white += f"<b>- {variety}:</b> {used}, {names}<br><br>"
                popup_html_white += "</div>"

                folium.Marker(
                    location=[lat, lon + 0.3],  # Slightly offset to avoid overlap
                    popup=folium.Popup(popup_html_white, max_width=300, max_height=200),  # Set max width and height for scrolling
                    tooltip=f"White Grapes in {pais}",
                    icon=folium.Icon(color="white", icon="circle")
                ).add_to(white_grape_group)

            # Red grapes
            red_grapes = red_grapes_data[red_grapes_data['pais_origen'] == pais]
            if not red_grapes.empty:
                varieties = red_grapes['varietats'].tolist()
                regions_used = red_grapes['regions_utilitzen'].tolist()
                regions_names = red_grapes['regions_noms'].tolist()

                popup_html_red = "<div style='text-align:left;'>"
                for variety, used, names in zip(varieties, regions_used, regions_names):
                    popup_html_red += f"<b>- {variety}:</b> {used}, {names}<br><br>"
                popup_html_red += "</div>"

                folium.Marker(
                    location=[lat, lon - 0.3],  # Slightly offset to avoid overlap
                    popup=folium.Popup(popup_html_red, max_width=400, max_height=300),  # Set max width and height for scrolling
                    tooltip=f"Red Grapes in {pais}",
                    icon=folium.Icon(color="red", icon="circle")
                ).add_to(red_grape_group)

        white_grape_group.add_to(m)
        red_grape_group.add_to(m)

    # Add GeoJSON and JSON layers for files in the data directory
    data_dir = "data/provincies"
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(data_dir, filename), "r", encoding="utf-8") as f:
                    geojson_data = json.load(f)
            except UnicodeDecodeError:
                with open(os.path.join(data_dir, filename), "r", encoding="latin-1") as f:
                    geojson_data = json.load(f)
            
            # Format the name
            layer_name = filename.replace(".json", "").replace("_", " ").title()

            # Determine the correct field name for the tooltip
            if 'NAME' in geojson_data['features'][0]['properties']:
                tooltip_field = 'NAME'
            elif 'name' in geojson_data['features'][0]['properties']:
                tooltip_field = 'name'
            else:
                tooltip_field = None

            if tooltip_field:
                folium.GeoJson(
                    geojson_data,
                    name=layer_name,
                    style_function=lambda feature: {
                        "fillColor": "#ffaf00",  # Set fill color
                        "color": "black",       # Set border color
                        "weight": 1,            # Border thickness
                        "fillOpacity": 0.5      # Transparency
                    },
                    tooltip=folium.GeoJsonTooltip(fields=[tooltip_field], aliases=['Region:']),
                    control=False  # Disable click
                ).add_to(folium.FeatureGroup(name=layer_name, show=False).add_to(m))

    folium.LayerControl(collapsed=False).add_to(m)
    
    return m

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Render the main page with the world map or the world grapes map based on user selection.

    Returns:
    str: Rendered HTML template with the embedded map.
    """
    if request.method == "POST":
        map_type = request.form.get("map_type")
        if map_type == "world_grapes":
            # Load data
            country_data = load_csv_data('data/countries.csv')
            white_grapes_data = load_csv_data('data/raims_blancs.csv')
            red_grapes_data = load_csv_data('data/raims_negres.csv')

            # Generate World Grapes Map with markers
            map_object = generate_map(country_data=country_data, white_grapes_data=white_grapes_data, red_grapes_data=red_grapes_data, include_regions=False)
        else:
            # Load data
            country_data = load_csv_data('data/countries.csv')
            region_data = load_csv_data('data/regions.csv')
            DO_data = load_csv_data('data/DOs.csv')
            white_grapes_data = load_csv_data('data/raims_blancs.csv')
            red_grapes_data = load_csv_data('data/raims_negres.csv')

            # Generate World Wines Map with markers
            map_object = generate_map(country_data, region_data, DO_data, white_grapes_data, red_grapes_data, include_regions=True)

        # Save map to an HTML file
        map_object.save('templates/map.html')

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
