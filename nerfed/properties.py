"""
.. warning:: you should read :mod:`nerfed.imperator` documentation before reading this.

This module defines the base class for :class:`nerfed.Imperator`'s
class properties and specific one. Those properties defines actions to be
executed on them and the imperator instance.

See :mod:`nerfed.imperator` for more information on them.

An imperator property is:

- a certain number of actions
- a certain number of options

And also:

- an class against which it's associated with a name
- an object against which a value is associtated

The a property constructor is ``Property(*actions, **options)``, nothing
is default, even if specialisation of this class can have mandatory values
and if used in a specific context, a Property might need a specific option.
"""


class Property(object):
    """Base class data-descriptor for Imperator properties. Subclass
    it to implement a new property and making some actions default on it.
    """

    def __init__(self, *actions, **options):
        self.actions = list(actions)
        self.options = options
        self.name = None  # set by the metaclass

    def __get__(self, object, cls=None):
        if not object:
            return self
        else:
            return object.data[self]

    def __set__(self, object, value):
        object.data[self] = value

    def __delete__(self, object):
        del object.data[self]

    def register(self, klass, name):
        klass.properties[name] = self
        self.name = name


class String(Property):
    pass


def convert_to_int(imperator, property, value):
    try:
        setattr(imperator, property.name, int(value))
    except:
        imperator.log_message(property, 'This is not an integer')


class Integer(Property):

    def __init__(self, *actions, **options):
        super(Integer, self).__init__(*actions, **options)
        if options.get('nullable', False):
            self.actions.insert(0, lambda imperator, property, value: True if not value else convert_to_int(x))
        else:
            self.actions.insert(0, convert_to_int)


class Float(Property):
    pass
