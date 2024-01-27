## Sistema de criação e gerenciamento de pedidos realizado para o Tech Challenge FIAP - SOAT - Grupo 31

Miro: https://miro.com/app/board/uXjVNe56-bI=/?share_link_id=839163216515<br>
Postman: https://documenter.getpostman.com/view/28694171/2s9YRCXrYf

# Arquitetura da Aplicação

## Arquitetura Kubernetes

![arquitetura-kubernetes](docs/arq-kubernetes-2.png)

## Arquitetura Código

![arquitetura-codigo](docs/arq-codigo-2.png)

1 - Usuário faz uma requisição: Um usuário interage com a aplicação fazendo uma requisição através da UI ou de um client API.

2 - Adapters / Entrypoints: A requisição atinge os entrypoints da API, que são os controladores (*_views.py), que interpretam os dados da requisição.

3 - Aplicação / DTOs: Os dados da requisição são então mapeados para Data Transfer Objects (DTOs), que são objetos simples usados para transferir dados entre processos. No caso, poderiam ser as classes em requests ou responses.
Aplicação / Caso de Uso: Os DTOs são passados para a lógica de negócios da aplicação, representada pelos casos de uso (*_usecase.py). Aqui, a requisição é processada de acordo com as regras de negócio.

4 - Domínio / Entidades: Os casos de uso operam em entidades do domínio (client.py, order.py, payment.py, product.py), que são as representações de negócio puras e contêm a lógica de negócios fundamental.

5 - Portas / Ports: Em seguida, os casos de uso interagem com os ports (*_port.py), que abstraem a comunicação com os adaptadores de infraestrutura externa.

6 - Infraestrutura / Repositórios: Por meio dos ports, os casos de uso interagem com os repositórios na camada de infraestrutura (*_repository.py). Estes repositórios abstraem a lógica de acessar o banco de dados e outras fontes de dados, como APIs externas ou serviços de armazenamento.

7 - Infraestrutura / Modelos de Banco de Dados: Os repositórios manipulam modelos de banco de dados (*_model.py) que são mapeamentos de entidades do domínio para tabelas de banco de dados ou esquemas de dados para armazenamento persistente.

Retorno da Requisição: Depois que a lógica de negócios é processada e os dados são persistidos ou atualizados conforme necessário, os resultados são então mapeados de volta para DTOs e enviados de volta pelos ports e adapters para a interface de usuário ou cliente


# Guia Rápido para Executar a Aplicação Flask
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
Primeiramente instale o `kubectl` para manipular o cluster kubernetes, de acordo com a [documentação oficial](https://kubernetes.io/docs/tasks/tools/#kubectl).

Em seguida, instale o Gerenciador de Pacote Helm da forma que desejar para o seu sistema operacional, conforme a [documentação](https://helm.sh/docs/intro/install/) 

Agora é necessário utilizar um cluster local para executar o ambiente. Existem diversos clusters que podem ser utilizados, porém recomendamos a utilização do minikube. Instale-o conforme a [documentação](https://minikube.sigs.k8s.io/docs/start/). Para a instalação do minikube é importante ter o [Docker](https://docs.docker.com/) instalado em sua máquina.
Após a instalação do minikube, inicie o cluster com:

```
minikube start
```

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
Certifique-se de ter instalado em sua máquina as mesmas dependências da Opção 2 (docker, kubectl, helm e minikube) e ter iniciado o cluster minikube.

No diretório raiz do projeto, execute:
```
bash run-kube.sh
```
Esse comando usará o helm para iniciar o ambiente e após os pods da aplicação estarem prontos, realizara a conexão entre o serviço e a porta 5000 do seu localhost.

Acesso o serviço pela url [http://localhost:5000](http://localhost:5000)
