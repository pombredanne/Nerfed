# -*- encoding: utf-8 -*-
"""This module defines the ``Imperator`` functor class which is central in
everything related to data and its processing. ``Imperator`` classes defines a
so-called declarative syntax, usally used in data mappers classes, to defined
specific behaviors executed at a specific time when an ``Imperator`` object is
called. Imperators are meant to be used in different context and different
application aka. Imperator should be able to move from application to
application while keeping the same semantic.

An ``Imperator`` can be seen both as a replacement for ``Form`` and ``Model``
classes that can be found in some frameworks. The :class:`nerfed.Form` class
only deals with rendering. As such you can both use it for:

- Wrapping data in a class and add to data specific behaviors in an
  object-oriented way.
- As a consequence of the above, it can be used for data validation, and
  the framework offers some machinery to help.

.. note:: You might wonder why merge both ``Model`` and ``Form`` class, it is
   so because both them do similar thing, they wrap data and process it. So why
   not a have a base class for both cases ?

Getting started
===============

Let's start with a simple declarative class of a ``Person` that inherits
``Imperator``:

.. code-block:: python

   from nerfed import Imperator
   from nerfed import Integer
   from nerfed import String


   class Person(Imperator):
       name = String()
       age = Integer()

This defines a ``Person`` with two properties ``name`` as ``String`` and
``status`` as an ``Integer``. It is not very usefull as such but you can
already instantiate it with the default constructor ``Imperator(data, app)``:

.. code-block:: python

   person = Person(dict(name='amirouche', age=28))

``data`` must be a dictionary and ``app`` should be a handle that allows to do
external calls, execute actions on the outside world, it will be shown later
how it can be useful.

The only method an ``Imperator`` implements except the constructor is
``__call__``, so you can call the ``Imperator`` instance:

.. code-block:: python

   ok = person()

It returns a boolean status. This is the result of calling properties actions
and objects actions. Properties actions are described in the
:mod:`nerfed.properties`. Objects actions are defined in ``actions`` class
attribute that allows to execute after every properties actions. You can
for instance say héllo using the following code:

.. code-block::

   def say_hello(person, ok):
       print('%s is %s year old' % (person.name, person.age))
       return True

   from nerfed import Imperator
   from nerfed import Integer
   from nerfed import String


   class Person(Imperator):
       name = String()
       age = Integer()

       actions = [say_hello]

Or it can be defined as a method of ``Person``:

.. code-block::

   from nerfed import Imperator
   from nerfed import Integer
   from nerfed import String


   class Person(Imperator):
       name = String()
       age = Integer()

       def say_hello(self, ok):
           print '%s is %s year old' % (person.name, person.age)
           return True

       actions = [say_hello]

    person = Person(dict(name='amirouche', age=28))
    person()

An imperator action takes the imperator instance as first argument and
the current status. As such it has access to all the data inside ``Person``,
you can store new values in data, or as properties or anything. The return
value of all actions will be used to compute the call status, if any
returns ``False`` the status will ``False``.

That said the above code is not nerfed. Indeed, ``print`` is global, and global
calls should be avoided because it means the imperator becomes dependant
of some functions being present in the local context which might not be
easy to override in another application. Instead you can pass as app an object
that defines the feature you need for instance this code is nerfed:

.. code-block::

   from nerfed import Imperator
   from nerfed import Integer
   from nerfed import String


   class CLIApp(object):

       def print(self, message):
           print(message)


   class Person(Imperator):
       name = String()
       age = Integer()

       def say_hello(self, ok):
           self.app.print('%s is %s year old' % (person.name, person.age))
           return True

       actions = [say_hello]

    person = Person(dict(name='amirouche', age=28), CLIApp())
    person()

This way you can reuse ``Person`` in another app easily by providing
the implementation of the application dependant in a class, isn't this neat ?

.. note:: This kind of overkill for most uses, if you don't need it,
   don't use it.

.. note:: This is also a way to avoid thread locals, a handle to the current
   app is passed from context to context in the life time of a request so that
   you never have to deal with what thread locals are (plus thread locals
   are not Pythonic (!))

You can now read the :mod:`nerfed.properties` documentation.
"""
from properties import Property


class PropertyBasedClass(type):
    """Metaclass for the so called declarative syntax"""

    def __init__(klass, classname, bases, class_dict):
        klass.properties = dict()

        # register properties defined in this class
        for name, property in class_dict.iteritems():
            if isinstance(property, Property):
                property.register(klass, name)


class Imperator(object):
    """Imperator holds data and can process them with actions.
    It's configured with ``Property`` as class properties aka.
    declarative syntax.

    Actions can be registered against properties and also
    object wide actions registererd in ``actions`` property.
    """

    __metaclass__ = PropertyBasedClass
    actions = tuple()

    def __init__(self, data=None):
        self.data = dict()
        data = data if data else dict()
        for name, value in data.iteritems():
            try:
                property = self.properties[name]
            except KeyError:
                continue
            else:
                self.data[property] = value

    def __call__(self, app):
        """Executes actions on each properties and object wide return False
        if one of the action do so"""
        all_ok = True
        for property in self.properties.values():
            value = self.data.get(property, None)
            for action in property.actions:
                ok = action(self, property, value)
                all_ok = False if not ok else all_ok
        for action in self.actions:
            ok = action(app, self, all_ok)
            all_ok = False if not ok else all_ok
        return all_ok

    def log_message(self, property, message):
        """Log message for a specific property"""
        if not hasattr(self, 'messages'):
            self.messages = dict()
        if property.name not in self.messages:
            self.messages[property.name] = list()
        self.messages[property.name].append(message)

    def dict(self):
        return dict(map(lambda item: (item[0].name, item[1]), self.data.iteritems()))
