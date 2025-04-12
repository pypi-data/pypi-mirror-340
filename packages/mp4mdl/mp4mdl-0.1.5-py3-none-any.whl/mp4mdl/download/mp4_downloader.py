import logging
import urllib3
import time

class mp4_downloader:
    def __init__(self, headers, url, file_name, logger):
        self.headers = headers
        self.url = url
        self.file_name = file_name
        self.logger = logger

    def download(self):
        urllib3_logger = logging.getLogger("urllib3")
        urllib3_logger.setLevel(logging.WARNING)
        
        try:
            http = urllib3.PoolManager()
            response = http.request('GET', self.url, headers=self.headers, preload_content=False)
            
            if response.status != 200:
                self.logger.error(f"Erreur lors du téléchargement: {response.status}")
                return False
            
            with open(self.file_name, 'wb') as f:
                chunk_size = 512 * 1024

                total_downloaded = 0
                start_time = time.time()
                
                for data in response.stream(chunk_size):
                    f.write(data)
                    total_downloaded += len(data)
                    
                    # Ajuster la taille du chunk en fonction de la vitesse
                    elapsed = time.time() - start_time
                    if elapsed >= 1:  # Ajuster toutes les secondes
                        speed = total_downloaded / elapsed  # octets/seconde
                        
                        # Augmenter/diminuer chunk_size selon la vitesse
                        if speed > 1024*1024:  # Si > 1 MB/s
                            chunk_size = min(chunk_size * 2, 5*1024*1024)  # Max 5MB
                        elif speed < 512*1024:  # Si < 512 KB/s
                            chunk_size = max(chunk_size // 2, 4096)  # Min 4KB

                        total_downloaded = 0
                        start_time = time.time()
                            
            response.release_conn()
            self.logger.debug(f"Téléchargement réussi : {self.file_name}")
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Erreur lors du téléchargement: {str(e)}")
            return False
