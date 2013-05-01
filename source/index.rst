.. Nerfed documentation master file, created by
   sphinx-quickstart on Thu May  2 00:41:47 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Nerfed's documentation!
==================================

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


Indeed there's classes, indeed it's more code, indeed you need to know object oriented programming. Also this code doesn't run you need a file ``index.html`` in a templates directory. You can find the demo application in the `forge <zhttps://github.com/amirouche/Nerfed/tree/master/demo>`_.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

