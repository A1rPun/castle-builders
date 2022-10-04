from baselexer import BaseLexer
from util import splitBytes, byteArrayToString, byteLength, splitBytesOn
from structlexer import StructLexer

class ByteLexer(BaseLexer):
    def getValues(self, values):
        lexer = StructLexer()
        lexed = lexer.tokenize(' '.join(values))
        return lexed

    def getParam(self, value):
        return {
            'register': int(value[0], 16),
            'param': byteArrayToString(value[1:]),
        }

    tokens = {
        END, # 00s
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
        return t

    SUBSTRACT = r'0[b|B]'
    MULTIPLY = r'0[c|C]'
    DIVIDE = r'0[d|D]'
    AND = r'10'
    OR = r'11'
    NOT = r'12'
    POP = r'17'
    TOINT = r'18'
    GETVAR = r'1[c|C]'
    SETVAR = r'1[d|D]'
    SETPROP = r'23'
    REMOVESPRITE = r'25'
    TRACE = r'26'
    RANDOM = r'30'
    GETTIME = r'34'
    CALLFUNC = r'3[d|D]'
    RETURN = r'3[e|E]'
    MODULO = r'3[f|F]'
    NEW = r'40'
    ADD2 = r'47'
    LESSTHAN = r'48'
    EQUALS = r'49'
    PUSHDUPLICATE = r'4[c|C]'
    GETMEMBER = r'4[e|E]'
    SETMEMBER = r'4[f|F]'
    INCREMENT = r'50'
    DECREMENT = r'51'
    CALLMETHOD = r'52'
    BITAND = r'60'
    BITOR = r'61'
    BITXOR = r'62'
    BITLSHIFT = r'63'
    BITRSHIFT = r'64'
    BITRSHIFTUNSIGNED = r'65'
    STRICTEQUAL = r'66'
    GREATERTHAN = r'67'
    UNKNOWN = r'70'

    @_(r"87")
    def STORE(self, t):
        nextBytes = self.getNextBytes(3)
        t.value = int(nextBytes[2], 16)
        return t

    @_(r"88")
    def DEFINEDICTIONARY(self, t):
        nextBytes = self.getNextBytes(2)[::-1]
        length = byteLength(''.join(nextBytes))
        nextBytes = self.getNextBytes(length)
        params = splitBytesOn(nextBytes[2:-1])
        t.value = list(map(byteArrayToString, params))
        return t

    @_(r"8[c|C]")
    def GOTOLABEL(self, t):
        nextBytes = self.getNextBytes(2)
        length = byteLength(nextBytes[0])
        nextBytes = self.getNextBytes(length)
        t.value = byteArrayToString(nextBytes)
        return t

    @_(r"8[e|E]")
    def DEFINEFUNC2(self, t):
        nextBytes = self.getNextBytes(2)
        length = byteLength(nextBytes[0])
        nextBytes = self.getNextBytes(length)
        splitted = splitBytesOn(nextBytes)
        fnName = byteArrayToString(splitted[0])
        paramLength = int(splitted[1][0], 16)
        regCount = int(splitted[2][0], 16)
        params = splitted[3:-1]
        # TODO Fix 0 params split issue
        fnLength = int(splitted[-1][0], 16)
        t.value = {
            'name': fnName,
            'paramLength': paramLength,
            'regCount': regCount,
            'params': list(map(self.getParam, params)),
            'functionLength': fnLength,
        }
        return t

    @_(r"96")
    def PUSH(self, t):
        nextBytes = self.getNextBytes(2)
        length = int(nextBytes[0], 16)
        nextBytes = self.getNextBytes(length)
        t.value = self.getValues(nextBytes)
        return t

    @_(r"99")
    def JUMP(self, t):
        nextBytes = self.getNextBytes(4)
        t.value = nextBytes
        return t

    @_(r"9[a|A]")
    def GETURL2(self, t):
        nextBytes = self.getNextBytes(3)
        t.value = nextBytes
        return t

    @_(r"9[b|B]")
    def DEFINEFUNC(self, t):
        nextBytes = self.getNextBytes(2)
        length = byteLength(nextBytes[0])
        nextBytes = self.getNextBytes(length)
        splitted = splitBytesOn(nextBytes)
        fnName = byteArrayToString(splitted[0])
        paramLength = int(splitted[1], 16)
        # params = self.getParams(splitted[2:-1])
        fnLength = int(splitted[-1], 16)
        t.value = {
            'name': fnName,
            'paramLength': paramLength,
            'params': params,
            'functionLength': fnLength,
        }
        return t

    @_(r"9[d|D]")
    def IF(self, t):
        nextBytes = self.getNextBytes(4)
        # TODO nextBytes[3] nextBytes[2]
        length = byteLength(nextBytes[2])
        t.value = length
        return t
