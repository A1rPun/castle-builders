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

    def getNextBytesFind(self, end = None, byte = " 00"):
        newIndex = self.text.index(byte, self.index + 1, (end if end is None else self.index + end * 3))
        # newIndex = self.text.index(byte, self.index + 1)
        nextBytes = self.text[self.index:newIndex]
        value = splitBytes(nextBytes)
        self.index += newIndex - self.index + 3
        return value

    def hasNextByte(self, end = None, byte = " 00"):
        try:
            newIndex = self.text.index(byte, self.index + 1, (end if end is None else self.index + end * 3))
        except ValueError:
            return -1
        except Exception:
            raise
        return newIndex

    def findBytes(self, start = None, end = None, byte = " 00"):
        try:
            mulStart = start * 3
            mulEnd = end * 3
            byteString = self.text[self.index + mulStart:self.index + mulStart + mulEnd]
            return byteString if byteString[:3] == byte else ""
        except ValueError:
            return ""
        except Exception:
            raise

    def getParam(self, value):
        return {
            'register': hexToInt(value[0]),
            'param': byteArrayToString(value[1:]),
        }

    def getParams(self, paramLength, length):
        params = []
        for i in range(0, paramLength):
            nextBytes = self.getNextBytesFind(length)  # TODO: Fix length
            params.append(self.getParam(nextBytes))
        return params

    def getOffset(self):
        return int((self.index - 2) / 3)

    def defaultValue(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    def nextByteIs(self, byte):
        nextIndex = self.index + 1
        nextByte = self.text[nextIndex:nextIndex + 2]
        skip = nextByte == byte
        if skip:
            self.index += 3
        return skip

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f'[{self.index}] Illegal character {t.value[0]!r}')
        self.index += 1
