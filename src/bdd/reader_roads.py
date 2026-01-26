import geopandas as gpd
import pandas as pd
import os

# Configuration des chemins
PATH_ROADS = r"C:\Users\Gwénaël\OneDrive\Bureau\ENAC\Programmation\projet_GPS\src\data\gis_osm_roads_free_1.shp"
PATH_EXPORT_CSV = r"C:\Users\Gwénaël\OneDrive\Bureau\ENAC\Programmation\projet_GPS\src\data\audit_routes.csv"

def export_roads_to_csv(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Erreur : Le fichier {input_path} est introuvable.")
        return

    print("Lecture du fichier Shapefile (cela peut prendre un moment)...")
    # On ne lit que les colonnes nécessaires pour économiser de la mémoire
    cols_to_keep = ['fclass', 'name', 'ref', 'oneway', 'maxspeed', 'layer', 'bridge', 'tunnel']
    
    # Lecture du fichier
    gdf = gpd.read_file(input_path)
    
    # Vérification des colonnes existantes (pour éviter les erreurs si une colonne manque)
    available_cols = [c for c in cols_to_keep if c in gdf.columns]
    
    print(f"Exportation de {len(gdf)} lignes vers le CSV...")
    # Conversion en DataFrame simple (on retire la géométrie pour le CSV)
    df_export = pd.DataFrame(gdf[available_cols])
    
    # Exportation
    df_export.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Succès ! Fichier exporté ici : {output_path}")

    # Petit résumé statistique pour vous aider
    print("\n--- Résumé des données ---")
    print(f"Nombre total de segments : {len(df_export)}")
    print("Top 5 des catégories (fclass) les plus présentes :")
    print(df_export['fclass'].value_counts().head(5))

if __name__ == "__main__":
    export_roads_to_csv(PATH_ROADS, PATH_EXPORT_CSV)