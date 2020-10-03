import json
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import abort
from flask import request
from zmqRequest import ZMQRequest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_conn = SQLAlchemy(app)


class SensorDAO(db_conn.Model):
    __tablename__ = "Sensor"
    id = db_conn.Column(db_conn.String(40), primary_key=True)
    max = db_conn.Column(db_conn.Integer, index=True)
    min = db_conn.Column(db_conn.Integer, index=True)
    data_type = db_conn.Column(db_conn.String(40), index=True)
    type_specific = db_conn.Column(db_conn.String(40), index=True)
    model = db_conn.Column(db_conn.String(40), index=True)

    def __init__(self, sensor_json, type_specific=None):
        super().__init__(id=sensor_json['id'], max=sensor_json['max'], min=sensor_json['min'],
                         model=sensor_json['model'], data_type=sensor_json['data_type'],
                         type_specific=json.dumps(type_specific))
        self.max = sensor_json['max']
        self.min = sensor_json['min']
        self.data_type = sensor_json['data_type']
        self.model = sensor_json['model']
        self.type_specific = json.dumps(type_specific)

    def __repr__(self):
        return '<Sensor {}>'.format(self.id)

    def to_json(self):
        return {'id': self.id, 'max': self.max, 'min': self.min, 'model': self.model,
                'data_type': self.data_type, 'type_specific': json.loads(self.type_specific)}


@app.route('/sensor', methods=['GET', 'POST', 'DELETE', 'PUT'])
def sensor():
    if request.method == 'GET':
        sensorD = None
        try:
            sensor_json = request.json
            sensorD = SensorDAO.query.filter_by(id=sensor_json['id']).first()
        except:
            abort(400)
        if sensorD is None:
            abort(404)
        request_json = sensorD.to_json()
        request_json['cmd'] = request.method
        response = ZMQRequest.talk_zmq(request_json)
        if not response:
            return '', 500
        else:
            return jsonify(response)
    elif request.method == 'POST':
        response = False
        try:
            request_json = request.json
            request_json['cmd'] = request.method
            # {'sensor':1,'data_type: 'temperature', 'type_specific': {'pin': 1}}
            type_specific = request_json.pop('type_specific')
            sensorD = SensorDAO(request_json, type_specific)
            db_conn.session.add(sensorD)
            db_conn.session.commit()
            request_json = sensorD.to_json()
            request_json['cmd'] = request.method
            response = ZMQRequest.talk_zmq(request_json)
        except Exception as e:
            print(e)
            abort(400)
        if response['ack']:
            return '', 201
        else:
            return '', 202
    elif request.method == 'PUT':
        try:
            sensor_json = request.json
            SensorDAO.query.filter_by(id=sensor_json['id']).update(
                {'max': sensor_json['max'], 'min': sensor_json['min'],
                 'data_type': sensor_json['data_type']})
            db_conn.session.commit()
        except Exception as e:
            print(e)
            abort(400)
        return '', 200
    elif request.method == 'DELETE':
        try:
            sensor_json = request.json
            SensorDAO.query.filter_by(id=sensor_json['id']).delete()
            db_conn.session.commit()
        except Exception as e:
            print(e)
            abort(400)
        return '', 200
    else:
        abort(400)


if __name__ == '__main__':
    db_conn.create_all()
    app.debug = False
    app.run()
