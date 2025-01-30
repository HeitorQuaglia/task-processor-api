# 📌 CSV & URL Processor API 
Esta API permite validar URLs e processar arquivos CSV carregados pelo usuário. O processamento é realizado de forma assíncrona, utilizando **FastAPI** com **BackgroundTasks**, e os resultados são armazenados no **MongoDB**. O armazenamento de arquivos é feito via **AWS S3**.

## 📝 Funcionalidades 
- ✅ Validar URLs - Verifica se a URL fornecida é válida e retorna o status.
- ✅ Processar CSVs - Calcula a média de uma coluna específica em arquivos CSV.
- ✅ Armazenamento em MongoDB - Mantém o status das tarefas para consulta posterior.
- ✅ Execução Assíncrona - Utiliza BackgroundTasks do FastAPI para processamento paralelo.
- ✅ Armazenamento S3 - Upload e recuperação de arquivos via S3.

## 🏗 Arquitetura do Projeto

📂 **app/**  
 ┣ 📂 **config/** - Configurações (MongoDB, LocalStack, etc.)  
 ┣ 📂 **models/** - Definições de modelos de dados (Pydantic)  
 ┣ 📂 **repositories/** - Repositórios para interação com MongoDB  
 ┣ 📂 **routers/** - Definição das rotas da API  
 ┣ 📂 **services/** - Lógica de negócios da aplicação  
 ┣ 📂 **utils/** - Utilitários como validação de URL, processamento de CSV, etc.  
 ┣ 📜 **main.py** - Ponto de entrada da API FastAPI  
 ┣ 📜 **app.py** - Configuração da API FastAPI  
📂 **tests/** - Testes automatizados com pytest  
📜 **requirements.txt** - Dependências do projeto  
📜 **Dockerfile** - Configuração do Docker  
📜 **docker-compose.yml** - Configuração do ambiente de desenvolvimento  
📜 **README.md** - Documentação do projeto  

## 🚀 Instalação e Configuração
### 1️⃣ Clonar o repositório
```
git clone https://github.com/HeitorQuaglia/dnc-code-challenge.git
cd dnc-code-challenge
```
### 2️⃣ Criar o arquivo .env
Crie um arquivo **.env** na raiz do projeto e configure as variáveis (disponibilizei um arquivo .env.local que deve funcionar)
### 3️⃣ Subir os serviços com Docker
```
docker-compose up -d --build
```
### 4️⃣ Acessar o container do Localstack
```
docker exec -it localstack bash
```
### 5️⃣ Criar o bucket S3 para armazenar os arquivos
```
aws --endpoint-url=http://localhost:4566 s3api create-bucket --bucket csv-files-processor --region us-east-1
```
obs: caso tenha substituído o nome do arquivo ou a região em .env, substituir aqui também

## 🔥 Uso da API
### 📍 1. Docs
Docs disponíveis em http://localhost:8000/docs

### 📍 2. Processar uma URL
📌 Endpoint: POST /process-data  

📤 Request:
```
curl --location 'http://localhost:8000/process-data' \
--form 'url="https://stackoverflow.com"'
```
📥 Response
```
{
    "task_id": "9409aa7e-2033-4e94-b00e-fa5c79fa0928",
    "url": "https://stackoverflow.com",
    "message": "Processando validação de URL"
}
```

### 📍 3. Processar um CSV
📌 Endpoint: POST /process-data  

📤 Request:
``` 
curl --location 'http://localhost:8000/process-data' \
--form 'file=@caminho/para/o/arquivo.csv"' \
--form 'column="1"'
```
📥 Response
```
{
    "task_id": "df6e0d9b-f8b2-42d3-b372-81e11216a034",
    "file_url": "https://csv-files-processor.s3.us-east-1.amazonaws.com/uploads/d81894e5-74dd-4a0f-8b09-ad406d26da1c.csv",
    "message": "Processando CSV..."
}
```
### 📍 4. Consultar o status de uma tarefa
📌 Endpoint: GET /results/{task_id}

📤 Request:
``` 
curl -X 'GET' 'http://localhost:8000/results/123e4567-e89b-12d3-a456-426614174000'
```

📥 Response (exemplo para um CSV)
```
{
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "type": "csv",
    "status": "completed",
    "result": 5.0,
    "comment": "Média calculada para a coluna '1': 5.0",
    "task_metadata": {
      "file_url": "https://csv-files-processor.s3.us-east-1.amazonaws.com/uploads/d81894e5-74dd-4a0f-8b09-ad406d26da1c.csv",
      "column_name": "1"
    }
}
```
📥 Response (exemplo para URL)
```
{
    "task_id":"c1bb343e-51a0-4295-8263-f009152e8258",
    "type":"url",
    "status":"completed",
    "result":"valid",
    "comment":"O link https://stackoverflow.com foi validado com sucesso.",
    "task_metadata": {
        "url":"https://stackoverflow.com"
        }
    }
```
## ✅ Testes
Para rodar os testes automatizados:

```
pytest -s -v
```

## 📌 Possíveis Melhorias

- Melhorar a escalabilidade usando fila de mensagens (Celery ou Redis) 📦