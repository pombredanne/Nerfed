from sqlalchemy import engine_from_config
from sqlalchemy import MetaData
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import Integer as SQLAInteger
from sqlalchemy import Text as SQLAText

from ..properties import String as NerfedString
from ..properties import Integer as NerfedInteger


class SQLAlchemyDB(object):

    NOT_COLUMN_PROPERTY = ['nullable', 'null']

    def __init__(self, configuration):
        self.engine = engine_from_config(dict(), **configuration)
        self.metadata = MetaData()
        self.metadata.bind = self.engine

    def _column_type(self, property):
        if isinstance(property, NerfedString):
            return SQLAText
        if isinstance(property, NerfedInteger):
            return SQLAInteger

    def _columns(self, imperator_class):
        for name, property in imperator_class.properties.iteritems():
            options = dict(filter(lambda x: x[0] not in SQLAlchemyDB.NOT_COLUMN_PROPERTY, property.options.iteritems()))
            yield Column(name, self._column_type(property), **options)

    def register(self, imperator_class):
        table = Table(
            imperator_class.__name__,
            self.metadata,
            *list(self._columns(imperator_class))
        )
        imperator_class._table = table
        return table

    def create_all(self):
        self.metadata.create_all(self.engine)

    def transaction(self):
        return self.engine.begin()

    def save(self, connection, imperator):
        if not imperator():
            raise Exception('Impossible to validate imperator object %s', imperator)
        connection.execute(imperator._table.insert(), **imperator.dict())
