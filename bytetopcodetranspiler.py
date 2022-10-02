from sly import Parser
from bytelexer import ByteLexer


class PCodeTranspiler(Parser):
    tokens = ByteLexer.tokens

    def __init__(self, names: dict = None):
        self.names = names or {}
        self.constantPool = []

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
        print("register%d" % p.REGISTER)

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
        print("Substract")

    @_('MULTIPLY')
    def expr(self, p):
        print("Multiply")

    @_('DIVIDE')
    def expr(self, p):
        print("Divide")

    @_('AND')
    def expr(self, p):
        print("And")

    @_('OR')
    def expr(self, p):
        print("Or")

    @_('NOT')
    def expr(self, p):
        print("Not")

    @_('POP')
    def expr(self, p):
        print("Pop")

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
        print("CallFunction")

    @_('RETURN')
    def expr(self, p):
        print("Return")

    @_('MODULO')
    def expr(self, p):
        print("Modulo")

    @_('NEW')
    def expr(self, p):
        print("New")

    @_('ADD2')
    def expr(self, p):
        print("Add2")

    @_('LESSTHAN')
    def expr(self, p):
        print("Less2")

    @_('EQUALS')
    def expr(self, p):
        print("Equals2")

    @_('PUSHDUPLICATE')
    def expr(self, p):
        print("Push")

    @_('GETMEMBER')
    def expr(self, p):
        print("GetMember")

    @_('SETMEMBER')
    def expr(self, p):
        print("SetMember")

    @_('INCREMENT')
    def expr(self, p):
        print("Increment")

    @_('DECREMENT')
    def expr(self, p):
        print("Decrement")

    @_('CALLMETHOD')
    def expr(self, p):
        print("CallMethod")

    @_('BITAND')
    def expr(self, p):
        print("BitAnd")

    @_('BITOR')
    def expr(self, p):
        print("BitOr")

    @_('BITXOR')
    def expr(self, p):
        print("BitXor")

    @_('BITLSHIFT')
    def expr(self, p):
        print("BitLShift")

    @_('BITRSHIFT')
    def expr(self, p):
        print("BitRShift")

    @_('BITRSHIFTUNSIGNED')
    def expr(self, p):
        # TODO
        print("BitRShift?")

    @_('STRICTEQUAL')
    def expr(self, p):
        print("StrictEquals")

    @_('GREATERTHAN')
    def expr(self, p):
        print("Greater")

    @_('UNKNOWN')
    def expr(self, p):
        print("Unknown_70")

    @_('STORE')
    def expr(self, p):
        print("StoreRegister %d" % p.STORE)

    @_('DEFINEDICTIONARY')
    def expr(self, p):
        self.constantPool = p.DEFINEDICTIONARY
        # TODO REMOVE DEV RESTRICTION
        # print("var ConstantPool = { %s };" % ','.join(self.constantPool))
        print("ConstantPool %s ..." % ' '.join(self.constantPool[:5]))

    @_('GOTOLABEL')
    def expr(self, p):
        print("GoToLabel")

    @_('DEFINEFUNC2')
    def expr(self, p):
        values = p.DEFINEFUNC2
        print("DefineFunction2 %s %d %d false true true false true false true false false %s {" %
              (values['name'], values['paramLength'], values['regCount'], ' '.join(values['params'])))

    @_('PUSH')
    def expr(self, p):
        print("Push")

    @_('JUMP')
    def expr(self, p):
        print("Jump")

    @_('GETURL2')
    def expr(self, p):
        print("GetURL2")

    @_('DEFINEFUNC')
    def expr(self, p):
        values = p.DEFINEFUNC2
        print("DefineFunction %s %d %s {" %
              (values['name'], values['paramLength'], ' '.join(values['params'])))

    @_('IF')
    def expr(self, p):
        print("If")
