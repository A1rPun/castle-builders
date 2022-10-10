from ccbuilder.bytelexer import ByteLexer
from ccbuilder.actionscript_parser import ActionScriptParser
from tests.data import test_data


def printTokens(tokens):
    for tok in tokens:
        print(tok)

def parseTokens(tokens):
    parser.parse(tokens)
    print(parser.getCode())

def run(text):
    tokens = lexer.tokenize(text)
    # printTokens(tokens)
    parseTokens(tokens)

def runFile(fileName):
    with open(fileName) as f:
        content = f.readlines()
    for line in content:
        run(line)

if __name__ == '__main__':
    test = 'if_then'
    # test = 'if_then_else'
    # test = 'if_else_if'
    # test = 'ternary'
    # test = 'while'
    # test = 'do_while'
    # test = 'switch'
    # test = 'values'
    # test = 'double_assign'
    # test = 'fib'
    lexer = ByteLexer()
    # parser = ActionScriptParser(True)
    parser = ActionScriptParser()
    # run(test_data[test][1])
    runFile(test)
