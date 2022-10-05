import argparse

from ccbuilder.bytelexer import ByteLexer
from ccbuilder.actionscript_parser import ActionScriptParser
from ccbuilder.pcode_parser import PCodeParser


def repl(lexer, parser):
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
            run(lexer, parser, text)
            linecount = linecount + 1


def run(lexer, parser, text):
    parser.parse(lexer.tokenize(text))
    print(parser.code)


def runFile(lexer, parser, fileName):
    with open(fileName) as f:
        content = f.readlines()
    for line in content:
        run(lexer, parser, line)


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument("filename", nargs='?')
    argParser.add_argument("-p", "--pcode", action=argparse.BooleanOptionalAction)
    args = argParser.parse_args()
    print('Castle Crashers Byte Lexer & Parser v0.0.4')
    print('---')
    lexer = ByteLexer()

    if args.pcode:
        parser = PCodeParser()
    else:
        parser = ActionScriptParser()

    if args.filename:
        runFile(lexer, parser, args.filename)
    else:
        repl(lexer, parser)
