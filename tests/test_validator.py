import pytest
import requests
from unittest.mock import patch, MagicMock

from app.utils.validator import validate_url

@pytest.mark.asyncio
@patch("requests.head")
def test_validate_url_success(mock_head):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_head.return_value = mock_response

    url = "https://example.com"
    result = validate_url(url)

    assert result["result"] == "valid"
    assert result["status"] == "completed"
    assert "foi validado com sucesso" in result["comment"]

@pytest.mark.asyncio
@patch("requests.head")
def test_validate_url_404(mock_head):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_head.return_value = mock_response

    url = "https://example.com/notfound"
    result = validate_url(url)

    assert result["result"] == "invalid"
    assert result["status"] == "completed"
    assert "O link https://example.com/notfound é inválido. Status: 404" in result["comment"]

@pytest.mark.asyncio
@patch("requests.head", side_effect=requests.ConnectionError)
def test_validate_url_connection_error(mock_head):
    url = "https://offline-website.com"
    result = validate_url(url)

    assert result["result"] == "invalid"
    assert result["status"] == "error"
    assert "Não foi possível estabelecer conexão" in result["comment"]

@pytest.mark.asyncio
@patch("requests.head", side_effect=requests.RequestException("Erro genérico"))
def test_validate_url_generic_exception(mock_head):
    url = "https://example.com"
    result = validate_url(url)

    assert result["result"] == "invalid"
    assert result["status"] == "error"
    assert "Erro ao validar a URL" in result["comment"]

