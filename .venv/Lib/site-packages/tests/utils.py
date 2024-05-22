
from unittest import TestCase

from mapping_shortcuts.utils import parse_args, first


class FirstTestCase(TestCase):
    def test_ok(self):
        itr = (i for i in range(10) if not i % 3)
        self.assertEqual(first(itr), 0)
        self.assertEqual(first(itr), 3)
        self.assertEqual(first(itr), 6)
        self.assertEqual(first(itr), 9)
        self.assertEqual(first(itr), None)
        self.assertEqual(first(itr), None)


class ParseArgsTestCase(TestCase):
    def test_none(self):
        res = parse_args(['a', 'b', 'c'])
        self.assertEqual(res, {})

    def test_flags(self):
        res = parse_args(['-a', '-b', '-c'])
        self.assertEqual(res, {'-a': True, '-b': True, '-c': True})

    def test_multiflags(self):
        res = parse_args(['-abc'])
        self.assertEqual(res, {'-abc': True})

    def test_params(self):
        res = parse_args(['--a=123', '--long-name=somearg', '--empty='])
        self.assertEqual(res, {'--a': '123', '--long-name': 'somearg', '--empty': ''})
