# Para fazer a instalacao da biblioteca
## git clone https://github.com/adafruit/Adafruit_Python_DHT.git
## sudo apt-get update
## sudo apt-get install build-essential python-dev
## sudo python setup.py install

import Adafruit_DHT
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
# tipo do sensor
sensor = Adafruit_DHT.DHT11
# pino de conexao com o data do sensor
pino = 25

class IOs_test_dht11:

    def read_umidade(self):
        umidade, temperatura = Adafruit_DHT.read_retry(sensor, pino)
        return umidade
    def read_temperatura(self):
        umidade, temperatura = Adafruit_DHT.read_retry(sensor, pino)
        return temperatura
    def write(self, data):
        return True

#while True:
#    umidade, temperatura = Adafruit_DHT.read_retry(sensor, pino)
#    print(umidade)
#    print(temperatura)
#    print('Temperatura: (0:0.1f)  Umidade: (0:0.1f)').format(temperatura,umidade)
#    print("Temperatura = {0:0.1f}  Umidade = {1:0.1f}n").format(temperatura, umidade);
#    time.sleep(5)

