import requests
from requests.exceptions import ConnectionError, Timeout, InvalidURL, RequestException, MissingSchema
import logging

logger = logging.getLogger(__name__)

def validate_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=(5, 10))

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

    except ConnectionError as e:
        # Caso a URL não exista ou tenha problemas de conexão
        result = "invalid"
        status = "error"
        comment = f"Não foi possível estabelecer uma conexão com o servidor da URL: {url}. Verifique a URL ou tente novamente mais tarde."
        logger.error(f"ConnectionError: {str(e)}")

    except Timeout as e:
        # Caso a requisição tenha expirado (problema de tempo de resposta)
        result = "invalid"
        status = "error"
        comment = f"A requisição para a URL {url} expirou. O servidor não respondeu a tempo."
        logger.error(f"TimeoutError: {str(e)}")

    except InvalidURL as e:
        # Caso a URL fornecida seja mal formada
        result = "invalid"
        status = "error"
        comment = f"A URL fornecida ({url}) é mal formada. Verifique a URL."
        logger.error(f"InvalidURL: {str(e)}")

    except MissingSchema as e:
        # Caso o esquema da URL não seja fornecido
        result = "invalid"
        status = "error"
        comment = f"A URL fornecida ({url}) está sem o esquema (como http ou https). Verifique a URL."
        logger.error(f"MissingSchema: {str(e)}")

    except RequestException as e:
        print(type(e))
        # Caso ocorra qualquer outro erro genérico durante a requisição
        result = "invalid"
        status = "error"
        comment = f"Erro ao validar a URL {url}: {str(e)}"
        logger.error(f"RequestException: {str(e)}")

    return {
        "result": result,
        "status": status,
        "comment": comment
    }