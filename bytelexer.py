from sly import Lexer
from util import splitBytes, byteArrayToString, byteLength


class CCByteLexer(Lexer):
    def getNextBytes(self, num):
        length = num * 3
        nextBytes = self.text[self.index:self.index + length]
        value = splitBytes(nextBytes)
        self.index += length
        return value

    def getStrings(self, arr):
        params = []
        while True:
            try:
                index = arr.index('00', 1)
            except ValueError:
                params.append(arr[1:])
                break
            newArr = arr[:index]
            params.append(newArr[1:])
            arr = arr[len(newArr):]
        return list(map(lambda x: "\"%s\"" % byteArrayToString(x), params))

    def getParams(self, arr):
        params = []
        while True:
            try:
                index = arr.index('00', 1)
            except ValueError:
                params.append(arr[2:])
                break
            newArr = arr[:index]
            params.append(newArr[2:])
            arr = arr[len(newArr):]
        return map(byteArrayToString, params)

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f'[{self.index}] Illegal character {t.value[0]!r}')
        self.index += 1

    tokens = {
        END, UNDEFINED, BOOLEAN, REGISTER, FLOAT, NUMBER, PROPERTY1, PROPERTY2, # 00s
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
    ignore = ' \t'

    END = r'00'
    UNDEFINED = r'03'

    @_(r"04")
    def REGISTER(self, t):
        nextBytes = self.getNextBytes(1)
        t.value = int(nextBytes[0], 16)
        return t

    @_(r"05")
    def BOOLEAN(self, t):
        nextBytes = self.getNextBytes(1)
        t.value = nextBytes[0] == "01"
        return t

    @_(r"06")
    def FLOAT(self, t):
        nextBytes = self.getNextBytes(8)[::-1]
        t.value = float.fromhex(''.join(nextBytes))
        return t

    @_(r"07")
    def NUMBER(self, t):
        nextBytes = self.getNextBytes(4)[::-1]
        t.value = int(''.join(nextBytes), 16)
        return t

    @_(r"08")
    def PROPERTY1(self, t):
        nextBytes = self.getNextBytes(1)
        t.value = int(nextBytes[0], 16)
        return t

    @_(r"09")
    def PROPERTY2(self, t):
        nextBytes = self.getNextBytes(2)[::-1]
        t.value = int(''.join(nextBytes), 16)
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
        t.value = nextBytes[::-1]
        return t

    @_(r"88")
    def DEFINEDICTIONARY(self, t):
        nextBytes = self.getNextBytes(2)[::-1]
        length = byteLength(''.join(nextBytes))
        nextBytes = self.getNextBytes(length)
        params = self.getStrings(nextBytes[1:-1])
        t.value = params
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
        index = nextBytes.index('00')
        fnName = byteArrayToString(nextBytes[:index])
        params = self.getParams(nextBytes[index+5:-3])
        t.value = {
            'name': fnName,
            'params': params,
        }
        self.index += 1
        return t

    @_(r"96")
    def PUSH(self, t):
        nextBytes = self.getNextBytes(2)
        t.value = int(nextBytes[0], 16)
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
        index = nextBytes.index('00')
        fnName = byteArrayToString(nextBytes[:index])
        params = self.getParams(nextBytes[index+5:-3])
        t.value = {
            'name': fnName,
            'params': params,
        }
        return t

    @_(r"9[d|D]")
    def IF(self, t):
        nextBytes = self.getNextBytes(4)
        t.value = nextBytes
        return t
