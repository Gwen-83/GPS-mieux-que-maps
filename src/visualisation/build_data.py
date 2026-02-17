import os
import gdown

# On définit le chemin absolu vers le dossier où est ce script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

files_to_download = {
    "ma_base.db": "1tdCOdYdF5QchCr95P8o6HQJ2MuTQEDBJ",
    "dico_final.json": "1NXsjXBL0Swzi3neALMYhbV0WVevtUclz",
    "routes_ville_adj.json": "1HtQlshnmTJqQNsqez6PlL-kCjS634T_q",
    "coords_villes.json": "1iO1zhnZjA1awWil7RSJzx3DpsOZuD9LT"
}

def download():
    print("--- DÉBUT TÉLÉCHARGEMENT BUILD ---")
    for filename, drive_id in files_to_download.items():
        destination = os.path.join(CURRENT_DIR, filename)
        if not os.path.exists(destination):
            print(f"Téléchargement de {filename}...")
            try:
                url = f'https://drive.google.com/uc?id={drive_id}'
                gdown.download(url, destination, quiet=False)
            except Exception as e:
                print(f"❌ Erreur {filename}: {e}")
        else:
            print(f"✅ {filename} déjà présent.")

if __name__ == "__main__":
    download()
