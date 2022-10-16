import unittest
from ccbuilder.byte_lexer import ByteLexer
from ccbuilder.actionscript_parser import ActionScriptParser
from tests.data import test_data


class ByteToActionScript(unittest.TestCase):

    def self_test(self, actionScript, byteString):
        lexer = ByteLexer()
        parser = ActionScriptParser()
        parser.parse(lexer.tokenize(byteString))
        self.assertEqual(parser.getCode(), actionScript)

    def test_empty(self):
        actionScript, byteString = test_data['empty']
        self.self_test(actionScript, byteString)

    def test_push_number(self):
        actionScript, byteString = test_data['push_number']
        self.self_test(actionScript, byteString)

    def test_do_while(self):
        actionScript, byteString = test_data['do_while']
        self.self_test(actionScript, byteString)

    def test_equals(self):
        actionScript, byteString = test_data['equals']
        self.self_test(actionScript, byteString)

    def test_not_equals(self):
        actionScript, byteString = test_data['not_equals']
        self.self_test(actionScript, byteString)

    def test_greater(self):
        actionScript, byteString = test_data['greater']
        self.self_test(actionScript, byteString)

    def test_greater_equals(self):
        actionScript, byteString = test_data['greater_equals']
        self.self_test(actionScript, byteString)

    def test_if_then(self):
        actionScript, byteString = test_data['if_then']
        self.self_test(actionScript, byteString)

    def test_if_then_else(self):
        actionScript, byteString = test_data['if_then_else']
        self.self_test(actionScript, byteString)

    def test_if_else_if(self):
        actionScript, byteString = test_data['if_else_if']
        self.self_test(actionScript, byteString)

    def test_lesser(self):
        actionScript, byteString = test_data['lesser']
        self.self_test(actionScript, byteString)

    def test_lesser_equals(self):
        actionScript, byteString = test_data['lesser_equals']
        self.self_test(actionScript, byteString)

    def test_root(self):
        actionScript, byteString = test_data['root']
        self.self_test(actionScript, byteString)

    def test_switch(self):
        actionScript, byteString = test_data['switch']
        self.self_test(actionScript, byteString)

    def test_ternary(self):
        actionScript, byteString = test_data['ternary']
        self.self_test(actionScript, byteString)

    def test_this(self):
        actionScript, byteString = test_data['this']
        self.self_test(actionScript, byteString)

    def test_this_root(self):
        actionScript, byteString = test_data['this_root']
        self.self_test(actionScript, byteString)

    # def test_values(self):
    #     actionScript, byteString = test_data['values']
    #     self.self_test(actionScript, byteString)

    def test_while(self):
        actionScript, byteString = test_data['while']
        self.self_test(actionScript, byteString)

    # def test_double_assign(self):
    #     actionScript, byteString = test_data['double_assign']
    #     self.self_test(actionScript, byteString)

    def test_fib(self):
        actionScript, byteString = test_data['fib']
        self.self_test(actionScript, byteString)


if __name__ == '__main__':
    unittest.main()
