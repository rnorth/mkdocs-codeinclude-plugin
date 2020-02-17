import unittest
from codeinclude.languages import get_lang_class


class MyTestCase(unittest.TestCase):
    def test_get_lang_class(self):
        self.assertEquals('java', get_lang_class('HelloWorld.java'))
        self.assertEquals('python', get_lang_class('HelloWorld.py'))
        self.assertEquals('csharp', get_lang_class('HelloWorld.cs'))
        self.assertEquals('rust', get_lang_class('HelloWorld.rs'))
        self.assertEquals('docker', get_lang_class('Dockerfile'))
        self.assertEquals('xml', get_lang_class('HelloWorld.xml'))
        self.assertEquals('toml', get_lang_class('HelloWorld.toml'))
        self.assertEquals('json', get_lang_class('HelloWorld.json'))


if __name__ == '__main__':
    unittest.main()
