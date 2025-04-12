import logging
import os
import uuid
from urllib.parse import urlparse
import shutil

from .lecteur import *

class mp4mdl:
    """
    Classe pour télécharger des vidéos depuis différents sites.
    
    Args:
        download_path (str): Chemin où télécharger temporairement les fichiers
        final_path (str): Chemin final où déplacer les fichiers
        url (str): URL de la vidéo à télécharger
        logger (logging.Logger, optional): Logger personnalisé (par défaut, "MP4mdl" avec le titre "MP4mdl-{title})
        title (str, optional): Titre pour le logger seulement si logger est None 
    """
    
    SUPPORTED_SITES = {
        "video.sibnet.ru": (sibnet, ["url", "file_name", "logger"]),
        "vidmoly.to": (vidmoly, ["url", "file_name", "logger"]),
        "oneupload.to": (oneupload, ["url", "file_name", "logger"]),
        "sendvid.com": (sendvid, ["url", "file_name", "logger"])
    }
    
    def __init__(self, download_path, final_path, url, logger=None, title=None):
        # Validation des entrées
        if not all([download_path, final_path, url]):
            raise ValueError("Tous les paramètres sont requis")
            
        # Initialisation du logger
        if title:
            self.logger = logger or logging.getLogger(f"MP4mdl-{title}")
        else:
            self.logger = logger or logging.getLogger(f"MP4mdl")
        
        # Normalisation des chemins
        self.download_path = os.path.normpath(download_path)
        self.final_path = os.path.normpath(final_path)
        self.url = url
        
        # Création du dossier temporaire
        self._setup_temp_directory()

    def download(self):
        site = self.SUPPORTED_SITES
        parsed_url = urlparse(self.url)
        base_name = parsed_url.netloc

        downloaded = False
        if base_name in site:
            # Préparer les arguments pour la fonction
            handler, param_names = site[base_name]
            args = {param: getattr(self, param) for param in param_names}

            self.logger.debug(f"call de la function {handler.__name__} avec les arguments {args}")
            # Appeler la fonction avec les bons arguments
            status = handler(**args)
            self.logger.debug(f"status: {status}")
            if status:
                try:
                    if os.path.exists(self.file_name):
                        shutil.move(self.file_name, self.final_path)
                        downloaded = True
                    else:
                        self.logger.error(f"Le fichier source n'existe pas: {self.file_name}")
                        downloaded = False
                except Exception as e:
                    self.logger.error(f"Erreur lors du déplacement du fichier: {e}")
                    downloaded = False
        else:
            self.logger.error(f"Le site {base_name} n'est pas supporté")
            downloaded = False
        try:
            if os.path.exists(self.temp_path):
                shutil.rmtree(self.temp_path)
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression du dossier temporaire: {e}")
        return downloaded

    def _setup_temp_directory(self):
        self.temp_name = str(uuid.uuid5(uuid.NAMESPACE_URL, self.url))
        self.temp_path = os.path.join(self.download_path, self.temp_name)
        os.makedirs(self.temp_path, exist_ok=True)
        self.file_name = os.path.join(self.temp_path, f"{self.temp_name}.mp4")

        
