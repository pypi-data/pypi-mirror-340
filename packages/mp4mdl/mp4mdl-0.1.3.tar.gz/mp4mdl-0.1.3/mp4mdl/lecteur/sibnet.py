from ..scrap import get_mp4_url
from ..download import mp4_downloader

def sibnet(url, file_name, logger):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive", "Upgrade-Insecure-Requests": "1"}
    match = r'player\.src\(\[\{src: "(.*?)"'
    video_url = get_mp4_url(url, headers, match=match, logger=logger)
    if not video_url:
        return False
        
    mp4_url = f"https://video.sibnet.ru{video_url}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36", "Referer": f"https://video.sibnet.ru"}
    downloader = mp4_downloader(headers, mp4_url, file_name, logger)
    status = downloader.download()
    return status

