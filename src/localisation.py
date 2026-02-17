import json
import os

# map.py est dans src/
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) 

# On descend dans le dossier visualisation pour trouver les fichiers
# Chemin : src/visualisation/dico_final.json
PATH_LOCALISATION = os.path.join(CURRENT_DIR, "visualisation", "coords_villes.json")

print(f"Tentative de chargement du dico depuis : {PATH_LOCALISATION}")

if os.path.exists(PATH_LOCALISATION):
    with open(PATH_LOCALISATION, encoding="utf-8") as f:
        localisation_ville = json.load(f)
    print("✅ maping chargé avec succès.")
else:
    print(f"❌ ERREUR : Fichier introuvable à l'emplacement : {PATH_LOCALISATION}")
    maping = {}
