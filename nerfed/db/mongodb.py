from pymongo import MongoClient


class MongoDB(object):

    def __init__(self, configuration):
        self.client = MongoClient(*configuration.MONGODB_SERVER.split(':'))

    def __getattribute__(self, attr):
        try:
            return super(MongoDB, self).__getattribute__(attr)
        except AttributeError:
            return getattr(self.client, attr)y
