import logging
from datetime import datetime

logger = logging.getLogger("bot")

def fetch_gun_van_data():
    try:
        # Pega a data atual formatada (ex: 24/07/2026)
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        
        # Link direto para o mapa interativo oficial filtrado na Gun Van
        map_link = "https://gtamap.net/map/gtao?city=ls&layer=game&groups=gun_van"
        
        # A imagem do mapa geral com os pontos
        map_image = "https://cdn.discordapp.com/attachments/1529474596368285832/1530378142148198541/gta-v-agency-suv-service-dropoff-location-maps-quick-travel-v0-tmsu6d1lbzca1_1.png?ex=6a655b36&is=6a6409b6&hm=4f8520bfa43f6c9829ced6548db02b5f18deb7dd7d789f451aa7066035187c1e&"

        return {
            "success": True,
            "location": f"Consulte o mapa interativo abaixo",
            "image_url": map_image,
            "link": map_link
        }

    except Exception as e:
        logger.error(f"Erro ao gerar dados da Gun Van: {e}")
        return {"success": False, "error": str(e)}

