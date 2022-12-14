from sly import Parser
from ccbuilder.actionscript_lexer import ActionScriptLexer
from ccbuilder.util import toByte


class ByteParser(Parser):
    tokens = ActionScriptLexer.tokens

    def __init__(self):
        self.names = {}
        self.bytes = []

    def getCode(self):
        pool = [0x88, 0x02, 0x00, 0x00, 0x00]
        result = pool + self.bytes + [0x00]
        return ' '.join(map(lambda x: toByte(x), result))

    # precedence = (
    #     ('left', PLUS, MINUS),
    #     ('left', TIMES, DIVIDE),
    #     ('right', UMINUS)
    # )

    # @_('expr')
    # def statement(self, p):
    #     pass

    # @_('LPAREN expr RPAREN')
    # def expr(self, p):
    #     print("()")
    #     return p.expr

    # @_('LACCOL expr RACCOL')
    # def expr(self, p):
    #     print("{}")
    #     return p.expr

    @_('NAME ASSIGN expr')
    def expr(self, p):
        self.names[p.NAME] = p.expr

    @_('";"')
    def expr(self, p):
        self.bytes += [0x17]

    # @_('expr PLUS expr')
    # def expr(self, p):
    #     return p.expr0 + p.expr1

    # @_('expr MINUS expr')
    # def expr(self, p):
    #     return p.expr0 - p.expr1

    # @_('expr TIMES expr')
    # def expr(self, p):
    #     return p.expr0 * p.expr1

    # @_('expr DIVIDE expr')
    # def expr(self, p):
    #     return p.expr0 / p.expr1

    # @_('MINUS expr %prec UMINUS')
    # def expr(self, p):
    #     return -p.expr

    @_('FUNCTION NAME LPAREN RPAREN')
    def expr(self, p):
        self.bytes += [0x8e]
        print("func")
        return p.expr

    @_('IF LPAREN NAME RPAREN')
    def expr(self, p):
        print("if")
        # return p.expr

    @_('NUMBER')
    def expr(self, p):
        print("number")
        self.bytes += [0x96, 0x05, 0x00, 0x07, int(p.NUMBER), 0x00, 0x00, 0x00]
    # return int(p.NUMBER)

    @_('TRUE')
    def expr(self, p):
        print("true")
        self.bytes += [0x96, 0x02, 0x00, 0x05, 0x01]

    @_('FALSE')
    def expr(self, p):
        print("false")
        self.bytes += [0x96, 0x02, 0x00, 0x05, 0x00]

    @_('NAME')
    def expr(self, p):
        print("name", p.NAME)
        # try:
        #     return self.names[p.NAME]
        # except LookupError:
        #     print(f'Undefined name {p.NAME!r}')
        #     return 0

    # tokens = ActionScriptLexer.tokens

    # def __init__(self, names: dict = None):
    #     self.names = names or {}
    #     self.stack = []
    #     self.byteArray = []

    # def addBytes(self, byte):
    #     self.byteArray.append(toByte(byte))

    # def getCode(self):
    #     return ""

    # @_('expr expr')
    # def expr(self, p):
    #     pass

    # @_('END')
    # def expr(self, p):
    #     self.addBytes(0x00)

    # @_('SUBSTRACT')
    # def expr(self, p):
    #     self.addBytes(0x0b)

    # @_('MULTIPLY')
    # def expr(self, p):
    #     self.addBytes(0x0c)

    # @_('DIVIDE')
    # def expr(self, p):
    #     self.addBytes(0x0d)

    # @_('AND')
    # def expr(self, p):
    #     self.addBytes(0x10)

    # @_('OR')
    # def expr(self, p):
    #     self.addBytes(0x11)

    # @_('NOT')
    # def expr(self, p):
    #     self.addBytes(0x12)

    # @_('POP')
    # def expr(self, p):
    #     self.addBytes(0x17)

    # @_('TOINT')
    # def expr(self, p):
    #     self.addBytes(0x18)

    # @_('GETVAR')
    # def expr(self, p):
    #     self.addBytes(0x1c)

    # @_('SETVAR')
    # def expr(self, p):
    #     self.addBytes(0x1d)

    # @_('SETPROP')
    # def expr(self, p):
    #     self.addBytes(0x23)

    # @_('REMOVESPRITE')
    # def expr(self, p):
    #     self.addBytes(0x25)

    # @_('TRACE')
    # def expr(self, p):
    #     self.addBytes(0x26)

    # @_('RANDOM')
    # def expr(self, p):
    #     self.addBytes(0x30)

    # @_('GETTIME')
    # def expr(self, p):
    #     self.addBytes(0x34)

    # @_('CALLFUNC')
    # def expr(self, p):
    #     self.addBytes(0x3d)

    # @_('RETURN')
    # def expr(self, p):
    #     self.addBytes(0x3e)

    # @_('MODULO')
    # def expr(self, p):
    #     self.addBytes(0x3f)

    # @_('NEW')
    # def expr(self, p):
    #     self.addBytes(0x40)

    # @_('TYPEDADD')
    # def expr(self, p):
    #     self.addBytes(0x47)

    # @_('TYPEDLESSTHAN')
    # def expr(self, p):
    #     self.addBytes(0x48)

    # @_('TYPEDEQUAL')
    # def expr(self, p):
    #     self.addBytes(0x49)

    # @_('PUSHDUPLICATE')
    # def expr(self, p):
    #     self.addBytes(0x4c)

    # @_('GETMEMBER')
    # def expr(self, p):
    #     self.addBytes(0x4e)

    # @_('SETMEMBER')
    # def expr(self, p):
    #     self.addBytes(0x4f)

    # @_('INCREMENT')
    # def expr(self, p):
    #     self.addBytes(0x50)

    # @_('DECREMENT')
    # def expr(self, p):
    #     self.addBytes(0x51)

    # @_('CALLMETHOD')
    # def expr(self, p):
    #     self.addBytes(0x52)

    # @_('BITAND')
    # def expr(self, p):
    #     self.addBytes(0x60)

    # @_('BITOR')
    # def expr(self, p):
    #     self.addBytes(0x61)

    # @_('BITXOR')
    # def expr(self, p):
    #     self.addBytes(0x62)

    # @_('BITLSHIFT')
    # def expr(self, p):
    #     self.addBytes(0x63)

    # @_('BITRSHIFT')
    # def expr(self, p):
    #     self.addBytes(0x64)

    # @_('BITRSHIFTUNSIGNED')
    # def expr(self, p):
    #     self.addBytes(0x65)

    # @_('STRICTEQUAL')
    # def expr(self, p):
    #     self.addBytes(0x66)

    # @_('GREATERTHAN')
    # def expr(self, p):
    #     self.addBytes(0x67)

    # @_('UNKNOWN')
    # def expr(self, p):
    #     self.addBytes(0x70)

    # @_('STORE')
    # def expr(self, p):
    #     self.addBytes(0x87)

    # @_('DEFINEDICTIONARY')
    # def expr(self, p):
    #     self.addBytes(0x88)

    # @_('GOTOLABEL')
    # def expr(self, p):
    #     self.addBytes(0x8c)

    # @_('DEFINEFUNC2')
    # def expr(self, p):
    #     self.addBytes(0x8e)

    # @_('PUSH')
    # def expr(self, p):
    #     self.addBytes(0x96)

    # @_('JUMP')
    # def expr(self, p):
    #     self.addBytes(0x99)

    # @_('GETURL2')
    # def expr(self, p):
    #     self.addBytes(0x9a)

    # @_('DEFINEFUNC')
    # def expr(self, p):
    #     self.addBytes(0x9b)

    # @_('IF')
    # def expr(self, p):
    #     self.addBytes(0x9d)
