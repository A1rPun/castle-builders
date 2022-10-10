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
    test = 'fib'
    lexer = ByteLexer()
    parser = ActionScriptParser(True)
    run(test_data[test][1])
    # runFile(test)
