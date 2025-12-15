import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.utils.session import Session
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException

def filter_research(session: Session, villes: list[str]):
    print("Filtrage depuis pappers...")
    final_url = "https://pappers.fr/recherche/?"
    try:
        session.driver.get(final_url)
    except UnexpectedAlertPresentException:
        try:
            alert = session.driver.switch_to.alert
            print("⚠️ Alerte détectée :", alert.text)
            alert.accept()  # Ferme la popup
            time.sleep(1)
            # Re-tente le chargement après coup
            session.driver.get(final_url)
        except NoAlertPresentException:
            pass
    time.sleep(3)
    
    try:
        alert = session.driver.switch_to.alert
        # print("Alerte détectée :", alert.text)
        alert.accept()
    except Exception:
        pass
    
    more_filters = session.driver.find_element(By.CSS_SELECTOR, "button.more-filters")
    more_filters.click()
    time.sleep(1)

    search_bar = WebDriverWait(session.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search")))
    time.sleep(2)

    filters = session.driver.find_elements(By.CLASS_NAME, "filtres-prioritaires-button")

    ville_btn = filters[6]
    ville_btn.click()
    time.sleep(0.5)

    for ville in villes:
        ville_search_bar = session.driver.find_element(By.CSS_SELECTOR, "input[class='el-select__input']")
        ville_search_bar.clear()
        ville_search_bar.send_keys(ville)
        try:
            WebDriverWait(session.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "el-select-dropdown__item")))
        except Exception:
            print(f"Ville {ville} non trouvée")
            continue
        time.sleep(1)
        session.driver.find_elements(By.CLASS_NAME, "el-select-dropdown__item")[0].click()
        time.sleep(0.5)

    search_bar.send_keys(Keys.ENTER)
    time.sleep(3)

