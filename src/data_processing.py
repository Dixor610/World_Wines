import json
import pandas as pd

def main():
    data_dir = "data"
    #for filename in os.listdir(data_dir):
    #    if filename.endswith(".geojson"):
    #        input_geojson = os.path.join(data_dir, filename)
    #        output_geojson = os.path.join(data_dir, filename)
    #        clean_geojson(input_geojson, output_geojson)
            
    #region_data = load_csv_data(r'N:\Doct\Codes\World_Wines\src\data\regions.csv')
    #process_grapes(region_data, 'raims_blancs', r'N:\Doct\Codes\World_Wines\src\data\raims_blancs.csv')
    #process_grapes(region_data, 'raims_negres', r'N:\Doct\Codes\World_Wines\src\data\raims_negres.csv')


def process_grapes(df, column_name, output_file):
    all_grapes = df[column_name].str.split(', ').explode().dropna().unique()
    all_grapes.sort()
    
    data = []
    for grape in all_grapes:
        count = df[column_name].str.contains(grape).sum()
        regions = df[df[column_name].str.contains(grape, na=False)]['regio'].tolist()
        data.append({
            'varietats': grape,
            'pais_origen': "",
            'regions_utilitzen': count,
            'regions_noms': ', '.join(regions),
            'tonalitats': ""
        })
    
    result_df = pd.DataFrame(data)
    result_df.to_csv(output_file, index=False, encoding='utf-8')

    return result_df

def clean_geojson(input_file, output_file):
    """
    Open a GeoJSON file, remove all properties except 'coordinates',
    and save the cleaned GeoJSON to a new file with minimized size.

    Parameters:
    - input_file (str): Path to the input GeoJSON file.
    - output_file (str): Path to save the cleaned GeoJSON file.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    for feature in geojson_data["features"]:
        # Keep only 'coordinates' (already in geometry)
        if "properties" in feature:
            feature["properties"] = {}

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(geojson_data, f, ensure_ascii=False, separators=(",", ":"), indent=None)