import requests
import logging

logger = logging.getLogger(__name__)

def validate_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=(3, 5))
        if response.status_code == 200:
            logger.info(f"✅ URL válida: {url}")
            return {"success": True, "status": "valid"}
        else:
            logger.warning(f"URL inválida: {url} - Status {response.status_code}")
            return {"success": True, "status": "invalid" ,"reason": f"Status code {response.status_code}"}
    except requests.RequestException as e:
        return {"success": False, "reason": str(e)}