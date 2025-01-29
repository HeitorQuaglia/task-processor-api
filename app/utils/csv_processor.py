import pandas as pd
from app.utils.s3_utils import download_from_s3
import logging

logger = logging.getLogger(__name__)

def process_csv(file_url: str, column_name: str):
    """
    Processa o CSV armazenado no S3, verifica a coluna e realiza o cálculo.
    :param file_url: URL do arquivo CSV no S3.
    :param column_name: Nome da coluna a ser verificada e calculada.
    :return: Dicionário com o resultado do processamento.
    """
    try:
        # Baixar o arquivo CSV do S3 usando a chave do arquivo
        file_key = file_url.split('/')[-1]  # Extrair o file_key da URL
        file_content = download_from_s3(file_key)

        # Validar se o conteúdo é um CSV válido
        from io import BytesIO
        csv_data = BytesIO(file_content)
        df = pd.read_csv(csv_data)

        # Verificar se a coluna existe
        if column_name not in df.columns:
            return {"status": "error", "result": False, "comment": f"A coluna '{column_name}' não existe no CSV."}

        # Verificar se os valores são numéricos
        if not pd.to_numeric(df[column_name], errors='coerce').notnull().all():
            return {"status": "error", "result": False, "comment": f"Nem todos os valores na coluna '{column_name}' são numéricos."}

        # Calcular a média dos valores na coluna
        column_values = pd.to_numeric(df[column_name], errors='coerce')
        average_value = column_values.mean()

        # Retornar sucesso com o valor calculado
        return {"status": "completed", "result": average_value, "comment": f"Média calculada para a coluna '{column_name}': {average_value}"}

    except Exception as e:
        logger.error(f"Erro ao processar o CSV: {e}")
        return {"status": "error", "result": False, "comment": "Erro interno ao processar o arquivo CSV."}
