import argparse
from ccbuilder.bytelexer import ByteLexer
from ccbuilder.actionscript_parser import ActionScriptParser
from ccbuilder.pcode_parser import PCodeParser


def repl():
    print('Type "exit" to quit the REPL')

    linecount = 0
    while True:
        try:
            text = input(f'CCBuilder({linecount}) ⇒ ')
        except EOFError:
            break
        if text:
            if text == 'exit':
                break
            run(text)
            linecount = linecount + 1


def run(text):
    parser.parse(lexer.tokenize(text))
    print(parser.getCode())


def runFile(fileName):
    with open(fileName) as f:
        content = f.readlines()
    for line in content:
        run(line)


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument("filename", nargs='?')
    argParser.add_argument("-p", "--pcode", action=argparse.BooleanOptionalAction)
    args = argParser.parse_args()
    lexer = ByteLexer()
    parser = PCodeParser() if args.pcode else ActionScriptParser()
    runFile(args.filename) if args.filename else repl()
