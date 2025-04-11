from ..scrap import get_mp4_url
from ..download import mp4_downloader


def sendvid(url, file_name, logger):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive", "Upgrade-Insecure-Requests": "1"}
    meta = 'og:video'
    video_url = get_mp4_url(url, headers, meta=meta, logger=logger)
    if not video_url:
        return False

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36", "Referer": f"https://video.sibnet.ru"}
    downloader = mp4_downloader(headers, video_url, file_name, logger)
    status = downloader.download()
    return status



