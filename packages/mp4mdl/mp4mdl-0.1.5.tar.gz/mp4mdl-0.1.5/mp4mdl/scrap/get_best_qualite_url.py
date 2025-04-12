import requests
from bs4 import BeautifulSoup


def get_best_qualite_url(m3u8_url, headers, logger):
    try:
        response = requests.get(m3u8_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'URL m3u8: {e}")
        return None
    
    lines = response.text.splitlines()
    best_url = None
    best_resolution = (0, 0)

    for i, line in enumerate(lines):
        if line.startswith("#EXT-X-STREAM-INF"):
            # Extraire les informations de la ligne
            parts = line.split(",")
            
            # Récupérer la résolution
            resolution_str = next((part.split("=")[1] for part in parts 
                                if part.startswith("RESOLUTION=")), None) 

            if resolution_str and i + 1 < len(lines):
                width, height = map(int, resolution_str.split("x"))
                
                # Mettre à jour si meilleure résolution trouvée
                if (width, height) > best_resolution:
                    best_url = lines[i + 1]

    return best_url