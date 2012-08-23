import unittest
import confit
import argparse
import optparse

class ArgparseTest(unittest.TestCase):
    def setUp(self):
        self.config = confit.RootView([])
        self.parser = argparse.ArgumentParser()

    def _parse(self, args):
        args = self.parser.parse_args(args.split())
        self.config.add_args(args)

    def test_text_argument_parsed(self):
        self.parser.add_argument('--foo', metavar='BAR')
        self._parse('--foo bar')
        self.assertEqual(self.config['foo'].get(), 'bar')

    def test_boolean_argument_parsed(self):
        self.parser.add_argument('--foo', action='store_true')
        self._parse('--foo')
        self.assertEqual(self.config['foo'].get(), True)

    def test_missing_optional_argument_not_included(self):
        self.parser.add_argument('--foo', metavar='BAR')
        self._parse('')
        with self.assertRaises(confit.NotFoundError):
            self.config['foo'].get()

    def test_argument_overrides_default(self):
        self.config.add({'foo': 'baz'})

        self.parser.add_argument('--foo', metavar='BAR')
        self._parse('--foo bar')
        self.assertEqual(self.config['foo'].get(), 'bar')

class OptparseTest(unittest.TestCase):
    def setUp(self):
        self.config = confit.RootView([])
        self.parser = optparse.OptionParser()

    def _parse(self, args):
        options, _ = self.parser.parse_args(args.split())
        self.config.add_args(options)

    def test_text_argument_parsed(self):
        self.parser.add_option('--foo', metavar='BAR')
        self._parse('--foo bar')
        self.assertEqual(self.config['foo'].get(), 'bar')

    def test_boolean_argument_parsed(self):
        self.parser.add_option('--foo', action='store_true')
        self._parse('--foo')
        self.assertEqual(self.config['foo'].get(), True)

    def test_missing_optional_argument_not_included(self):
        self.parser.add_option('--foo', metavar='BAR')
        self._parse('')
        with self.assertRaises(confit.NotFoundError):
            self.config['foo'].get()

    def test_argument_overrides_default(self):
        self.config.add({'foo': 'baz'})

        self.parser.add_option('--foo', metavar='BAR')
        self._parse('--foo bar')
        self.assertEqual(self.config['foo'].get(), 'bar')
