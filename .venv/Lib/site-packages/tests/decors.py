
from unittest import TestCase

from mapping_shortcuts.decors import create_collector
from mapping_shortcuts.decors import create_class_collector


class DecorTestCase(TestCase):

    def test_ok(self):
        decor, collection = create_collector()

        @decor('1')
        def f1():
            ...

        @decor('2')
        def f2():
            ...

        self.assertEqual(len(collection), 2)
        self.assertIn('1', collection)
        self.assertIn('2', collection)
        self.assertIs(collection['1'], f1)
        self.assertIs(collection['2'], f2)

    def test_duplicate_raise(self):
        decor, collection = create_collector()

        @decor('1')
        def f1():
            ...

        try:
            @decor('1')
            def f2():
                ...
        except ValueError as ex:
            self.assertTrue(str(ex).startswith('Duplication for key'))
        else:
            self.assertTrue(False, 'expected exception here')

        self.assertEqual(len(collection), 1)
        self.assertIn('1', collection)
        self.assertIs(collection['1'], f1)

    def test_duplicate_ok(self):
        decor, collection = create_collector(
            raise_on_duplicate=False,
        )

        @decor('1')
        def f1():
            ...

        @decor('1')
        def f2():
            ...

        self.assertEqual(len(collection), 1)
        self.assertIn('1', collection)
        self.assertIs(collection['1'], f2)


class DecorClassTestCase(TestCase):
    def test_simple(self):
        decor, collection = create_class_collector()

        @decor
        class A:
            ...

        @decor
        class B:
            ...

        self.assertEqual(len(collection), 2)
        self.assertIn('A', collection)
        self.assertIs(collection['A'], A)
        self.assertIn('B', collection)
        self.assertIs(collection['B'], B)

    def test_key(self):
        decor, collection = create_class_collector()

        @decor('1')
        class A:
            ...

        @decor('2')
        class B:
            ...

        self.assertEqual(len(collection), 2)
        self.assertIn('1', collection)
        self.assertIs(collection['1'], A)
        self.assertIn('2', collection)
        self.assertIs(collection['2'], B)

    def test_duplicate_raise(self):
        decor, collection = create_class_collector(raise_on_duplicate=True)

        @decor
        class A:
            ...

        try:
            @decor
            class A:
                ...
        except ValueError as ex:
            self.assertTrue(str(ex).startswith('Duplication for key'))

        else:
            self.assertTrue(False, 'expected exception here')

        self.assertEqual(len(collection), 1)
        self.assertIn('A', collection)
        self.assertIs(collection['A'], A)

    def test_duplicate_ok(self):
        decor, collection = create_class_collector(raise_on_duplicate=False)

        @decor
        class A:
            ...

        @decor
        class A:
            ...

        self.assertEqual(len(collection), 1)
        self.assertIn('A', collection)
        self.assertIs(collection['A'], A)

    def test_key_getter(self):
        decor, collection = create_class_collector(key_getter=lambda x: x.x)

        @decor
        class A:
            x = 123

        @decor
        class B:
            x = 456

        self.assertEqual(len(collection), 2)
        self.assertIn(123, collection)
        self.assertIs(collection[123], A)
        self.assertIn(456, collection)
        self.assertIs(collection[456], B)
