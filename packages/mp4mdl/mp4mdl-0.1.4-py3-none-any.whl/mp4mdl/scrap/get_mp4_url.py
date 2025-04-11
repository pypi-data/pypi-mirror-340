import requests
from bs4 import BeautifulSoup
import re


def get_mp4_url(url, headers, logger, match=None, meta=None):
    if not match and not meta:
        logger.error("match ou meta non definis")
        return None
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        logger.error(f"Erreur lors de la requête HTTP: {e}")
        return None
    except Exception as e:
        logger.error(f"Erreur inattendue: {e}")
        return None
    
    if match:
        scripts = soup.find_all('script', type="text/javascript")
        
        if not scripts:
            logger.error("Aucun script JavaScript trouvé dans la page")
            return None
        
        for script in scripts:
            script_content = script.string
            if script_content:
                matchs = re.search(match, script_content)
                if matchs:
                    video_url = matchs.group(1)
                    if not video_url:
                        logger.error("URL de la vidéo non trouvée dans le script")
                        return None
                    else:
                        return video_url
    elif meta:
        meta_tag = soup.find("meta", property=meta)

        if not meta_tag:
            logger.error("Aucune vidéo trouvée dans la page")
            return None
        
        video_url = meta_tag['content']
        if not video_url:
            logger.error("URL de la vidéo non trouvée")
            return None
            
        return video_url
    else:
        logger.error("Aucun match ou meta trouvé")
        return None
                    