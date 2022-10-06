from ccbuilder.baselexer import BaseLexer
from ccbuilder.util import splitBytes, byteArrayToString, hexToInt, splitBytesOn
from ccbuilder.structlexer import StructLexer
from ccbuilder.funcoption import FuncOption


class ByteLexer(BaseLexer):
    def getValues(self, values):
        lexer = StructLexer()
        lexed = lexer.tokenize(' '.join(values))
        return lexed

    def getParam(self, value):
        return {
            'register': hexToInt(value[0]),
            'param': byteArrayToString(value[1:]),
        }

    def getParams(self, paramLength):
        params = []
        for i in range(0, paramLength):
            nextBytes = self.getNextBytesFind()
            params.append(self.getParam(nextBytes))
        return params

    def getOffset(self):
        return int((self.index - 2) / 3)

    def nextByteIs(self, byte):
        nextIndex = self.index + 1
        nextByte = self.text[nextIndex:nextIndex + 2]
        skip = nextByte == byte
        if skip:
            self.index += 3
        return skip

    tokens = {
        END,  # 00s
        AND, OR, SUBSTRACT, MULTIPLY, DIVIDE, NOT, POP, TOINT, GETVAR, SETVAR,  # 10s
        SETPROP, REMOVESPRITE, TRACE,  # 20s
        RANDOM, GETTIME, CALLFUNC, RETURN, MODULO,  # 30s
        NEW, ADD2, LESSTHAN, EQUALS, PUSHDUPLICATE, GETMEMBER, SETMEMBER,  # 40s
        INCREMENT, DECREMENT, CALLMETHOD,  # 50s
        BITAND, BITOR, BITXOR, BITLSHIFT, BITRSHIFT, BITRSHIFTUNSIGNED, STRICTEQUAL, GREATERTHAN,  # 60s
        UNKNOWN,  # 70s
        STORE, DEFINEDICTIONARY, GOTOLABEL, DEFINEFUNC2,  # 80s
        PUSH, JUMP, GETURL2, DEFINEFUNC, IF  # 90s
    }

    @_(r"00")
    def END(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"0[b|B]")
    def SUBSTRACT(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"0[c|C]")
    def MULTIPLY(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"0[d|D]")
    def DIVIDE(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"10")
    def AND(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"11")
    def OR(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"12")
    def NOT(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"17")
    def POP(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"18")
    def TOINT(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"1[c|C]")
    def GETVAR(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"1[d|D]")
    def SETVAR(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"23")
    def SETPROP(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"25")
    def REMOVESPRITE(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"26")
    def TRACE(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"30")
    def RANDOM(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"34")
    def GETTIME(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"3[d|D]")
    def CALLFUNC(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"3[e|E]")
    def RETURN(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"3[f|F]")
    def MODULO(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"40")
    def NEW(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"47")
    def ADD2(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"48")
    def LESSTHAN(self, t):
        offset = self.getOffset()
        modifier = self.nextByteIs("12")
        t.value = {'offset': offset, 'modifier': modifier}
        return t

    @_(r"49")
    def EQUALS(self, t):
        offset = self.getOffset()
        modifier = self.nextByteIs("12")
        t.value = {'offset': offset, 'modifier': modifier}
        return t

    @_(r"4[c|C]")
    def PUSHDUPLICATE(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"4[e|E]")
    def GETMEMBER(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"4[f|F]")
    def SETMEMBER(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"50")
    def INCREMENT(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"51")
    def DECREMENT(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"52")
    def CALLMETHOD(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"60")
    def BITAND(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"61")
    def BITOR(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"62")
    def BITXOR(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"63")
    def BITLSHIFT(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"64")
    def BITRSHIFT(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"65")
    def BITRSHIFTUNSIGNED(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"66")
    def STRICTEQUAL(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"67")
    def GREATERTHAN(self, t):
        offset = self.getOffset()
        modifier = self.nextByteIs("12")
        t.value = {'offset': offset, 'modifier': modifier}
        return t

    @_(r"70")
    def UNKNOWN(self, t):
        offset = self.getOffset()
        t.value = {'offset': offset}
        return t

    @_(r"87")
    def STORE(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(3)
        modifier = self.nextByteIs("4f")
        t.value = {
            'offset': offset,
            'value': hexToInt(nextBytes[2]),
            'modifier': modifier,
        }
        return t

    @_(r"88")
    def DEFINEDICTIONARY(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(2)[::-1]
        length = hexToInt(''.join(nextBytes))
        nextBytes = self.getNextBytes(length)
        params = splitBytesOn(nextBytes[2:-1])
        t.value = {
            'pool': list(map(byteArrayToString, params)),
            'offset': offset,
        }
        return t

    @_(r"8[c|C]")
    def GOTOLABEL(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(2)
        length = hexToInt(nextBytes[0])
        nextBytes = self.getNextBytes(length)
        t.value = {'offset': offset, 'value': byteArrayToString(nextBytes)}
        return t

    @_(r"8[e|E]")
    def DEFINEFUNC2(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(2)
        length = hexToInt(nextBytes[0])
        nextBytes = self.getNextBytesFind()
        fnName = byteArrayToString(nextBytes)
        nextBytes = self.getNextBytes(1)
        paramLength = hexToInt(nextBytes[0])
        nextBytes = self.getNextBytes(2)
        regCount = hexToInt(nextBytes[1])
        nextBytes = self.getNextBytes(2)
        funcOption = FuncOption(hexToInt(nextBytes[0]))
        params = self.getParams(paramLength)
        nextBytes = self.getNextBytes(2)
        fnLength = hexToInt(''.join(nextBytes[::-1]))
        t.value = {
            'name': fnName,
            'paramLength': paramLength,
            'regCount': regCount,
            'params': params,
            'options': funcOption,
            'functionLength': fnLength,
            'offset': offset + length + 3,
        }
        return t

    @_(r"96")
    def PUSH(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(2)
        length = hexToInt(nextBytes[0])
        nextBytes = self.getNextBytes(length)
        t.value = {'offset': offset, 'value': self.getValues(nextBytes)}
        return t

    @_(r"99")
    def JUMP(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(4)
        length = hexToInt(f"{nextBytes[3]}{nextBytes[2]}")
        t.value = {
            'value': length,
            'offset': offset + 5,
        }
        return t

    @_(r"9[a|A]")
    def GETURL2(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(3)
        t.value = {'offset': offset, 'value': nextBytes}
        return t

    @_(r"9[b|B]")
    def DEFINEFUNC(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(2)
        length = hexToInt(nextBytes[0])
        nextBytes = self.getNextBytesFind()
        fnName = byteArrayToString(nextBytes)
        nextBytes = self.getNextBytes(2)
        paramLength = hexToInt(nextBytes[0])
        params = self.getParams(paramLength)
        nextBytes = self.getNextBytes(2)
        fnLength = hexToInt(''.join(nextBytes[::-1]))
        t.value = {
            'name': fnName,
            'paramLength': paramLength,
            'params': params,
            'functionLength': fnLength,
            'offset': offset + length + 3,
        }
        return t

    @_(r"9[d|D]")
    def IF(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(4)
        # TODO nextBytes[3] nextBytes[2]
        length = hexToInt(f"{nextBytes[3]}{nextBytes[2]}")
        t.value = {
            'value': length,
            'offset': offset + 5,
        }
        return t
