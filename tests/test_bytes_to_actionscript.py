import unittest
from ccbuilder.bytelexer import ByteLexer
from ccbuilder.actionscript_parser import ActionScriptParser


class ByteToActionScript(unittest.TestCase):

    def test_empty(self):
        text = "88 02 00 00 00 00"
        lexer = ByteLexer()
        parser = ActionScriptParser()
        parser.parse(lexer.tokenize(text))
        self.assertEqual(parser.code, "")

    # 96 07
    def test_push_number(self):
        text = "88 02 00 00 00 96 05 00 07 00 00 00 00 17 00"
        lexer = ByteLexer()
        parser = ActionScriptParser()
        parser.parse(lexer.tokenize(text))
        self.assertEqual(parser.code, "0;\n")

    # 48
    def test_lesser(self):
        text = "88 02 00 00 00 96 0a 00 07 01 00 00 00 07 02 00 00 00 48 17 00"
        lexer = ByteLexer()
        parser = ActionScriptParser()
        parser.parse(lexer.tokenize(text))
        self.assertEqual(parser.code, "1 < 2;\n")

    def test_greater_equals(self):
        text = "88 02 00 00 00 96 0a 00 07 01 00 00 00 07 02 00 00 00 48 12 17 00"
        lexer = ByteLexer()
        parser = ActionScriptParser()
        parser.parse(lexer.tokenize(text))
        self.assertEqual(parser.code, "1 >= 2;\n")

    # 49
    def test_equals(self):
        text = "88 02 00 00 00 96 0a 00 07 01 00 00 00 07 02 00 00 00 49 17 00"
        lexer = ByteLexer()
        parser = ActionScriptParser()
        parser.parse(lexer.tokenize(text))
        self.assertEqual(parser.code, "1 == 2;\n")

    def test_not_equals(self):
        text = "88 02 00 00 00 96 0a 00 07 01 00 00 00 07 02 00 00 00 49 12 17 00"
        lexer = ByteLexer()
        parser = ActionScriptParser()
        parser.parse(lexer.tokenize(text))
        self.assertEqual(parser.code, "1 != 2;\n")

    # 67
    def test_greater(self):
        text = "88 02 00 00 00 96 0a 00 07 01 00 00 00 07 02 00 00 00 67 17 00"
        lexer = ByteLexer()
        parser = ActionScriptParser()
        parser.parse(lexer.tokenize(text))
        self.assertEqual(parser.code, "1 > 2;\n")

    def test_lesser_equals(self):
        text = "88 02 00 00 00 96 0a 00 07 01 00 00 00 07 02 00 00 00 67 12 17 00"
        lexer = ByteLexer()
        parser = ActionScriptParser()
        parser.parse(lexer.tokenize(text))
        self.assertEqual(parser.code, "1 <= 2;\n")

    # def test_if_then_else(self):
    #     text = "88 02 00 00 00 9b 0f 00 69 66 54 68 65 6e 45 6c 73 65 00 00 00 22 00 96 02 00 05 01 12 9d 02 00 0e 00 96 05 00 07 01 00 00 00 17 99 02 00 09 00 96 05 00 07 02 00 00 00 17 00"
    #     lexer = ByteLexer()
    #     parser = ActionScriptParser()
    #     parser.parse(lexer.tokenize(text))
    #     self.assertEqual(parser.code, "function ifThenElse()\n{\n  if (true)\n  {\n    1;\n  }\n  else\n  {\n    2;\n  }\n}\n")

    # def test_ternary(self):
    #     text = "88 02 00 00 00 9b 10 00 73 68 6f 72 74 48 61 6e 64 49 66 00 00 00 21 00 96 02 00 05 01 12 9d 02 00 0d 00 96 05 00 07 01 00 00 00 99 02 00 08 00 96 05 00 07 02 00 00 00 17 00"
    #     lexer = ByteLexer()
    #     parser = ActionScriptParser()
    #     parser.parse(lexer.tokenize(text))
    #     self.assertEqual(parser.code, "function shortHandIf()\n{\n  true ? 1 : 2;\n}\n")

    def test_switch(self):
        text = "88 02 00 00 00 9b 0f 00 73 77 69 74 63 68 43 61 73 65 00 00 00 4e 00 96 02 00 05 01 87 01 00 00 96 02 00 05 01 66 9d 02 00 15 00 96 02 00 04 00 96 02 00 05 00 66 9d 02 00 13 00 99 02 00 1c 00 96 05 00 07 01 00 00 00 17 99 02 00 17 00 96 05 00 07 02 00 00 00 17 99 02 00 09 00 96 05 00 07 00 00 00 00 17 00"
        lexer = ByteLexer()
        parser = ActionScriptParser()
        parser.parse(lexer.tokenize(text))
        self.assertEqual(parser.code, "function switchCase()\n{\n  switch (true)\n  {\n    case true:\n      1;\n      break;\n    case false:\n      2;\n      break;\n    default:\n      0;\n  }\n}\n")

    # def test_while(self):
    #     text = "88 02 00 00 00 9b 0e 00 77 68 69 6c 65 54 72 75 65 00 00 00 19 00 96 02 00 05 01 12 9d 02 00 0e 00 96 05 00 07 01 00 00 00 17 99 02 00 e7 ff 00"
    #     lexer = ByteLexer()
    #     parser = ActionScriptParser()
    #     parser.parse(lexer.tokenize(text))
    #     self.assertEqual(parser.code, "function whileTrue()\n{\n  while (true)\n  {\n    1;\n  }\n}\n")

    # def test_fib(self):
    #     text = "88 06 00 01 00 66 69 62 00 8e 0e 00 66 69 62 00 01 00 02 2a 00 01 6e 00 58 00 96 02 00 04 01 96 05 00 07 02 00 00 00 48 12 9d 02 00 0a 00 96 02 00 04 01 99 02 00 39 00 96 02 00 04 01 96 05 00 07 01 00 00 00 0b 96 05 00 07 01 00 00 00 96 02 00 08 00 3d 96 02 00 04 01 96 05 00 07 02 00 00 00 0b 96 05 00 07 01 00 00 00 96 02 00 08 00 3d 47 3e 00"
    #     lexer = ByteLexer()
    #     parser = ActionScriptParser()
    #     parser.parse(lexer.tokenize(text))
    #     self.assertEqual(parser.code, "function fib(n)\n{\n  return n < 2 ? n : fib(n - 1) + fib(n - 2);\n}\n")


if __name__ == '__main__':
    unittest.main()
