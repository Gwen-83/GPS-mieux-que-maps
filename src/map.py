import json
import os

# map.py est dans src/
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) 

# On descend dans le dossier visualisation pour trouver les fichiers
# Chemin : src/visualisation/dico_final.json
PATH_DICO_FINAL = os.path.join(CURRENT_DIR, "visualisation", "dico_final.json")

print(f"Tentative de chargement du dico depuis : {PATH_DICO_FINAL}")

if os.path.exists(PATH_DICO_FINAL):
    with open(PATH_DICO_FINAL, encoding="utf-8") as f:
        maping = json.load(f)
    print("✅ maping chargé avec succès.")
else:
    print(f"❌ ERREUR : Fichier introuvable à l'emplacement : {PATH_DICO_FINAL}")
    maping = {}
