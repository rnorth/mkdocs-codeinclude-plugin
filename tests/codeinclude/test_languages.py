import unittest
from codeinclude.languages import get_extension, get_lang_class


class MyTestCase(unittest.TestCase):
    def test_get_extension_simple_name(self):
        filename = 'HelloWorld.java'
        expected = 'java'
        self.assertEqual(get_extension(filename), expected)

    def test_get_extension_relative_name(self):
        filename = './HelloWorld.java'
        expected = 'java'
        self.assertEqual(get_extension(filename), expected)

    def test_get_extension_dots_in_name(self):
        filename = 'HelloWorld.template.java'
        expected = 'java'
        self.assertEqual(get_extension(filename), expected)

    def test_get_lang_class(self):
        self.assertEquals('java', get_lang_class('HelloWorld.java'))
        self.assertEquals('xml', get_lang_class('HelloWorld.xml'))
        self.assertEquals('json', get_lang_class('HelloWorld.json'))
        self.assertEquals('rs', get_lang_class('HelloWorld.rs'))


if __name__ == '__main__':
    unittest.main()
