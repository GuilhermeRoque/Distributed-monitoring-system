import zmq

context = zmq.Context()
HOST = "localhost"
PORT = "50007"
path = "tcp://" + HOST + ":" + PORT
socket = context.socket(zmq.REQ)


class ZMQRequest:

    @staticmethod
    def talk_zmq(json_msg):
        socket.connect(path)
        socket.send_json(json_msg)
        resp_json = socket.recv_json()
        return resp_json