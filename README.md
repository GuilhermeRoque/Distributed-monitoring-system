# Projeto Estação Meteorologia

## Acessos:
- Login: admin
- Senha: admin

## Implementação:
* Este projeto foi implementado utilizando a Python3, Flask, Flask-SQLAlchemy, Adafruit, RPi.GPIO e Rabbitmq

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
## Comandos HTTP:
* curl --header "Content-Type: application/json" --request POST --data '{"id":"sensor1","max":10,"min":5,"type":"temp"}' localhost:5000/sensor
* curl --header "Content-Type: application/json" --request PUT --data '{"id":"sensor1","max":8,"min":5,"type":"temp"}' localhost:5000/sensor
* curl --header "Content-Type: application/json" --request GET --data '{"id":"sensor1"}' localhost:5000/sensor
* curl --header "Content-Type: application/json" --request DELETE --data '{"id":"sensor2"}' localhost:5000/sensor

## Documentação API-REST
[API-REST](API-REST.md)

## Página Projeto:

![Página do projeto](wikiPIJ2.pdf){width=65%}
