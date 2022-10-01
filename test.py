import sys
from lexer import CCByteLexer
from parser import CCByteParser

def repl(lexer, parser):
    print('Type "exit" to quit the REPL')

    linecount = 0
    while True:
        try:
            text = input(f'λ({linecount}) ⇒ ')
        except EOFError:
            break
        if text:
            if text == 'exit':
                break
            run(lexer, parser, text)
            linecount = linecount + 1


def run(lexer, parser, text):
    parser.parse(lexer.tokenize(text))
    # for tok in lexer.tokenize(text):
    #     print(tok)


def runFile(lexer, parser, fileName):
    with open(fileName) as f:
        content = f.readlines()
    for line in content:
        run(lexer, parser, line)


if __name__ == '__main__':
    lexer = CCByteLexer()
    parser = CCByteParser()
    print('---')
    print('Castle Crashers Byte Lexer & Parser v0.0.1')
    print('---')

    if len(sys.argv) > 1:
        runFile(lexer, parser, sys.argv[1])
    else:
        repl(lexer)
