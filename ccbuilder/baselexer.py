from sly import Lexer
from ccbuilder.util import splitBytes


class BaseLexer(Lexer):
    tokens = {}
    ignore = ' \t'

    def getNextBytes(self, num):
        length = num * 3
        nextBytes = self.text[self.index:self.index + length]
        value = splitBytes(nextBytes)
        self.index += length
        return value

    def getNextBytesFind(self, byte = " 00"):
        newIndex = self.text.index(byte, self.index + 1)
        nextBytes = self.text[self.index:newIndex]
        value = splitBytes(nextBytes)
        self.index += newIndex - self.index + 3
        return value

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f'[{self.index}] Illegal character {t.value[0]!r}')
        self.index += 1
