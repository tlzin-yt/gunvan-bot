import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("bot")

def fetch_latest_rockstar_news():
    url = "https://www.rockstargames.com/gta-online/newswire"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.9"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Tenta buscar os dados estruturados do site da Rockstar
        # Buscando o primeiro card de notícia principal
        article = soup.find("article") or soup.find("div", class_="news-article")
        
        title = "Nova Atualização do GTA Online"
        link = url
        image_url = "https://i.imgur.com/4X1kR5W.png"
        date = "Recente"

        if article:
            title_tag = article.find("h3") or article.find("h2")
            if title_tag:
                title = title_tag.text.strip()
                
            link_tag = article.find("a", href=True)
            if link_tag:
                href = link_tag["href"]
                link = href if href.startswith("http") else f"https://www.rockstargames.com{href}"
                
            img_tag = article.find("img")
            if img_tag and img_tag.get("src"):
                image_url = img_tag.get("src")

            date_tag = article.find("time")
            if date_tag:
                date = date_tag.text.strip()

        return {
            "success": True,
            "title": title,
            "link": link,
            "date": date,
            "image_url": image_url
        }

    except Exception as e:
        logger.error(f"Erro ao buscar notícias da Rockstar: {e}")
        return {"success": False, "error": str(e)}

