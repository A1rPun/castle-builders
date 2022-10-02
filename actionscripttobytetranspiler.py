from sly import Parser
from bytelexer import CCByteLexer
from util import toByte


class CCByteTranspiler(Parser):
    tokens = CCByteLexer.tokens

    def __init__(self, names: dict = None):
        self.names = names or {}
        self.stack = []
        self.byteArray = []

    def addBytes(self, byte):
        self.byteArray.append(toByte(byte))

    # @property
    # def last_item_on_stack(self):
    #     return self.stack[-1] if len(self.stack) > 0 else None

    # def error(self, p):
    #     if p:
    #         self.errok()

    @_('expr expr')
    def expr(self, p):
        pass

    @_('END')
    def expr(self, p):
        self.addBytes(0x00)

    @_('UNDEFINED')
    def expr(self, p):
        self.addBytes(0x03)

    @_('REGISTER')
    def expr(self, p):
        self.addBytes(0x04)

    @_('BOOLEAN')
    def expr(self, p):
        self.addBytes(0x05)

    @_('FLOAT')
    def expr(self, p):
        self.addBytes(0x06)

    @_('NUMBER')
    def expr(self, p):
        self.addBytes(0x07)

    @_('PROPERTY1')
    def expr(self, p):
        self.addBytes(0x08)

    @_('PROPERTY2')
    def expr(self, p):
        self.addBytes(0x09)

    @_('SUBSTRACT')
    def expr(self, p):
        self.addBytes(0x0b)

    @_('MULTIPLY')
    def expr(self, p):
        self.addBytes(0x0c)

    @_('DIVIDE')
    def expr(self, p):
        self.addBytes(0x0d)

    @_('AND')
    def expr(self, p):
        self.addBytes(0x10)

    @_('OR')
    def expr(self, p):
        self.addBytes(0x11)

    @_('NOT')
    def expr(self, p):
        self.addBytes(0x12)

    @_('POP')
    def expr(self, p):
        self.addBytes(0x17)

    @_('TOINT')
    def expr(self, p):
        self.addBytes(0x18)

    @_('GETVAR')
    def expr(self, p):
        self.addBytes(0x1c)

    @_('SETVAR')
    def expr(self, p):
        self.addBytes(0x1d)

    @_('SETPROP')
    def expr(self, p):
        self.addBytes(0x23)

    @_('REMOVESPRITE')
    def expr(self, p):
        self.addBytes(0x25)

    @_('TRACE')
    def expr(self, p):
        self.addBytes(0x26)

    @_('RANDOM')
    def expr(self, p):
        self.addBytes(0x30)

    @_('GETTIME')
    def expr(self, p):
        self.addBytes(0x34)

    @_('CALLFUNC')
    def expr(self, p):
        self.addBytes(0x3d)

    @_('RETURN')
    def expr(self, p):
        self.addBytes(0x3e)

    @_('MODULO')
    def expr(self, p):
        self.addBytes(0x3f)

    @_('NEW')
    def expr(self, p):
        self.addBytes(0x40)

    @_('ADD2')
    def expr(self, p):
        self.addBytes(0x47)

    @_('LESSTHAN')
    def expr(self, p):
        self.addBytes(0x48)

    @_('EQUALS')
    def expr(self, p):
        self.addBytes(0x49)

    @_('PUSHDUPLICATE')
    def expr(self, p):
        self.addBytes(0x4c)

    @_('GETMEMBER')
    def expr(self, p):
        self.addBytes(0x4e)

    @_('SETMEMBER')
    def expr(self, p):
        self.addBytes(0x4f)

    @_('INCREMENT')
    def expr(self, p):
        self.addBytes(0x50)

    @_('DECREMENT')
    def expr(self, p):
        self.addBytes(0x51)

    @_('CALLMETHOD')
    def expr(self, p):
        self.addBytes(0x52)

    @_('BITAND')
    def expr(self, p):
        self.addBytes(0x60)

    @_('BITOR')
    def expr(self, p):
        self.addBytes(0x61)

    @_('BITXOR')
    def expr(self, p):
        self.addBytes(0x62)

    @_('BITLSHIFT')
    def expr(self, p):
        self.addBytes(0x63)

    @_('BITRSHIFT')
    def expr(self, p):
        self.addBytes(0x64)

    @_('BITRSHIFTUNSIGNED')
    def expr(self, p):
        self.addBytes(0x65)

    @_('STRICTEQUAL')
    def expr(self, p):
        self.addBytes(0x66)

    @_('GREATERTHAN')
    def expr(self, p):
        self.addBytes(0x67)

    @_('UNKNOWN')
    def expr(self, p):
        self.addBytes(0x70)

    @_('STORE')
    def expr(self, p):
        self.addBytes(0x87)

    @_('DEFINEDICTIONARY')
    def expr(self, p):
        self.addBytes(0x88)

    @_('GOTOLABEL')
    def expr(self, p):
        self.addBytes(0x8c)

    @_('DEFINEFUNC2')
    def expr(self, p):
        print(p.DEFINEFUNC2)
        self.addBytes(0x8e)

    @_('PUSH')
    def expr(self, p):
        print(p.PUSH)
        self.addBytes(0x96)

    @_('JUMP')
    def expr(self, p):
        self.addBytes(0x99)

    @_('GETURL2')
    def expr(self, p):
        self.addBytes(0x9a)

    @_('DEFINEFUNC')
    def expr(self, p):
        self.addBytes(0x9b)

    @_('IF')
    def expr(self, p):
        self.addBytes(0x9d)
