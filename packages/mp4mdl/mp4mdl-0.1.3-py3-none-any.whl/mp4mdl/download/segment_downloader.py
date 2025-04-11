import os
import ffmpeg

class segment_downloader:
    def __init__(self, best_qualite_url, headers_dict, file_name, logger):
        self.best_qualite_url = best_qualite_url
        self.file_name = file_name
        self.logger = logger
        self.headers_dict = headers_dict

    def download_segments(self):
        try:
            if os.path.exists(self.file_name):
                os.remove(self.file_name)
            
            # Créer le stream d'entrée avec les headers
            input_stream = ffmpeg.input(
                self.best_qualite_url,
                protocol_whitelist="file,https,http,tls,tcp",
                headers=self.headers_dict
            )
            
            # Configurer le stream de sortie
            output_stream = ffmpeg.output(
                input_stream,
                self.file_name,
                c='copy'  # Copier les streams sans ré-encoder
            )
            
            # Exécuter la commande
            ffmpeg.run(output_stream, capture_stdout=True, capture_stderr=True)
            
            self.logger.debug(f"Téléchargement des segments réussi : {self.file_name}")
            return True
            
        except ffmpeg.Error as e:
            error_message = e.stderr.decode()
            if "403 Forbidden" in error_message:
                self.logger.error(f"Erreur ffmpeg 403: Forbidden for url - {self.best_qualite_url}")
                self.logger.debug(f"{self.headers_dict}, {self.best_qualite_url}, {self.file_name}")
                return False
            self.logger.error(f"Erreur ffmpeg : {error_message}")
            return False
        except Exception as e:
            self.logger.error(f"Erreur lors du téléchargement des segments : {e}")
            return False
