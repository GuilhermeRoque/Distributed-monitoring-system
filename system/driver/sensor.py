from driver.sensorIO import SensorIO


class Sensor(SensorIO):
    def __init__(self, sensor_dict, **kwargs):
        self.max = sensor_dict['max']
        self.min = sensor_dict['min']
        self.model = sensor_dict['model']
        self.id = sensor_dict['id']

    def __repr__(self):
        return '<Sensor {}>'.format(self.id)
