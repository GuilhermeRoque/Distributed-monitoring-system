from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import abort
from flask import request
from sensor import Sensor

sensors_list = []
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_conn = SQLAlchemy(app)


def get_sensor(id):
    for s in sensors_list:
        if id == s.id:
            return s


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
            sensor = Sensor(sensor_json)
            sensorDAO = SensorDAO(sensor)
            db_conn.session.add(sensorDAO)
            db_conn.session.commit()
            response = sensor.active()
            sensors_list.append(sensor)
        except:
            abort(400)
        if response:
            return '', 201
        else:
            return '', 202
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        pass


db_conn.create_all()
sensors = SensorDAO.query.all()
for sensor in sensors:
    sensors_list.append(Sensor(sensor.to_json()))
app.debug=False
app.use_reloader=False