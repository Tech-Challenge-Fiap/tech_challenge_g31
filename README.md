## Sistema de criação e gerenciamento de pedidos realizado para o Tech Challenge FIAP - SOAT - Grupo 31

## Guia Rápido para Executar a Aplicação Flask
Este guia rápido descreve como configurar e executar a aplicação Flask usando Docker Compose e migrações de banco de dados.

## Passo 1: Iniciar o Ambiente com o Docker Compose
Certifique-se de ter o Docker Compose instalado em sua máquina. Se não o tiver, instale-o.
No diretório raiz do projeto, execute o seguinte comando para iniciar o ambiente:
- docker-compose up --build -V
Isso criará e iniciará os contêineres necessários para a aplicação.

## Passo 2: Acessar o Container da Aplicação WEB
Após a conclusão do Passo 1, você pode acessar o container da aplicação WEB. Use o seguinte comando:
- docker-compose exec web bash
Isso o levará para dentro do container da aplicação.

## Passo 3: Realizar a Migração das Tabelas do Banco de Dados
Dentro do container da aplicação, execute o seguinte comando para criar as migrações das tabelas do banco de dados:
- flask db migrate
Este comando gerará os arquivos de migração.

## Passo 4: Atualizar o Banco de Dados para Criar as Tabelas
Agora, você pode aplicar as migrações para criar as tabelas no banco de dados. Execute o seguinte comando dentro do container da aplicação:
- flask db upgrade
Isso aplicará as migrações e criará as tabelas no banco de dados.

## Passo 5: Testar a Aplicação
Agora, você está pronto para testar a aplicação. Você pode usar o Postman ou qualquer outra ferramenta de teste que preferir para interagir com a aplicação.

## Contribuindo
Se você deseja contribuir para o projeto, envie uma mensagem para um integrante da organização.