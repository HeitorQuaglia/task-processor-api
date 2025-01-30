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

        if column_index < 0 or column_index >= len(df.columns):
            return {"status": "error", "result": False,
                    "comment": f"O índice '{column_index}' está fora do intervalo válido."}

        column_name = df.columns[column_index]

        if not pd.to_numeric(df[column_name], errors='coerce').notnull().all():
            return {"status": "error", "result": False,
                    "comment": f"Nem todos os valores na coluna de índice '{column_index}' são numéricos."}

        column_values = pd.to_numeric(df[column_name], errors='coerce')
        average_value = column_values.mean()

        return {"status": "completed", "result": average_value,
                "comment": f"Média calculada para a coluna de índice '{column_index}': {average_value}"}

    except Exception as e:
        logger.error(f"Erro ao processar o CSV: {e}")
        return {"status": "error", "result": False, "comment": "Erro interno ao processar o arquivo CSV."}
