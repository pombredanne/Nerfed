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
import re


def force_null(imperator, property, value):
    setattr(imperator, property.name, None)
    return True


class Property(object):
    """Base class data-descriptor for Imperator properties. Subclass
    it to implement a new property and making some actions default on it.
    """

    def __init__(self, *actions, **options):
        self.actions = list(actions)
        self.options = options
        self.name = None  # set by the metaclass
        if options.pop('null', False):
            self.actions.insert(0, force_null)
            options['nullable'] = True

    def __get__(self, object, cls=None):
        if not object:
            return self
        else:
            return object.data.get(self, None)

    def __set__(self, object, value):
        object.data[self] = value

    def __delete__(self, object):
        del object.data[self]

    def register(self, klass, name):
        klass.properties[name] = self
        self.name = name


def strip(imperator, property, value):
    if value:
        setattr(imperator, property.name, value.strip())
    return True


class String(Property):

    def __init__(self, *actions, **options):
        super(String, self).__init__(**options)
        actions = list(actions)
        actions.insert(0, strip)
        self.actions.extend(actions)


def convert_to_int(imperator, property, value):
    try:
        setattr(imperator, property.name, int(value))
    except:
        imperator.log_message(property, 'This is not an integer')


class Integer(Property):

    def __init__(self, *actions, **options):
        super(Integer, self).__init__(**options)
        actions = list(actions)
        if self.options.get('nullable', False):
            actions.insert(0, lambda imperator, property, value: True if not value else convert_to_int(imperator, property, value))
        else:
            actions.insert(0, convert_to_int)
        self.actions.extend(actions)


def convert_to_float(imperator, property, value):
    try:
        setattr(imperator, property.name, float(value))
    except:
        imperator.log_message(property, 'This is not a float')


class Float(Property):

    def __init__(self, *actions, **options):
        actions = list(actions)
        if options.get('nullable', False):
            actions.insert(0, lambda imperator, property, value: True if not value else convert_to_float(imperator, property, value))
        else:
            actions.insert(0, convert_to_float)
        super(Integer, self).__init__(*actions, **options)


regex = re.compile(
    r'^(?:http|ftp)s?://'  # secure http or ftp
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def validate_url(imperator, property, value):
    if not regex.search(value):
        imperator.log_message(property, 'This is not a valid URL')
        return False
    return True


class URL(String):

    def __init__(self, *actions, **options):
        actions = list(actions)
        actions.insert(0, validate_url)
        super(URL, self).__init__(*actions, **options)
