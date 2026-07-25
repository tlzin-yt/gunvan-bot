import logging
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger("bot")

def fetch_gun_van_data():
    url = "https://gtamap.net/map/gtao?city=ls&layer=game&groups=gun_van"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Tenta capturar o título ou descrição do local do dia no site
        location_name = "Localização Atual da Gun Van"
        title_tag = soup.find("h1") or soup.find("title") or soup.find("meta", property="og:title")
        if title_tag:
            location_name = title_tag.get_text(strip=True) if title_tag.name != "meta" else title_tag.get("content")

        # Tenta capturar a imagem do mapa do dia
        image_url = None
        img_tag = soup.find("meta", property="og:image") or soup.find("img", class_="map-image")
        if img_tag:
            image_url = img_tag.get("content") if img_tag.name == "meta" else img_tag.get("src")
            
        # Fallback caso ele não ache a imagem exata da página do dia
        if not image_url:
            image_url = "https://i.imgur.com/4X1kR5W.png"

        return {
            "success": True,
            "location": location_name,
            "image_url": image_url,
            "link": url
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao acessar o site da Gun Van: {e}")
        return {"success": False, "error": str(e)}
