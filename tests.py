from unittest import TestCase

from nerfed import String
from nerfed import Integer
from nerfed import Property
from nerfed import Imperator


def action(imperator, field, value):
    setattr(imperator, field.name, True)
    print imperator.property, field.name
    imperator.flag2 = True
    return True


class Simple(Imperator):
    property = Property(action)

    def flag(self, ok):
        self.flag = True
        return True

    actions = [flag]


class TestImperator(TestCase):

    def test_create_class(self):
        simple = Simple(dict(property=False))
        self.assertTrue(simple())
        self.assertTrue(simple.property)
        self.assertTrue(simple.flag)
