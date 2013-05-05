.. Nerfed documentation master file, created by
   sphinx-quickstart on Thu May  2 00:41:47 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Nerfed's documentation!
##################################

Nerfed is Object Oriented web framework. Here is a «Héllo world» application:

.. code-block:: python

   import os

   from nerfed import Application
   from nerfed import Sub


   class Settings(object):

       root = os.path.dirname(__file__)

       @property
       def templates_path(self):
           return os.path.join(self.root, 'templates')


   class Hello(Sub):

       def __init__(self, app, path, instance_name=None):
           super(Hello, self).__init__(app, path)

       def get(self, request):
           return self.app.render(request, 'index.html')


   class Demo(Application):

       def __init__(self):
           super(Demo, self).__init__(Settings())
           self.register('localhost', Hello, '^/$')

   demo = Demo()


Indeed there's classes, indeed it's more code, indeed you need to know object oriented programming. Also this code doesn't run you need a file ``index.html`` in a templates directory. You can find the demo application in the `forge <https://github.com/amirouche/Nerfed/tree/master/demo>`_.

Bases
=====

You know already about three objects in *Nerfed*, ``Settings``, ``Sub`` and ``Application``. At least you read about them. Let's digg further what they do and how they interact, also I will explain the public methods aka. the methods that you will certainly need to use.

``settings``
------------

This is the simplest, since it's a *Plain Old Python Object*. You will pass an instance of it as the first argument and only parameter of ``Application`` object, the main object of your project. Depending on the the usage you do of the framework some properties must be defined, this is documented in the relevant classes and methods.

.. note:: In the above example, ``settings`` is an instance of a class, but it can be any Python object, even a module like in other popular frameworks.

Application
-----------

.. image:: http://farm4.staticflickr.com/3132/3249616410_c753a40a40_b.jpg
   :align: center

It's the main object in your project.


``Application(settings=None)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The constructor takes as only parameter a setting object.

``Application.register(domain, sub_class, path, *args, **kwargs)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Application`` objects are the root of a tree of ``Sub`` objects. To add a ``Sub`` to an application use the ``register(domain, sub_class, path, *args, **kwargs)`` method:

- ``domain`` must be a regex rule that will be compiled to match the request domain against. It can be as simple as a string like ``r'www\.hypermove\.net'`` or contain a named group ``r'(?P<lang>\w{2})\.hypermove.net``. The dictionary of matched **named groups** will be available on the request object as ``request.domain_match``. **Becarful** it **doesn't accept** unnamed groups, so every group **must** be named. Also **don't forget** that this argument is compiled by the ``re`` module to a regular expression which means that ``.`` isn't the dot character but the *regex match anything* operator.
- ``sub_class`` is a ``Sub`` class, the third and last class that we will be interested in this part of the documentation
- ``path`` must be a regex rule that will be compiled to match the request path against. Something like ``r'/rubrique`` or a bit more complex ``r'/article/(?P<id>\d+)'``. Just like ``domain``, only named groups are accepted, matched groups can later be retrieved in ``request.path_match``. For a given path in the ``Sub`` tree, group names must unique or they will be overwritten.
- ``*args``, ``**kwargs`` are passed to ``sub_class`` constructor so that you can configure a ``Sub`` without having to inherit it or create a property in ``app.settings``, neat isn't it?

The ``Application`` object of a tree, is always accessible in its children as the ``app`` property or ``self.app`` in ``Sub`` perspective. Because it defines methods that can be used application wide and in particular it must also reference databases objects, template engine and anything *generic* that can be used application wide. The following paragraph describe such a generic method.

.. warning:: Application class **must not** have business related methods, there is another object for this kind of matters that will be described later.

.. note:: This relatively controlversial, but I think that thread locals are a bad thing. It's complex concept and also it's not needed to understand it to make web framework, so why not just avoid them if one can? Moreover, thread locals need to be imported in the case of the ``request`` or ``db``, it makes for two pervasive imports. Also, thread locals are inherited from PHP thinking pattern. Instead the request object is parameter and databases objects are ``Application`` object properties.

``Application.render(request, path, **context)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nerfed is bundled with Jinja2 rendering engine, it's accessible as ``render(request, path, **context)`` method from ``Application`` objects, the parameter can be explained as follow:

- ``request`` is a Webob request object that is an argument of ``Sub`` methods and which will be included in the template
- ``path`` is the path to the file that will be rendered relative to ``app.settings.templates_path``, *so* if you want to use ``render``, your application settings must at least defined ``templates_path`` property.
- ``**context`` are keyword arguments that will be used to populate the template context.

**Also** ``app.settings`` is included in the templates context. So in a template context you will find:

- Everything you pass as keyword arguments to ``render`` that is not ``path``
- Current ``request`` object
- ``app.settings`` current application's settings

If ``self`` is a ``Sub`` the following call ``self.app.render(request, 'profile/profile.html', username=username, bio=bio)`` can be valid.

``Sub``
-------

FIXME


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

