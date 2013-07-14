from pymongo import MongoClient


class MongoDB(object):

    def __init__(self, configuration):
        server, port = configuration.MONGODB_SERVER.split(':')
        port = int(port)
        self.client = MongoClient(server, port)
        self.name = configuration.MONGODB_DATABASE_NAME

    def __getattribute__(self, attr):
        try:
            return super(MongoDB, self).__getattribute__(attr)
        except AttributeError:
            return getattr(getattr(self.client, self.name), attr)
