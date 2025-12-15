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

def get_pappers_datas(session: Session, company_names: list[str] = [])-> dict[str, dict[str, list[str]]]:
    """
    Renvoie une liste de nom d'entreprise

    {
        "nom sur pappers": {
            "code NAF": "",
            "nom dans les données": ""
        }
    }
    """
    print("recupération des entreprises depuis pappers...")

    company_names_pappers = []
    company_links = []
    datas = {}
    up = True
    tour = 0
    print(len(company_names), " entreprises a trouver")
    try:
        for company_name in company_names:
            index = company_names.index(company_name)
            print(f"{index+1}/{len(company_names)} {company_name}")
            search_bar = session.driver.find_element(By.CLASS_NAME, "search")
            search_bar.click()
            time.sleep(.5)
            search_bar.send_keys(Keys.CONTROL + "a")
            time.sleep(.1)
            search_bar.send_keys(Keys.BACKSPACE)
            time.sleep(.1)
            search_bar.send_keys(company_name)
            time.sleep(.5)
            search_bar.send_keys(Keys.RETURN)
            time.sleep(2)
            try:
                time.sleep(1)
                a = WebDriverWait(session.driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.nom-entreprise a')))
                names = [link.text for link in a if not link.text in company_names]
                links = [link.get_attribute("href") for link in a if not link.get_attribute("href") in company_links]
                for i in range(len(names)):
                    link = links[i]
                    name = names[i]
                    datas[name] = {
                        "code NAF": "",
                        "nom dans les données": company_name,
                        "pappers link": link
                    }
                company_links.extend(links)
                company_names_pappers.extend(names)
                try:
                    next_page = session.driver.find_element(By.CLASS_NAME, 'pagination-image-right')
                    previous_page = session.driver.find_element(By.CLASS_NAME, 'pagination-image-left')

                    if next_page.tag_name == "a" and up:
                        next_page.click()
                    elif next_page.tag_name != "a" and up:
                        up = False
                        tour += 1
                    elif previous_page.tag_name == "a" and not up:
                        previous_page.click()
                    elif previous_page.tag_name != "a" and not up:
                        up = True
                except Exception:
                    pass
                time.sleep(2)
            except Exception as err:
                datas[company_name] = {
                    "code NAF": "",
                    "nom dans les données": company_name,
                    "pappers link": ""
                }
                print(company_name, "pas trouvée sur pappers")
                continue

    except Exception as err:
        print("une erreur est apparue durant la recherche sur pappers (Captcha / limite atteintes...)")
        raise err

    print("\n\n\n")
    print(len(company_links), " entreprises a chercher sur pappers")
    
    for i in range(len(company_names_pappers)):
        print(f"{i+1}/{len(company_names_pappers)} {company_names_pappers[i]}")
        link = company_links[i]
        name = company_names_pappers[i]
        session.driver.get(link)
        time.sleep(3)
        data = datas[name]
        try:
            td = WebDriverWait(session.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'info-dirigeant')))
            # 1. Trouver le th contenant le texte
            td = session.driver.find_element(
                By.XPATH,
                "//tr[th[contains(normalize-space(.), 'Code NAF ou APE :')]]/td"
            )

            code_NAF = td.text.split(" ")[0]
            data["code NAF"] = code_NAF
            datas[name] = data
        except Exception:
            data["code NAF"] = ""
            datas[name] = data

    return datas
    
