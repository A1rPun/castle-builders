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
    # test = 'while'
    # test = 'if_then'
    # test = 'switch'
    # test = 'if_then_else'
    test = 'if_else_if'
    lexer = ByteLexer()
    parser = ActionScriptParser()
    tokens = lexer.tokenize(test_data[test][1])
    # printTokens(tokens)
    parseTokens(tokens)
