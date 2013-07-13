from pymongo import MongoClient


class MongoDB(object):

    def __init__(self, configuration):
        server, port = configuration.MONGODB_SERVER.split(':')
        port = int(port)
        self.client = MongoClient(server, port)

    def __getattribute__(self, attr):
        try:
            return super(MongoDB, self).__getattribute__(attr)
        except AttributeError:
            return getattr(self.client, attr)
