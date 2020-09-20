from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_conn = SQLAlchemy(app)

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

db_conn.create_all()