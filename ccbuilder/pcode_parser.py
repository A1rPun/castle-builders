from sly import Parser
from ccbuilder.bytelexer import ByteLexer
from ccbuilder.util import boolToStr
from ccbuilder.funcoption import FuncOption


class PCodeParser(Parser):
    tokens = ByteLexer.tokens

    def __init__(self, names: dict = None):
        self.names = names or {}
        self.constantPool = []
        self.code = ""

    def error(self, t):
        print(f'[{self}] Illegal character {t}')

    def printCode(self, code):
        self.code += f"{code}\n"

    def parseStructItem(self, item):
        if item.type == 'STRING':
            return item.value
        elif item.type == 'FLOAT':
            return str(item.value)
        elif item.type == 'NULL':
            return "null"
        elif item.type == 'REGISTER':
            return "register%d" % item.value
        elif item.type == 'BOOLEAN':
            return boolToStr(item.value)
        elif item.type == 'DOUBLE':
            return str(item.value)
        elif item.type == 'INTEGER':
            return str(item.value)
        elif item.type == 'DICTLOOKUP':
            return self.constantPool[item.value]
        elif item.type == 'DICTLOOKUPLARGE':
            return self.constantPool[item.value]
        return "undefined"

    def parseStruct(self, struct):
        values = map(self.parseStructItem, struct)
        return ' '.join(values)

    @_('expr expr')
    def expr(self, p):
        pass

    @_('END')
    def expr(self, p):
        self.printCode("}")

    @_('SUBSTRACT')
    def expr(self, p):
        self.printCode("Substract")

    @_('MULTIPLY')
    def expr(self, p):
        self.printCode("Multiply")

    @_('DIVIDE')
    def expr(self, p):
        self.printCode("Divide")

    @_('AND')
    def expr(self, p):
        self.printCode("And")

    @_('OR')
    def expr(self, p):
        self.printCode("Or")

    @_('NOT')
    def expr(self, p):
        self.printCode("Not")

    @_('POP')
    def expr(self, p):
        self.printCode("Pop")

    @_('TOINT')
    def expr(self, p):
        self.printCode("ToInteger")

    @_('GETVAR')
    def expr(self, p):
        self.printCode("GetVariable")

    @_('SETVAR')
    def expr(self, p):
        self.printCode("SetVariable")

    @_('SETPROP')
    def expr(self, p):
        self.printCode("SetProperty")

    @_('REMOVESPRITE')
    def expr(self, p):
        self.printCode("RemoveSprite")

    @_('TRACE')
    def expr(self, p):
        self.printCode("Trace")

    @_('RANDOM')
    def expr(self, p):
        self.printCode("Random")

    @_('GETTIME')
    def expr(self, p):
        self.printCode("GetTime")

    @_('CALLFUNC')
    def expr(self, p):
        self.printCode("CallFunction")

    @_('RETURN')
    def expr(self, p):
        self.printCode("Return")

    @_('MODULO')
    def expr(self, p):
        self.printCode("Modulo")

    @_('NEW')
    def expr(self, p):
        self.printCode("NewObject")

    @_('ADD2')
    def expr(self, p):
        self.printCode("Add2")

    @_('LESSTHAN')
    def expr(self, p):
        self.printCode("Less2")

    @_('EQUALS')
    def expr(self, p):
        self.printCode("Equals2")

    @_('PUSHDUPLICATE')
    def expr(self, p):
        self.printCode("Push")

    @_('GETMEMBER')
    def expr(self, p):
        self.printCode("GetMember")

    @_('SETMEMBER')
    def expr(self, p):
        self.printCode("SetMember")

    @_('INCREMENT')
    def expr(self, p):
        self.printCode("Increment")

    @_('DECREMENT')
    def expr(self, p):
        self.printCode("Decrement")

    @_('CALLMETHOD')
    def expr(self, p):
        self.printCode("CallMethod")

    @_('BITAND')
    def expr(self, p):
        self.printCode("BitAnd")

    @_('BITOR')
    def expr(self, p):
        self.printCode("BitOr")

    @_('BITXOR')
    def expr(self, p):
        self.printCode("BitXor")

    @_('BITLSHIFT')
    def expr(self, p):
        self.printCode("BitLShift")

    @_('BITRSHIFT')
    def expr(self, p):
        self.printCode("BitRShift")

    @_('BITRSHIFTUNSIGNED')
    def expr(self, p):
        # TODO
        self.printCode("BitRShift?")

    @_('STRICTEQUAL')
    def expr(self, p):
        self.printCode("StrictEquals")

    @_('GREATERTHAN')
    def expr(self, p):
        self.printCode("Greater")

    @_('UNKNOWN')
    def expr(self, p):
        self.printCode("Unknown_70")

    @_('STORE')
    def expr(self, p):
        self.printCode("StoreRegister %d" % p.STORE['value'])

    @_('DEFINEDICTIONARY')
    def expr(self, p):
        self.constantPool = list(map(lambda x: f"\"{x}\"", p.DEFINEDICTIONARY['pool']))
        # self.printCode(f"ConstantPool {' '.join(self.constantPool)}")

    @_('GOTOLABEL')
    def expr(self, p):
        self.printCode("GoToLabel")

    @_('DEFINEFUNC2')
    def expr(self, p):
        values = p.DEFINEFUNC2
        paramStr = ','.join(map(lambda x: f"{x['register']} \"{x['param']}\"", values['params']))
        options = values['options']
        optionStr = ""
        for op in (FuncOption):
            optionStr += f"{boolToStr(options & op.value)} "
        optionStr += "false"
        self.printCode(f"DefineFunction2 \"{values['name']}\" {values['paramLength']} {values['regCount']} {optionStr} {paramStr} {{")

    @_('PUSH')
    def expr(self, p):
        self.printCode("Push %s" % self.parseStruct(p.PUSH['value']))

    @_('JUMP')
    def expr(self, p):
        self.printCode("Jump")

    @_('GETURL2')
    def expr(self, p):
        self.printCode("GetURL2")

    @_('DEFINEFUNC')
    def expr(self, p):
        values = p.DEFINEFUNC
        paramStr = ','.join(map(lambda x: f"{x['register']} \"{x['param']}\"", values['params']))
        self.printCode(f"DefineFunction \"{values['name']}\" {values['paramLength']} {paramStr} {{")

    @_('IF')
    def expr(self, p):
        self.printCode("If")
