from sqlalchemy import engine_from_config
from sqlalchemy import MetaData
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import Integer as SQLAInteger
from sqlalchemy import Text as SQLAText

from properties import String as NerfedString
from properties import Integer as NerfedInteger


class SQLAlchemyDB(object):

    def __init__(self, configuration):
        self.engine = engine_from_config(dict(), **configuration)
        self.metadata = MetaData()

    def _column_type(self, property):
        if isinstance(property, NerfedString):
            return SQLAText
        if isinstance(property, NerfedInteger):
            return SQLAInteger

    def _columns(self, imperator):
        for name, property in imperator.properties.iteritems():
            yield Column(name, self._column_type(property), **property.options)

    def register(self, imperator):
        table = Table(
            imperator.name,
            self.metadata,
            *self._columns(imperator)
        )
        imperator._table = table
        return table

    def create_all(self):
        self.metadata.create_all(self.engine)
