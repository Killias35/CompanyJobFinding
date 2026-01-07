import os, time, json
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


VILLES = ["MARSEILLE"]
FILES_PATH = ["MARSEILLE.xlsx"]
ANNUAIRE_EXPERT_COMPTABLE_URL = "https://annuaire.experts-comptables.org/tous-les-cabinets-experts-comptables-par-region"
SOCIETE_COM_URL = "https://www.societe.com/"

def set_parameters():
    global VILLES, FILES_PATH
    if os.path.exists("parameters.json"):
        with open("parameters.json", "r") as f:
            parameters = json.load(f)
            VILLES = parameters.get("villes", VILLES)
            FILES_PATH = parameters.get("chemins_fichier", FILES_PATH)
    else:
        print("parameters.json n'existe pas, création avec valeurs par defaut...")
        with open("parameters.json", "w") as f:
            json.dump({"villes": VILLES, "chemins_fichier": FILES_PATH}, f, indent=4)

def is_files_valid():
    for i in range(len(FILES_PATH)):
        if not os.path.exists(FILES_PATH[i]):
            return False, f"Le fichier {FILES_PATH[i]} n'existe pas"
    return True, "Tout les fichiers existent"


set_parameters()
