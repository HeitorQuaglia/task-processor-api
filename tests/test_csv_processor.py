import pytest
from unittest.mock import patch


@pytest.mark.parametrize("csv_content, column_index, expected_result", [
    (
            "A,B,C\n1,2,3\n4,5,6\n7,8,9\n",
            1,
            {"status": "completed", "result": 5.0, "comment": "Média calculada para a coluna de índice '1': 5.0"}
    ),
])
@patch("app.utils.csv_processor.download_from_s3", return_value=b"A,B,C\n1,2,3\n4,5,6\n7,8,9\n")
def test_process_csv_success(mock_download, csv_content, column_index, expected_result):
    file_url = "https://s3.com/sample.csv"

    result = process_csv(file_url, column_index)

    mock_download.assert_called_once_with("sample.csv")

    assert result == expected_result


@pytest.mark.asyncio
@patch("app.utils.csv_processor.download_from_s3", return_value=b"")
def test_process_csv_empty_file(mock_download):
    file_url = "https://s3.com/empty.csv"

    result = process_csv(file_url, column_index=0)

    mock_download.assert_called_once_with("empty.csv")

    assert result == {"status": "error", "result": False, "comment": "Arquivo CSV está vazio."}


@pytest.mark.asyncio
@patch("app.utils.csv_processor.download_from_s3", return_value=b"A,B,C\n1,2,3\n4,5,6\n7,8,9\n")  # CSV com 3 colunas
def test_process_csv_invalid_column_index(mock_download):
    file_url = "https://s3.com/sample.csv"
    invalid_index = 5

    result = process_csv(file_url, invalid_index)

    mock_download.assert_called_once_with("sample.csv")

    assert result == {
        "status": "error",
        "result": False,
        "comment": f"O índice '{invalid_index}' está fora do intervalo válido."
    }


@pytest.mark.asyncio
@patch("app.utils.csv_processor.download_from_s3",
       return_value=b"A,B,C\nx,y,z\nw,t,u\n")
def test_process_csv_non_numeric_column(mock_download):
    file_url = "https://s3.com/sample.csv"
    column_index = 1

    result = process_csv(file_url, column_index)

    mock_download.assert_called_once_with("sample.csv")

    assert result == {
        "status": "error",
        "result": False,
        "comment": f"A coluna '{column_index}' contém valores inválidos ou está vazia."
    }


import pytest
from unittest.mock import patch
from app.utils.csv_processor import process_csv


@pytest.mark.asyncio
@patch("app.utils.csv_processor.download_from_s3", return_value=b'{"foo":"bar"}')
def test_process_csv_invalid_format(mock_download):
    file_url = "https://s3.com/invalid_format.csv"

    result = process_csv(file_url, column_index=0)

    mock_download.assert_called_once_with("invalid_format.csv")

    assert result == {
        "status": "error",
        "result": False,
        "comment": "O arquivo não está em um formato de CSV válido."
    }
