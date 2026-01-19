import geopandas as gpd
from geopandas import sjoin

cities_file = r"C:\Users\Gwénaël\OneDrive\Bureau\ENAC\Programmation\projet_GPS\src\data\gis_osm_places_free_1.shp"
roads_file  = r"C:\Users\Gwénaël\OneDrive\Bureau\ENAC\Programmation\projet_GPS\src\data\gis_osm_roads_free_1.shp"

cities = gpd.read_file(cities_file)
roads  = gpd.read_file(roads_file)

cities = cities[cities['fclass'].isin(['city', 'town'])]
roads  = roads[roads['fclass'].isin(['motorway', 'primary', 'secondary', 'tertiary'])]

cities = cities.to_crs(epsg=2154)
roads  = roads.to_crs(epsg=2154)

cities['buffer_geom'] = cities.geometry.buffer(1000)
cities_buffer = cities.set_geometry('buffer_geom')

roads_with_cities = sjoin(roads, cities_buffer[['name', 'buffer_geom']], how='inner', predicate='intersects')

roads_with_cities = roads_with_cities.rename(columns={'name_right': 'city_name', 'name_left': 'road_name'})

roads_with_cities = roads_with_cities.to_crs(epsg=4326)

cities_routes = roads_with_cities.groupby('city_name').agg({
    'road_name': list,
    'fclass': list,
    'geometry': 'first',
    'maxspeed': list
}).reset_index()

print(cities_routes.head())

# convertir les colonnes listes en chaînes séparées par des virgules
cities_routes['road_name'] = cities_routes['road_name'].apply(lambda x: ', '.join(map(str, x)))
cities_routes['fclass']    = cities_routes['fclass'].apply(lambda x: ', '.join(map(str, x)))
cities_routes['maxspeed']  = cities_routes['maxspeed'].apply(lambda x: ', '.join(map(str, x)))

# exporter en CSV
cities_routes.to_csv(r"C:\Users\Gwénaël\OneDrive\Bureau\ENAC\Programmation\projet_GPS\cities_routes.csv", index=False)

print("CSV exporté avec succès !")
