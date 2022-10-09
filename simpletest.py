from ccbuilder.bytelexer import ByteLexer
from ccbuilder.actionscript_parser import ActionScriptParser
from ccbuilder.pcode_parser import PCodeParser
from tests.data import test_data


def printTokens(tokens):
    for tok in tokens:
        print(tok)

def parseTokens(tokens):
    parser.parse(tokens)
    print(parser.code)

if __name__ == '__main__':
    # test = 'empty'
    # test = 'push_number'
    # test = 'equals'
    # test = 'not_equals'
    # test = 'lesser'
    # test = 'lesser_equals'
    # test = 'greater'
    # test = 'greater_equals'
    test = 'if_then'
    # test = 'if_then_else'
    # test = 'if_else_if' # FIX
    # test = 'ternary' # FIX
    # test = 'while'
    # test = 'do_while' # FIX
    # test = 'switch'
    # test = 'this'
    # test = 'root' # FIX
    # test = 'this_root'
    # test = 'values' # FIX string
    # test = 'double_assign' # FIX
    # test = 'fib' # FIX
    lexer = ByteLexer()
    parser = ActionScriptParser()
    tokens = lexer.tokenize(test_data[test][1])
    # printTokens(tokens)
    parseTokens(tokens)
