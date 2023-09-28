### build da imagem do docker
`docker build -t telegram_scheduler:latest .`

### rodando o container -d
`docker run -d --name live4 telegram_scheduler:latest`

### Verificando status do container
`docker container ls`

### parando execucao do container
`docker stop live4`

### Deletando o container
`docker rm -f live4`
