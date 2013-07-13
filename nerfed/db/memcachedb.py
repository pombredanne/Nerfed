from memcache import Client


class MemcacheDB(Client):

    def __init__(self, configuration):
        super(MemcacheDB, self).__init__(configuration.MEMCACHED_SERVERS)
