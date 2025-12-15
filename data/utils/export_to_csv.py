import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import csv

def export_to_csv(datas: dict, filename: str = "entreprises.csv"):
    """
    Exporte les entreprises au format csv
    datas est sous cette forme:
    {
        "nom sur pappers": {
            "code NAF": "",
            "nom dans les données": ""
        }
    }
    """
    print("Exportation au format csv...")
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ENTREPRISE (PAPPERS)", "CODE NAF", "ENTREPRISE (DEPUIS FICHIER)"])
        for name, data in datas.items():
            code_naf = data["code_naf"]
            data_name = data["nom dans les données"]

            writer.writerow([name, code_naf, data_name])            
            
    print(f"✅ Fichier sauvegardé : {filename}")

if __name__ == "__main__":
    # export_to_csv(data)
    pass