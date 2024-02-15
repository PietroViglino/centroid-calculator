import os
import geojson
from geojson import dump

for file_name in os.listdir('test'):
    gj = None
    with open(f'test/{file_name}') as f:
        gj = geojson.load(f)
    base_name = file_name.replace('.geojson', '')
    with open(f'test/{base_name}_centroids.geojson', 'w') as f:
        dump(gj, f)