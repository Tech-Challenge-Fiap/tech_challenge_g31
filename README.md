## Sistema de criação e gerenciamento de pedidos realizado para o Tech Challenge FIAP - SOAT - Grupo 31

## Guia Rápido para Executar a Aplicação Flask
Este guia rápido descreve como configurar e executar a aplicação Flask usando Docker Compose e migrações de banco de dados.

## Opção 1: Inicie o Ambiente com o Docker Compose
Certifique-se de ter o Docker Compose instalado em sua máquina. Se não o tiver, instale-o.
No diretório raiz do projeto, execute o seguinte comando para iniciar o ambiente:
```
docker-compose up --build -V
```
Isso criará e iniciará os contêineres necessários para a aplicação.
Acesse o serviço pela url [http://localhost:5000](http://localhost:5000)


## Opção 2: Inicie o Ambiente com Helm
No diretório raiz do projeto, execute os seguintes comandos:
```
helm package fiaptechchallenge
helm install fiaptechchallenge-0.1.0.tgz --generate-name
```
Com isso o servidor iniciará em seu cluster configurado.

Se o cluster não tiver configurado para exportar as portas para o host local, utilize o comando
```
kubectl port-forward service/svcfiaptechchallenge 5000:80
```
e acesse o serviço pela url [http://localhost:5000](http://localhost:5000)


## Opção Bonus: Inicie o ambiente com script run-kube

No diretório raiz do projeto, execute:
```
bash run-kube.sh
```
Esse comando usará o helm para iniciar o ambiente e após os pods da aplicação estarem prontos, realizara a conexão entre o serviço e a porta 5000 do seu localhost.

Acesso o serviço pela url [http://localhost:5000](http://localhost:5000)
