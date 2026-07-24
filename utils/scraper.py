import logging
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger("bot")


def fetch_gun_van_data():
    url = "https://gtamap.net/gta-online/daily/gun-van"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title_element = soup.find("h1") or soup.find("title")
        location_name = title_element.get_text(strip=True) if title_element else "Localização Atual"

        img_element = soup.find("img", class_="map-image") or soup.find("meta", property="og:image")

        if img_element:
            image_url = img_element.get("content") if img_element.name == "meta" else img_element.get("src")
        else:
            image_url = "https://i.imgur.com/4X1kR0W.png"

        return {
            "success": True,
            "location": location_name,
            "image_url": image_url,
            "link": url,
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao acessar o site da Gun Van: {e}")
        return {"success": False, "error": str(e)}

