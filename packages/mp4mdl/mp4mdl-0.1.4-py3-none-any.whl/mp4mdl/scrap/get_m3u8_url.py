import requests
from bs4 import BeautifulSoup
import re

def get_m3u8_url(url, headers, match, logger, list_match=False):
    if not match:
        logger.error("match non definis")
        return None
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'URL m3u8: {e}")
        return None
    
    if list_match: 
        for m in match:
            m3u8_url = find_match(soup, m, logger)
            if m3u8_url:
                return m3u8_url
        return None
    else:
        return find_match(soup, match, logger)


def find_match(soup, match, logger):
    if match:
        scripts = soup.find_all('script')
        for script in scripts:
            script_content = script.string
            if script_content:
                matchs = re.search(match, script_content)
                if matchs:
                    m3u8_url = matchs.group(1)
                    if not m3u8_url:
                        logger.error("m3u8 URL non trouvée dans le script")
                        return None
                    else:
                        return m3u8_url
