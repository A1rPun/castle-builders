from sly import Lexer
from util import splitBytes


class BaseLexer(Lexer):
    tokens = {}
    ignore = ' \t'

    def getNextBytes(self, num):
        length = num * 3
        nextBytes = self.text[self.index:self.index + length]
        value = splitBytes(nextBytes)
        self.index += length
        return value

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f'[{self.index}] Illegal character {t.value[0]!r}')
        self.index += 1
