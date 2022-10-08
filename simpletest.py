from ccbuilder.bytelexer import ByteLexer
from ccbuilder.actionscript_parser import ActionScriptParser
from ccbuilder.pcode_parser import PCodeParser
from tests.data import test_data


if __name__ == '__main__':
    lexer = ByteLexer()
    parser = ActionScriptParser()
    tokens = lexer.tokenize(test_data['if_then'][1])
    for tok in tokens:
        print(tok)
    parser.parse(tokens)
    print(parser.code)
