import threading

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import abort
from flask import request
from dht11 import DHT11

sensors_list = []
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_conn = SQLAlchemy(app)


def get_sensor(id):
    for s in sensors_list:
        if id == id:
            return s


def build_sensor(sensorDAO):
    sensor_json = sensorDAO.to_json()
    if sensor_json['type'] == 'DHT11':
        sensors_list.append(DHT11(sensor_json, pin=4))


class SensorDAO(db_conn.Model):
    __tablename__ = "Sensor"
    id = db_conn.Column(db_conn.String(40), primary_key=True)
    max = db_conn.Column(db_conn.Integer, index=True)
    min = db_conn.Column(db_conn.Integer, index=True)
    type = db_conn.Column(db_conn.String(40), index=True)

    def __init__(self, sensor):
        super().__init__(id=sensor.id, max=sensor.max, min=sensor.min, type=sensor.type)
        self.max = sensor.max
        self.min = sensor.min
        self.type = sensor.type

    def __repr__(self):
        return '<Sensor {}>'.format(self.id)

    def to_json(self):
        return {'id': self.id, 'max': self.max, 'min': self.min, 'type': self.type}


@app.route('/sensor', methods=['GET', 'POST', 'DELETE', 'PUT'])
def sensor():
    if request.method == 'GET':
        sensor = None
        id = ''
        try:
            sensor_json = request.json
            id = sensor_json['id']
            sensor = get_sensor(id)
        except:
            abort(400)
        if sensor is None:
            abort(404)
        response = sensor.read()
        if not response:
            return '', 500
        else:
            resp_json = {'id': id, 'value': response}
            return jsonify(resp_json)
    elif request.method == 'POST':
        response = False
        try:
            sensor_json = request.json
            sensor = None
            if sensor_json['type'].upper() == 'DHT11':
                sensor = DHT11(sensor_json, pin=sensor_json['pin'])
            sensorDAO = SensorDAO(sensor)
            db_conn.session.add(sensorDAO)
            db_conn.session.commit()
            response = sensor.activate()
            sensors_list.append(sensor)
        except:
            abort(400)
        if response:
            return '', 201
        else:
            return '', 202
    elif request.method == 'PUT':
        sensor = None
        try:
            sensor_json = request.json
            sensor = get_sensor(sensor_json['id'])
            sensor.max = sensor_json['max']
            sensor.min = sensor_json['min']
            SensorDAO.query.filter_by(id=sensor_json['id']).update(
                {'max': sensor_json['max'], 'min': sensor_json['min']})
            db_conn.session.commit()
        except:
            abort(400)
        if sensor is None:
            abort(404)
        else:
            return '', 200
    elif request.method == 'DELETE':
        sensor = None
        try:
            sensor_json = request.json
            sensor = get_sensor(sensor_json['id'])
            sensors_list.remove(sensor)
            SensorDAO.query.filter_by(id=sensor_json['id']).delete()
            db_conn.session.commit()
        except:
            abort(400)
        if sensor is None:
            abort(404)
        else:
            return '', 200
    else:
        abort(400)


db_conn.create_all()
sensors = SensorDAO.query.all()
for sensor in sensors:
    build_sensor(sensor)
app.debug = False
app.use_reloader = False
web_t = threading.Thread(target=app.run)
web_t.start()
