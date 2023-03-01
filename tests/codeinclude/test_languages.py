import unittest
from codeinclude.languages import get_lang_class


class MyTestCase(unittest.TestCase):
    def test_get_lang_class(self):
        self.assertEqual("java", get_lang_class("HelloWorld.java"))
        self.assertEqual("python", get_lang_class("HelloWorld.py"))
        self.assertEqual("csharp", get_lang_class("HelloWorld.cs"))
        self.assertEqual("rust", get_lang_class("HelloWorld.rs"))
        self.assertEqual("docker", get_lang_class("Dockerfile"))
        self.assertEqual("xml", get_lang_class("HelloWorld.xml"))
        self.assertEqual("toml", get_lang_class("HelloWorld.toml"))
        self.assertEqual("json", get_lang_class("HelloWorld.json"))


if __name__ == "__main__":
    unittest.main()
