from sly import Lexer


def splitBytes(string):
    return string.strip().split(" ")

def byteArrayToString(byteArray):
    return bytes.fromhex(''.join(byteArray)).decode("utf-8")

def byteLength(string):
    return int(string, 16) * 3


class CCByteLexer(Lexer):
    tokens = {
        END, UNDEFINED, BOOLEAN, REGISTER, PROPERTY, FLOAT, NUMBER, CONSTANT, # 00s
        AND, OR, SUBSTRACT, MULTIPLY, DIVIDE, NOT, POP, TOINT, GETVAR, SETVAR, # 10s
        SETPROP, REMOVESPRITE, TRACE, # 20s
        RANDOM, GETTIME, CALLFUNC, RETURN, MODULO, # 30s
        NEW, ADD2, LESSTHAN, EQUALS, PUSHDUPLICATE, GETMEMBER, SETMEMBER, # 40s
        INCREMENT, DECREMENT, CALLMETHOD, # 50s
        BITAND, BITOR, BITXOR, BITLSHIFT, BITRSHIFT, BITRSHIFTUNSIGNED, STRICTEQUAL, GREATERTHAN, # 60s
        UNKNOWN, # 70s
        STORE, DEFINEDICTIONARY, GOTOLABEL, DEFINEFUNCV7, # 80s
        PUSH, JUMP, GETURL2, DEFINEFUNC, IF # 90s
    }
    ignore = ' \t'

    END = r'00'
    UNDEFINED = r'03'

    @_(r"04 [0-9a-fA-F]+")
    def REGISTER(self, t):
        register = splitBytes(t.value)[1]
        t.value = int(register, 16)
        return t

    @_(r"05 [0-1]+")
    def BOOLEAN(self, t):
        boolean = splitBytes(t.value)[1]
        t.value = int(boolean, 16)
        return t

    @_(r"06 [0-9a-fA-F]+ [0-9a-fA-F]+ [0-9a-fA-F]+ [0-9a-fA-F]+ [0-9a-fA-F]+ [0-9a-fA-F]+ [0-9a-fA-F]+ [0-9a-fA-F]+")
    def FLOAT(self, t):
        byteArray = splitBytes(t.value)[:0:-1]
        t.value = float.fromhex(''.join(byteArray))
        return t

    @_(r"07 [0-9a-fA-F]+ [0-9a-fA-F]+ [0-9a-fA-F]+ [0-9a-fA-F]+")
    def NUMBER(self, t):
        byteArray = splitBytes(t.value)[:0:-1]
        t.value = int(''.join(byteArray), 16)
        return t

    @_(r"08 [0-9a-fA-F]+")
    def PROPERTY(self, t):
        prop = splitBytes(t.value)[1]
        t.value = int(prop, 16)
        return t

    @_(r"09 [0-9a-fA-F]+ [0-9a-fA-F]+")
    def CONSTANT(self, t):
        byteArray = splitBytes(t.value)
        t.value = int(''.join(byteArray), 16)
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

    @_(r"87 [0-9a-fA-F]+ [0-9a-fA-F]+ [0-9a-fA-F]+")
    def STORE(self, t):
        byteArray = splitBytes(t.value)[:0:-1]
        t.value = byteArray
        return t

    @_(r"88 [0-9a-fA-F]+ [0-9a-fA-F]+")
    def DEFINEDICTIONARY(self, t):
        length = splitBytes(t.value)[:0:-1]
        length = byteLength(''.join(length))
        value = self.text[self.index:self.index+length]
        value = splitBytes(value)
        t.value = byteArrayToString(value)
        # t.value = value
        self.index += length
        return t

    @_(r"8[c|C] [0-9a-fA-F]+ [0-9a-fA-F]+")
    def GOTOLABEL(self, t):
        length = splitBytes(t.value)[1]
        length = byteLength(length)
        value = self.text[self.index:self.index+length]
        value = splitBytes(value)
        t.value = byteArrayToString(value)
        self.index += length
        return t

    @_(r"8[e|E] [0-9a-fA-F]+ [0-9a-fA-F]+")
    def DEFINEFUNCV7(self, t):
        length = splitBytes(t.value)[1]
        length = byteLength(length)
        value = self.text[self.index:self.index+length]
        value = splitBytes(value)
        # t.value = byteArrayToString(value)
        t.value = value
        self.index += length
        return t

    @_(r"96 [0-9a-fA-F]+ [0-9a-fA-F]+")
    def PUSH(self, t):
        length = splitBytes(t.value)[1]
        t.value = int(length, 16)
        return t

    @_(r"99 [0-9a-fA-F]+ [0-9a-fA-F]+ [0-9a-fA-F]+ [0-9a-fA-F]+")
    def JUMP(self, t):
        byteArray = splitBytes(t.value)[1:]
        t.value = byteArray
        return t

    @_(r"9[a|A] [0-9a-fA-F]+ [0-9a-fA-F]+ [0-9a-fA-F]+")
    def GETURL2(self, t):
        byteArray = splitBytes(t.value)[1:]
        t.value = byteArray
        return t

    @_(r"9[b|B] [0-9a-fA-F]+ [0-9a-fA-F]+")
    def DEFINEFUNC(self, t):
        length = splitBytes(t.value)[1]
        length = byteLength(length)
        value = self.text[self.index:self.index+length]
        value = splitBytes(value)
        # t.value = byteArrayToString(value)
        t.value = value
        self.index += length
        return t

    @_(r"9[d|D] [0-9a-fA-F]+ [0-9a-fA-F]+ [0-9a-fA-F]+ [0-9a-fA-F]+")
    def IF(self, t):
        byteArray = splitBytes(t.value)[1:]
        t.value = byteArray
        return t

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += 1

    def error(self, t):
        value = self.text[self.index:self.index+2]
        print("[%d] Illegal character '%s'" % (self.index, value))
        self.index += 2
