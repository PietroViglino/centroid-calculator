import geopandas as gpd
import os
from shapely.geometry import Point
import geojson
from geojson import dump
            
def correct_coordinates(geom):
    if geom.coords[0] == (8.704347663979942, 44.264337341739356): # regione Liguria
        return Point(8.683531836855193, 44.45206883496183)
    if geom.coords[0] == (8.20921943078088, 45.52531936141556): # provincia di Vercelli
        return Point(8.308994130858247, 45.439495958632804)
    if geom.coords[0] == (10.478846791157835, 43.144980401921586): # provincia di Livorno
        return Point(10.499399887400761, 43.319794934857285)
    if geom.coords[0] == (12.439838617193596, 43.926903712934269): # provincia di Rimini
        return Point(12.537177942640268, 44.01872840882674)
    if geom.coords[0] == (12.366707571225877, 42.664597602363976): # provincia di Terni
        return Point(12.360869975310054, 42.63145888038969)
    if geom.coords[0] == (14.07280260521307, 37.356907692388098): # provincia di Caltanissetta
        return Point(14.038956407703049, 37.335605929682536)
    if geom.coords[0] == (14.8294650444412, 37.51236230304287): # provincia di Catania
        return Point(14.893817193816242, 37.52153310873328)
    if geom.coords[0] == (9.107372216468665, 39.207381682327124): # provincia di Cagliari
        return Point(9.106919137130825, 39.240240124056015)
    return geom

# Centroids as geometry
def centroids_as_geometry(input_folder=os.getcwd(), output_folder=os.getcwd()):
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.geojson') and 'centroids' not in file_name:
            df = gpd.read_file(f'{input_folder}/{file_name}')
            df['geometry'] = df['geometry'].to_crs(epsg=4326)
            df['geometry'] = df['geometry'].centroid
            df['geometry'] = df['geometry'].apply(correct_coordinates)
            base_name = file_name.replace('.geojson', '')
            df.to_file(f'{output_folder}/{base_name}_centroids.geojson')
    print('Done')

# Centroids as new property
def centroids_as_property(input_folder=os.getcwd(), output_folder=os.getcwd()):
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.geojson') and 'centroids' not in file_name:
            df = gpd.read_file(f'{input_folder}/{file_name}')
            centroids = gpd.GeoSeries()
            df['geometry'] = df['geometry'].to_crs(epsg=4326)
            centroids = df['geometry'].centroid
            centroids = centroids.apply(correct_coordinates)
            with open(f'{input_folder}/{file_name}') as f:
                gj = geojson.load(f)
            assert len(gj['features']) == len(centroids), 'Lengths of geojson features and centroids not matching'
            for index in range(len(gj['features'])):
                properties = gj['features'][index]['properties']
                centroid = centroids[index]
                point_coords_list = [centroid.x, centroid.y]
                properties["center"] = point_coords_list
            base_name = file_name.replace('.geojson', '')
            with open(f'{base_name}_centroids.geojson', 'w') as f:
                dump(gj, f)
    print('Done')  

if __name__ == '__main__':
    centroids_as_property()