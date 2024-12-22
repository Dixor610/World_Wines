import folium
from folium.plugins import MarkerCluster
from geopy.distance import geodesic

def create_interactive_map(country_data, region_data):
    """
    Creates an interactive map with country and region markers.

    Parameters:
        country_data (DataFrame): Country-level data with coordinates and information.
        region_data (DataFrame): Region-level data with coordinates and information.

    Returns:
        folium.Map: A folium map object.
    """
    # Initialize the map
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="OpenStreetMap")

    # Add country markers
    for _, row in country_data.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"<b>{row['name']}</b><br>{row['info']}",
            tooltip=row["name"]
        ).add_to(m)

    # Add region markers with clustering
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in region_data.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"<b>{row['name']}</b><br>{row['info']}",
            tooltip=row["name"]
        ).add_to(marker_cluster)

    return m

def process_click(latitude, longitude, country_data, region_data):
    """
    Processes a map click to determine if the user clicked on a country
    or region and returns the associated information.

    Parameters:
        latitude (float): Latitude of the clicked location.
        longitude (float): Longitude of the clicked location.
        country_data (DataFrame): Country-level data with coordinates and information.
        region_data (DataFrame): Region-level data with coordinates and information.

    Returns:
        dict: Information about the clicked country or region.
    """
    # Find the closest country or region to the clicked location
    closest_country = _find_closest_point(latitude, longitude, country_data)
    closest_region = _find_closest_point(latitude, longitude, region_data)

    # Determine which is closer
    if closest_region["distance"] < closest_country["distance"]:
        return {
            "type": "Region",
            "name": closest_region["name"],
            "info": closest_region["info"]
        }
    else:
        return {
            "type": "Country",
            "name": closest_country["name"],
            "info": closest_country["info"]
        }

def _find_closest_point(latitude, longitude, data):
    """
    Finds the closest point in a dataset to the given latitude and longitude.

    Parameters:
        latitude (float): Latitude of the clicked location.
        longitude (float): Longitude of the clicked location.
        data (DataFrame): DataFrame containing location data (latitude, longitude).

    Returns:
        dict: Closest point's name, info, and distance.
    """
    closest = None
    min_distance = float("inf")
    for _, row in data.iterrows():
        point_distance = geodesic((latitude, longitude), (row["latitude"], row["longitude"])).kilometers
        if point_distance < min_distance:
            closest = row
            min_distance = point_distance

    return {
        "name": closest["name"],
        "info": closest["info"],
        "distance": min_distance
    }
