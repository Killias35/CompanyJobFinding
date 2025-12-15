import time
from data.utils.session import Session
from data.get_file_data import get_file_datas
from data.get_pappers_datas import get_pappers_datas
from data.utils.export_to_csv import export_to_csv
from conf.conf import VILLES, FILES_PATH
import traceback

def main():
    print("Debut du script")
    print("Chargement du naviguateur...")
    session = Session()
        
    try:
        for i in range(len(VILLES)):
            VILLE = VILLES[i]
            FILE_PATH = FILES_PATH[i]

            companies = get_file_datas(FILE_PATH)
            scrapped_companies = get_pappers_datas(session, companies, VILLE)
            session.close()
            export_to_csv(scrapped_companies)
            print(f"Entreprise dans le fichier: {len(companies)}\nEntreprise trouvées: {len(scrapped_companies)}")

    except Exception:
        session.close()
        print("une erreur est apparue, un fichier 'debug.txt' a été crée contenant l'erreur, merci de me l'envoyer stp")
        with open("debug.txt", "w") as f:
            f.write(traceback.format_exc())
        time.sleep(10000)
    

if __name__ == "__main__": 
    main()