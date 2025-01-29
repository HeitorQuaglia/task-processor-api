# Define as variáveis de ambiente para a AWS
$env:AWS_REGION = "us-east-1"
$env:AWS_ACCESS_KEY_ID = "test"
$env:AWS_SECRET_ACCESS_KEY = "test"

# Cria o bucket S3 chamado csv-files-processor
aws --endpoint-url=http://localhost:4566 s3api create-bucket --bucket csv-files-processor --region $env:AWS_REGION