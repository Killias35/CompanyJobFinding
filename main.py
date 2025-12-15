import time
from data.utils.session import Session
from data.get_file_data import get_file_datas
from data.filter_research_pappers import filter_research
from data.get_pappers_datas import get_pappers_datas
from data.utils.export_to_csv import export_to_csv
from conf.conf import VILLE
import traceback

def main():
    session = Session()
        
    try:
        print("Debut du script")
        companies = get_file_datas()

        filter_research(session, [VILLE])
        scrapped_companies = get_pappers_datas(session, companies)
        session.close()
        export_to_csv(scrapped_companies)
        print(f"Entreprise dans le fichier: {len(companies)}\nEntreprise trouvées: {len(scrapped_companies)}")

    except Exception as e:
        session.close()
        print("une erreur est apparue, un fichier 'debug.txt' a été crée contenant l'erreur, merci de me l'envoyer stp")
        with open("debug.txt", "w") as f:
            f.write(traceback.format_exc())
        time.sleep(10000)
    

if __name__ == "__main__": 
    main()