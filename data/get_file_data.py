import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    
import pandas as pd
from conf.conf import FILE_PATH

def fix_mojibake(text):
    if not isinstance(text, str):
        return text
    try:
        # Tente de réparer les accents mal décodés
        return text.encode("latin1").decode("utf-8")
    except:
        # Si impossible, renvoie le texte original
        return text

def get_file_datas()->list[str]:
    if not os.path.exists(FILE_PATH):
        print(f"Le fichier {FILE_PATH} n'existe pas a coté du script, merci de le mettre dans le meme dossier")
        raise FileNotFoundError(f"Le fichier {FILE_PATH} n'existe pas")
    # Charge ton fichier
    df = pd.read_excel(FILE_PATH)

    # Récupère la colonne qui t'intéresse
    col = df["current_company_name"]

    # Corrige chaque valeur
    fixed = col.apply(fix_mojibake)

    # Récupère la liste des entreprises
    companies = []
    for company in fixed:
        companies.append(str(company))
    
    return companies

if __name__ == "__main__":
    companies = get_file_datas()
    print(len(companies), companies[0:10])