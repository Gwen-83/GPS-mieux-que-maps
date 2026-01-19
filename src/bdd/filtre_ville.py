import geopandas as gpd

path_source = r"C:\Users\Gwénaël\OneDrive\Bureau\ENAC\Programmation\projet_GPS\src\data\gis_osm_places_free_1.shp"

print("Chargement des données...")
gdf = gpd.read_file(path_source)

# Filtrage
filtre_categories = ['city', 'town', 'village']
gdf_filtre = gdf[gdf['fclass'].isin(filtre_categories)].copy()

# CRÉATION DE L'IDENTIFIANT UNIQUE : Nom_osmID
gdf_filtre['unique_name'] = gdf_filtre['name'].astype(str) + "_" + gdf_filtre['osm_id'].astype(str)

path_dest = r"C:\Users\Gwénaël\OneDrive\Bureau\ENAC\Programmation\projet_GPS\src\data\places_filtres.shp"
gdf_filtre.to_file(path_dest)

print(f"Filtrage terminé. Lieux restants : {len(gdf_filtre)}")
print(f"Le fichier filtré avec IDs uniques a été sauvegardé : {path_dest}")