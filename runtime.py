import sys
from bytelexer import CCByteLexer
from actionscripttobytetranspiler import CCByteTranspiler
from bytetoactionscripttranspiler import CCActionScriptTranspiler


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
    lexed = lexer.tokenize(text)
    # for tok in lexed: print(tok)
    parser.parse(lexed)


def runFile(lexer, parser, fileName):
    with open(fileName) as f:
        content = f.readlines()
    for line in content:
        run(lexer, parser, line)


if __name__ == '__main__':
    lexer = CCByteLexer()
    # parser = CCByteTranspiler()
    parser = CCActionScriptTranspiler()
    print('---')
    print('Castle Crashers Byte Lexer & Parser v0.0.2')
    print('---')

    if len(sys.argv) > 1:
        runFile(lexer, parser, sys.argv[1])
    else:
        repl(lexer, parser)
