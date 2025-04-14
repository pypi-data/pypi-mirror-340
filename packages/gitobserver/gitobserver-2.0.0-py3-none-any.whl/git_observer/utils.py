import os
import subprocess
import platform
import json
from colorama import init

# 🖌️ Initialisation de Colorama pour Windows
init(autoreset=True)
FILE_NAME = "observer.config.json"

def get_current_directory():
    """Récupération du dossier courant (compatible Linux & Windows)"""
    return os.getcwd() if platform.system() == "Windows" else subprocess.run(["pwd"], capture_output=True, text=True).stdout.strip()



def init_and_load_config(filename=FILE_NAME):
    """Crée le fichier config s'il n'existe pas et retourne son contenu"""
    
    default_config = {
        "commit_delay": 5,
        "commit_patern": "commit_name=",
        "response_delay": 2,
        "max_files": 10,
        "commit_message": "auto commit",
    }

    config_path = os.path.join(get_current_directory(), filename)

    # Créer le fichier si inexistant
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=4)

    # Lire le contenu du fichier
    with open(config_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default_config  # fallback au cas où le fichier est corrompu



def read_config(filename=FILE_NAME):
    """Lit le fichier config et retourne son contenu en dict"""
    config_path = os.path.join(get_current_directory(), filename)

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Le fichier {filename} est introuvable à la racine du projet.")

    with open(config_path, "r") as f:
        return json.load(f)
    