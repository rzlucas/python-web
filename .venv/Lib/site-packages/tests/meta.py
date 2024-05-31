
from unittest import TestCase

from mapping_shortcuts.meta import create_collection_meta


class MetaTestCase(TestCase):
    def test_ok(self):
        MetaClass, collection = create_collection_meta()

        class A(metaclass=MetaClass):
            ...

        class B(metaclass=MetaClass):
            ...

        self.assertEqual(len(collection), 2)

    def test_base(self):
        class SubClass(type):
            ...

        MetaClass, collection = create_collection_meta(base=SubClass)

        class A(metaclass=MetaClass):
            ...

        class B(metaclass=MetaClass):
            ...

        self.assertEqual(len(collection), 2)
        self.assertIsInstance(A, SubClass)
        self.assertIsInstance(B, SubClass)

    def test_getter(self):

        MetaClass, collection = create_collection_meta(
            getter=lambda cls: cls.__name__,
        )

        class A(metaclass=MetaClass):
            ...

        class B(metaclass=MetaClass):
            ...

        self.assertEqual(len(collection), 2)
        self.assertIn('A', collection)
        self.assertEqual(collection['A'], A)
        self.assertIn('B', collection)
        self.assertEqual(collection['B'], B)

    def test_duplicate_ok(self):

        non_unique_key = 'NotUniqueKey'

        MetaClass, collection = create_collection_meta(
            getter=lambda cls: non_unique_key,
            raise_on_duplicate=False,
        )

        class A(metaclass=MetaClass):
            ...

        class B(metaclass=MetaClass):
            ...

        self.assertEqual(len(collection), 1)
        self.assertIn(non_unique_key, collection)
        self.assertEqual(collection[non_unique_key], B)

    def test_duplicate_exception(self):

        non_unique_key = 'NotUniqueKey'

        MetaClass, collection = create_collection_meta(
            getter=lambda cls: non_unique_key,
            raise_on_duplicate=True,
        )

        class A(metaclass=MetaClass):
            ...

        try:
            class B(metaclass=MetaClass):
                ...
        except ValueError as ex:
            self.assertTrue(str(ex).startswith('Duplication for key'))
        else:
            self.assertTrue(False, 'expected exception here')

        self.assertEqual(len(collection), 1)
        self.assertIn(non_unique_key, collection)
        self.assertEqual(collection[non_unique_key], A)
