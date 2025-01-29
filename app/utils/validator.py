import requests
import logging

logger = logging.getLogger(__name__)

def validate_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=(3, 5))

        if response.status_code == 200:
            result = "valid"
            comment = f"O link {url} foi validado com sucesso."
            status = "completed"
        else:
            result = "invalid"
            comment = f"O link {url} é inválido. Status: {response.status_code}"
            status = "completed"

        return {
            "result": result,
            "status": status,
            "comment": comment
        }
    except requests.RequestException as e:
        return {
            "result": "invalid",
            "status": "error",
            "comment": f"Erro ao validar a URL: {str(e)}"
        }