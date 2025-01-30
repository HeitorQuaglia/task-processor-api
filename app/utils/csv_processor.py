import pandas as pd
import logging
from io import BytesIO
from app.utils.s3_utils import download_from_s3

logger = logging.getLogger(__name__)

def process_csv(file_url: str, column_index: int):
    """
    Processa o CSV armazenado no S3, verifica a coluna pelo índice e calcula a média.

    :param file_url: URL do arquivo CSV no S3.
    :param column_index: Índice da coluna a ser processada.
    :return: Dicionário com o resultado do processamento.
    """
    try:
        file_key = file_url.split('/')[-1]
        file_content = download_from_s3(file_key)

        csv_data = BytesIO(file_content)
        df = pd.read_csv(csv_data)

        if df.empty:
            return {"status": "error", "result": False, "comment": "Arquivo CSV está vazio."}

        if column_index < 0 or column_index >= len(df.columns):
            return {"status": "error", "result": False,
                    "comment": f"O índice '{column_index}' está fora do intervalo válido."}

        column_name = df.columns[column_index]
        column_values = pd.to_numeric(df[column_name], errors='coerce')

        if column_values.isna().all():
            return {"status": "error", "result": False,
                    "comment": f"A coluna '{column_index}' contém valores inválidos ou está vazia."}

        average_value = round(column_values.mean(), 2)

        return {"status": "completed", "result": average_value,
                "comment": f"Média calculada para a coluna de índice '{column_index}': {average_value}"}

    except FileNotFoundError:
        logger.error(f"Arquivo não encontrado: {file_url}")
        return {"status": "error", "result": False, "comment": "Arquivo não foi encontrado no S3."}

    except  pd.errors.ParserError:
        logger.error(f"Erro ao analisar o CSV: {file_key}")
        return {"status": "error", "result": False, "comment": "O arquivo não está em um formato de CSV válido."}

    except ValueError as ve:
        logger.error(f"Erro de valor: {ve}")
        return {"status": "error", "result": False, "comment": "Erro nos valores do arquivo CSV."}

    except Exception as e:
        logger.error(f"Erro ao processar o CSV: {e}")
        return {"status": "error", "result": False, "comment": "Erro interno ao processar o arquivo CSV."}
