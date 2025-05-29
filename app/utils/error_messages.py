class ErrorMessages:
    # Erros Internos
    FILE_NOT_UPLOADED = "Arquivo não foi enviado ou não foi possível processá-lo."
    # Erros de Tasks
    TASK_NOT_FOUND_MSG = "Task não encontrada."

    # Erros de Arquivo
    INVALID_FILE_TYPE = "Arquivo inválido. Apenas arquivos CSV são aceitos."
    S3_UPLOAD_ERROR = "Erro ao fazer upload do arquivo para o S3."
    UNEXPECTED_FILE_PROCESSING_ERROR = "Erro inesperado ao tentar processar o arquivo."
    FILE_DOWNLOAD_ERROR = "Erro ao fazer download do arquivo."
    INVALID_COLUMN_INDEX = "Índice da coluna inválido."

    # Erros de URL
    INVALID_URL = "URL fornecida é inválida."
    URL_VALIDATION_ERROR = "Erro ao validar o formato da URL."
    URL_MISSING_SCHEMA = "A URL fornecida está sem o esquema (como http ou https). Verifique a URL."
    URL_CONNECTION_ERROR = "Não foi possível estabelecer conexão com {url}. Verifique a URL ou tente novamente mais tarde."
    URL_TIMEOUT_ERROR = "A requisição para {url} expirou. O servidor não respondeu a tempo."
    URL_INVALID_FORMAT = "A URL fornecida ({url}) é mal formada. Verifique a URL."
    URL_VALIDATION_GENERIC_ERROR = "Erro ao validar a URL {url}: {error_message}."
