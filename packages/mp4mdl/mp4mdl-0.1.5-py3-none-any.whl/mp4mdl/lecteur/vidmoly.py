from ..scrap import get_m3u8_url, get_best_qualite_url
from ..download import segment_downloader


def vidmoly(url, file_name, logger):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',"Referer": "https://vidmoly.to/","Origin": "https://vidmoly.to"}
    user_agent = headers['User-Agent']
    headers_dict = {
    'Referer': headers['Referer'],
    'Origin': headers['Origin']
    }

    match = [r'(https?://[^\s]+/master\.m3u8\?[^\s"]+)', r'(https?://[^\s]+/master\.m3u8)']
    
    m3u8_url = get_m3u8_url(url=url, headers=headers, match= match, list_match=True, logger=logger)
    if not m3u8_url:
        return False

    best_qualite_url = get_best_qualite_url(m3u8_url=m3u8_url, headers=headers, logger=logger)
    if not best_qualite_url:
        return False

    downloader = segment_downloader(best_qualite_url=best_qualite_url, headers_dict=headers_dict, user_agent=user_agent, file_name=file_name, logger=logger)
    status = downloader.download_segments()
    return status

    
