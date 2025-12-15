import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from data.utils.session import Session
from selenium.webdriver.common.by import By
from urllib.parse import urlencode

def search_duckduckgo(session: Session, query, max_results=5):
    url = "https://google.com/search"
    params = {"q": query}
    session.driver.get(f"{url}?{urlencode(params)}")
    time.sleep(3)
    links = []
    try:
        center = session.driver.find_element(By.ID, "center_col")
        for a in center.find_elements(By.TAG_NAME, "a"):
            href = a.get_attribute("href")
            if href and href.startswith("http"): # type: ignore
                links.append(href)
            if len(links) >= max_results:
                break
    except:
        pass
    return links