import requests
from requests.exceptions import ConnectionError, Timeout, InvalidURL, RequestException, MissingSchema
import logging

logger = logging.getLogger(__name__)

def validate_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=(5, 10))

        if response.status_code < 400:
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

    except (ConnectionError, Timeout, InvalidURL, MissingSchema, RequestException) as e:

        error_messages = {
            ConnectionError: f"Não foi possível estabelecer conexão com {url}. Verifique a URL ou tente novamente mais tarde.",
            Timeout: f"A requisição para {url} expirou. O servidor não respondeu a tempo.",
            InvalidURL: f"A URL fornecida ({url}) é mal formada. Verifique a URL.",
            MissingSchema: f"A URL fornecida ({url}) está sem o esquema (como http ou https). Verifique a URL.",
            RequestException: f"Erro ao validar a URL {url}: {str(e)}"
        }

        comment = error_messages.get(type(e), f"Erro desconhecido ao validar {url}: {str(e)}")

        logger.error(f"{type(e).__name__}: {comment}")

        return {
            "result": "invalid",
            "status": "error",
            "comment": comment
        }