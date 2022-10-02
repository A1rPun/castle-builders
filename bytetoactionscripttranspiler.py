from sly import Parser
from bytelexer import CCByteLexer


class CCActionScriptTranspiler(Parser):
    # debugfile = 'parser.out'
    tokens = CCByteLexer.tokens

    def __init__(self, names: dict = None):
        self.names = names or {}
        self.constantPool = []
        self.stack = []

    def error(self, t):
        print(f'[{self}] Illegal character {t}')

    @_('expr expr')
    def expr(self, p):
        pass

    @_('END')
    def expr(self, p):
        print("}")

    @_('UNDEFINED')
    def expr(self, p):
        print("undefined")

    @_('REGISTER')
    def expr(self, p):
        print("_loc%d_" % p.REGISTER)

    @_('BOOLEAN')
    def expr(self, p):
        print("true" if p.BOOLEAN else "false")

    @_('FLOAT')
    def expr(self, p):
        print(p.FLOAT)

    @_('NUMBER')
    def expr(self, p):
        print(p.NUMBER)

    @_('PROPERTY1')
    def expr(self, p):
        print(self.constantPool[p.PROPERTY1])

    @_('PROPERTY2')
    def expr(self, p):
        print(self.constantPool[p.PROPERTY2])

    @_('SUBSTRACT')
    def expr(self, p):
        print("-")

    @_('MULTIPLY')
    def expr(self, p):
        print("*")

    @_('DIVIDE')
    def expr(self, p):
        print("/")

    @_('AND')
    def expr(self, p):
        print("&&")

    @_('OR')
    def expr(self, p):
        print("||")

    @_('NOT')
    def expr(self, p):
        print("!")

    @_('POP')
    def expr(self, p):
        print("pop")

    @_('TOINT')
    def expr(self, p):
        print("ToInteger")

    @_('GETVAR')
    def expr(self, p):
        print("GetVariable")

    @_('SETVAR')
    def expr(self, p):
        print("SetVariable")

    @_('SETPROP')
    def expr(self, p):
        print("SetProperty")

    @_('REMOVESPRITE')
    def expr(self, p):
        print("RemoveSprite")

    @_('TRACE')
    def expr(self, p):
        print("Trace")

    @_('RANDOM')
    def expr(self, p):
        print("Random")

    @_('GETTIME')
    def expr(self, p):
        print("GetTime")

    @_('CALLFUNC')
    def expr(self, p):
        print("()")

    @_('RETURN')
    def expr(self, p):
        print("return")

    @_('MODULO')
    def expr(self, p):
        print("%")

    @_('NEW')
    def expr(self, p):
        print("new")

    @_('ADD2')
    def expr(self, p):
        print("+")

    @_('LESSTHAN')
    def expr(self, p):
        print("<")

    @_('EQUALS')
    def expr(self, p):
        print("==")

    @_('PUSHDUPLICATE')
    def expr(self, p):
        print("??")

    @_('GETMEMBER')
    def expr(self, p):
        print("GetMember")

    @_('SETMEMBER')
    def expr(self, p):
        print("SetMember")

    @_('INCREMENT')
    def expr(self, p):
        print("++")

    @_('DECREMENT')
    def expr(self, p):
        print("--")

    @_('CALLMETHOD')
    def expr(self, p):
        print("()")

    @_('BITAND')
    def expr(self, p):
        print("&")

    @_('BITOR')
    def expr(self, p):
        print("|")

    @_('BITXOR')
    def expr(self, p):
        print("^")

    @_('BITLSHIFT')
    def expr(self, p):
        print("<<")

    @_('BITRSHIFT')
    def expr(self, p):
        print(">>")

    @_('BITRSHIFTUNSIGNED')
    def expr(self, p):
        print(">>>")

    @_('STRICTEQUAL')
    def expr(self, p):
        print("==")

    @_('GREATERTHAN')
    def expr(self, p):
        print(">")

    @_('UNKNOWN')
    def expr(self, p):
        print("YESYESFULP")

    @_('STORE')
    def expr(self, p):
        print("StoreRegister")

    @_('DEFINEDICTIONARY')
    def expr(self, p):
        self.constantPool = p.DEFINEDICTIONARY
        # TODO REMOVE DEV RESTRICTION [:10]
        # print("var ConstantPool = { %s };" % ','.join(self.constantPool))
        print("var ConstantPool = { %s , ... };" % ','.join(self.constantPool[:5]))

    @_('GOTOLABEL')
    def expr(self, p):
        print(p)

    @_('DEFINEFUNC2')
    def expr(self, p):
        values = p.DEFINEFUNC2
        print("function2 %s(%s) {" %
              (values['name'], ','.join(values['params'])))

    @_('PUSH')
    def expr(self, p):
        print("Push")

    @_('JUMP')
    def expr(self, p):
        print("jump")

    @_('GETURL2')
    def expr(self, p):
        print("GETURL2")

    @_('DEFINEFUNC')
    def expr(self, p):
        values = p.DEFINEFUNC2
        print("function %s(%s) {" %
              (values['name'], ','.join(values['params'])))

    @_('IF')
    def expr(self, p):
        print("if")
