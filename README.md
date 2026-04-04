
# MVP Marketplace — Documentação

Documentação oficial do MVP Marketplace.

## Estrutura
/docs
  - 01-requisitos.md
  - 02-arquitetura.md
  - 03-planejamento.md

## Passos do Projeto
  - Faça um git clone do projeto
  - Na pasta raiz do projeto (o primeiro mkbackend) crie um arquivo e o nomeie como .env
  - Insira o seguinte código nele:
    
    DATABASE_URL= *****  (informe a connection string)
    
    SECRET_KEY=Admin123  (aqui utilize sua senha do github)
    
    DEBUG=True
    
    ``


  - Na raiz do projeto, crie um arquivo e o nomeie como .gitignore
  - Insira o seguinte código nele:    
    .venv/
    env/
    
    __pycache__/
    *.py[cod]
    
    .env
    

    
## Execute as Migrações
  - python manage.py makemigrations
  - python manage.py migrate

## Executar servidor: 
  - python manage.py runserver

## Swagger: 
  - http://localhost:8000/api/docs/

