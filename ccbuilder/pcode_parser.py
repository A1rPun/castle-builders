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

    @_('DEFINELOCAL')
    def expr(self, p):
        self.printCode("DefineLocal")

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

    @_('TYPEDADD')
    def expr(self, p):
        self.printCode("TYPEDADD")

    @_('TYPEDLESSTHAN')
    def expr(self, p):
        self.printCode("Less2")

    @_('TYPEDEQUAL')
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
        self.constantPool = list(
            map(lambda x: f"\"{x}\"", p.DEFINEDICTIONARY['pool']))
        # self.printCode(f"ConstantPool {' '.join(self.constantPool)}")

    @_('GOTOLABEL')
    def expr(self, p):
        self.printCode("GoToLabel")

    @_('DEFINEFUNC2')
    def expr(self, p):
        values = p.DEFINEFUNC2
        paramStr = ','.join(
            map(lambda x: f"{x['register']} \"{x['param']}\"", values['params']))
        options = values['options']
        optionStr = ""
        for op in (FuncOption):
            optionStr += f"{boolToStr(options & op.value)} "
        optionStr += "false"
        self.printCode(
            f"DefineFunction2 \"{values['name']}\" {values['paramLength']} {values['regCount']} {optionStr} {paramStr} {{")

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
        paramStr = ','.join(
            map(lambda x: f"{x['register']} \"{x['param']}\"", values['params']))
        self.printCode(
            f"DefineFunction \"{values['name']}\" {values['paramLength']} {paramStr} {{")

    @_('IF')
    def expr(self, p):
        self.printCode("If")

    @_('ADD')
    def expr(self, p):
        pass

    @_('EQUAL')
    def expr(self, p):
        pass

    @_('LESSTHAN')
    def expr(self, p):
        pass

    @_('NEXTFRAME')
    def expr(self, p):
        pass

    @_('PREVIOUSFRAME')
    def expr(self, p):
        pass

    @_('PLAY')
    def expr(self, p):
        pass

    @_('STOP')
    def expr(self, p):
        pass

    @_('TOGGLEQUALITY')
    def expr(self, p):
        pass

    @_('STOPSOUND')
    def expr(self, p):
        pass

    @_('STRINGEQUAL')
    def expr(self, p):
        pass

    @_('STRINGLENGTH')
    def expr(self, p):
        pass

    @_('SUBSTRING')
    def expr(self, p):
        pass

    @_('SETTARGETDYNAMIC')
    def expr(self, p):
        pass

    @_('STRINGCONCAT')
    def expr(self, p):
        pass

    @_('GETPROP')
    def expr(self, p):
        pass

    @_('DUPLICATESPRITE')
    def expr(self, p):
        pass

    @_('STARTDRAG')
    def expr(self, p):
        pass

    @_('STOPDRAG')
    def expr(self, p):
        pass

    @_('STRINGLESSTHAN')
    def expr(self, p):
        pass

    @_('THROW')
    def expr(self, p):
        pass

    @_('CASTOBJ')
    def expr(self, p):
        pass

    @_('IMPLEMENTS')
    def expr(self, p):
        pass

    @_('STRINGLENGTH2')
    def expr(self, p):
        pass

    @_('ORD')
    def expr(self, p):
        pass

    @_('CHR')
    def expr(self, p):
        pass

    @_('SUBSTRING2')
    def expr(self, p):
        pass

    @_('ORD2')
    def expr(self, p):
        pass

    @_('CHR2')
    def expr(self, p):
        pass

    @_('DELETE')
    def expr(self, p):
        pass

    @_('DELETEALL')
    def expr(self, p):
        pass

    @_('DECLARELOCAL')
    def expr(self, p):
        pass

    @_('DECLAREARRAY')
    def expr(self, p):
        pass

    @_('DECLAREOBJECT')
    def expr(self, p):
        pass

    @_('TYPEOF')
    def expr(self, p):
        pass

    @_('TARGETOF')
    def expr(self, p):
        pass

    @_('ENUMERATE')
    def expr(self, p):
        pass

    @_('VALUEOF')
    def expr(self, p):
        pass

    @_('TOSTRING')
    def expr(self, p):
        pass

    @_('SWAP')
    def expr(self, p):
        pass

    @_('NEWMETHOD')
    def expr(self, p):
        pass

    @_('INSTANCEOF')
    def expr(self, p):
        pass

    @_('ENUMERATEOBJECT')
    def expr(self, p):
        pass

    @_('STRINGGREATERTHAN')
    def expr(self, p):
        pass

    @_('EXTENDS')
    def expr(self, p):
        pass

    @_('GOTOFRAME')
    def expr(self, p):
        pass

    @_('GETURL')
    def expr(self, p):
        pass

    @_('WAITFORFRAME')
    def expr(self, p):
        pass

    @_('SETTARGET')
    def expr(self, p):
        pass

    @_('WAITFORFRAMEDYNAMIC')
    def expr(self, p):
        pass

    @_('TRY')
    def expr(self, p):
        pass

    @_('WITH')
    def expr(self, p):
        pass

    @_('CALLFRAME')
    def expr(self, p):
        pass

    @_('GOTO')
    def expr(self, p):
        pass
