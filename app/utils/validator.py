import requests
from requests.exceptions import ConnectionError, Timeout, InvalidURL, RequestException, MissingSchema
import logging

from app.utils.error_messages import ErrorMessages

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
            ConnectionError: lambda input_url: ErrorMessages.URL_CONNECTION_ERROR.format(url=input_url),
            Timeout: lambda input_url: ErrorMessages.URL_TIMEOUT_ERROR.format(url=input_url),
            InvalidURL: lambda input_url: ErrorMessages.URL_INVALID_FORMAT.format(url=input_url),
            MissingSchema: lambda input_url: ErrorMessages.URL_MISSING_SCHEMA,
            RequestException: lambda input_url, error_detail: ErrorMessages.URL_VALIDATION_GENERIC_ERROR.format(
                url=input_url, error_message=str(error_detail)
            )
        }

        error_handler = error_messages.get(type(e), lambda input_url, error_detail:
        f"Erro desconhecido ao validar {input_url}: {str(error_detail)}")

        if callable(error_handler):
            comment = error_handler(url, e) if error_handler.__code__.co_argcount > 1 else error_handler(url)
        else:
            comment = error_handler

        logger.error(f"{type(e).__name__}: {comment}")

        return {
            "result": "invalid",
            "status": "error",
            "comment": comment
        }
