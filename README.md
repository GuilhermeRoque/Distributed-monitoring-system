# Projeto Estação Meteorologia

## Passos para executar o projeto:
* É preciso executar o Rabbitmq Server, em um sistema Debina/Ubuntu siga o passos a seguir:
    * sudo apt install erlang
    * sudo apt install rabbitmq-server 
    * sudo rabbitmq-plugins enable rabbitmq_management
    * sudo systemctl start rabbitmq-server.service
* Na Raspberry Pi com o sistema Debin/Ubuntu, na pasta raiz do projeto, é preciso seguir os seguintes passos:
    * python3 -m venv venv
    * source venv/bin/activate
    * pip install -r requirements.txt

## Documentação API-REST
[API-REST](API-REST.md)

## Página Projeto:

[Página do projeto](https://wiki.sj.ifsc.edu.br/index.php/Guilherme_Anderson-PJI2-2020-1)
