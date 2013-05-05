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

       def get(self, request):
           return self.app.render(request, 'index.html')


   class Demo(Application):

       def __init__(self):
           super(Demo, self).__init__(Settings())
           self.hello = self.register('localhost', Hello, '^/$')

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

``register(domain, sub_class, path, *args, **kwargs)`` returns a ``Sub`` instance that you can put in a dictionary or a store as a property of the ``Application`` object like it's done in the demo application above.

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

Like it's said above, an application is a tree, a tree of ``Sub`` object. As such ``Sub`` is node in the tree possibly a leaf node, in which case it doesn't have children. A ``Sub``'s child is another ``Sub```, it's a recursive datastructure, and that's what is called a tree.


``Sub(app, parent, path, *args, **kwargs)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Sub can be created using ``Application.register(domain, sub_class, path, *args, **kwargs)`` or using ```Sub.register(self, sub_class, path)``. You never use the constructor of a sub in principle. Still it's interesting to know what makes a ``Sub`` to use it with perfection. The constructor parameters are defined as follows:

- ``app``, is the application the Sub is taking part in
- ``parent``, is the parent node, most of the time it's another ```Sub``, but for ```Sub`` that forms the first level of ``Sub`` in the application in tree, it's the application object (again).
- ``path``, path is used to compute to which answer this ``Sub`` answers to, to know the path to this ``Sub`` you can use the internal property ``self._fullpath``.
- ``*args`` & ``**kwargs`` those are supplemental parameters that can be used to configure the object.

Like it's said above, you never use directly the constructore, but I hope it made things more clear.

``register(sub_class, path)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used to add a ``Sub`` to another ``Sub``, this is how you build the tree of ``Sub`` in principle you call this method in the constructor. Arguments are explained in the following:
 
- ```sub_class`` is a ``Sub`` class, how unexpected ?
- ``path`` is the *current* ``path`` a request should be resolved to when it has already consumed the elements of ``request.path`` from the ``Sub`` that are before in the branch.

Like it's said in the above ``path`` is what will be checked against what remains of ``request.path`` to match the request to this ``Sub`` as a *container* of ``Sub`` and *methods*. Indeed ``Sub`` is also a request handler, if you define one of the accepted methods: get, head, post, put; it will answer the request, only if it's a *full match* i.e. it consumed the remaining of ``request.path``.

.. note:: add a diagram.

``reverse(**kwargs)``
~~~~~~~~~~~~~~~~~~~~~

This method allows to reverse the current ``Sub`` to a ``path`` or full ``depending`` how the application is built. This is also the method used in templates to retrieve the url for ``Sub`` given some parameters ``kwargs```.


Conclusion
##########

The documentation needs more work but I hope you got the basic principles.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

