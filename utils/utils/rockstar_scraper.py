import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("bot")

def fetch_latest_rockstar_news():
    # URL oficial de notícias do GTA Online na Rockstar Games
    url = "https://www.rockstargames.com/gta-online/newswire"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # O site da Rockstar utiliza elementos estruturados; tentamos pegar a primeira notícia em destaque
        # Como alternativa segura e estável para JSON/RSS da Rockstar:
        rss_url = "https://www.rockstargames.com/newswire/feed.xml"
        rss_response = requests.get(rss_url, headers=headers, timeout=15)
        
        if rss_response.status_code == 200:
            rss_soup = BeautifulSoup(rss_response.text, "xml")
            item = rss_soup.find("item")
            
            if item:
                title = item.find("title").text if item.find("title") else "Nova Notícia da Rockstar"
                link = item.find("link").text if item.find("link") else "https://www.rockstargames.com/gta-online/newswire"
                pub_date = item.find("pubDate").text if item.find("pubDate") else ""
                
                # Tenta achar a imagem dentro do conteúdo ou descrição do RSS
                description = item.find("description")
                image_url = "https://i.imgur.com/4X1kR5W.png" # Imagem padrão caso não ache
                if description:
                    desc_soup = BeautifulSoup(description.text, "html.parser")
                    img_tag = desc_soup.find("img")
                    if img_tag and img_tag.get("src"):
                        image_url = img_tag.get("src")

                return {
                    "success": True,
                    "title": title,
                    "link": link,
                    "date": pub_date[:16], # Corta para exibir data/hora limpa
                    "image_url": image_url
                }

        return {"success": False, "error": "Nenhuma notícia encontrada no feed."}

    except Exception as e:
        logger.error(f"Erro ao buscar notícias da Rockstar: {e}")
        return {"success": False, "error": str(e)}

