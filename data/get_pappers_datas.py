import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.utils.session import Session
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from data.utils.google_search import search_duckduckgo

def get_pappers_datas(session: Session, company_names: list[str] = [], ville: str = "")-> dict[str, dict[str, list[str]]]:
    """
    Renvoie une liste de nom d'entreprise

    {
        "nom sur pappers": {
            "code_naf": "",
            "nom dans les données": ""
        }
    }
    """
    print("recupération des entreprises depuis pappers...")

    search_data = {}
    datas = {}
    print(len(company_names), " entreprises a trouver")
    try:
        for company_name in company_names:
            company_links = []
            
            index = company_names.index(company_name)
            print(f"{index+1}/{len(company_names)} {company_name}")
            links = search_duckduckgo(session, f"entreprise {company_name} {ville} pappers", max_results=3)
            for link in links:
                if "pappers.fr/entreprise/" in link:
                    company_links.append(link)
            if len(links) == 0:
                datas[company_name] = {"code_naf": "", "nom dans les données": company_name}
            search_data[company_name] = company_links
            time.sleep(2)

    except Exception as err:
        print("une erreur est apparue durant la recherche internet...")
        raise err

    print("\n\n\n")
    print(len(search_data), " entreprises a chercher sur pappers")
    
    for company_name, company_search in search_data.items():
        i = company_names.index(company_name)
        print(f"{i+1}/{len(search_data)} ------- {company_name}") # type: ignore

        for link in company_search:
            session.driver.get(link)
            time.sleep(2)
            try:
                td = WebDriverWait(session.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'info-dirigeant')))
                td = session.driver.find_element(
                    By.XPATH,
                    "//tr[th[contains(normalize-space(.), 'Code NAF ou APE :')]]/td"
                )
                name = session.driver.find_element(By.TAG_NAME, "h1").text
                code_NAF = td.text.split(" ")[0]
                data = {
                    "nom dans les données": company_name, 
                    "code_naf": code_NAF}
                
                datas[name] = data
            except Exception as err:
                if datas.get(company_name) is None:
                    datas[company_name] = {"code_naf": "", "nom dans les données": company_name}
                print("entreprise non trouvée\n" + link, err)

    return datas
    
