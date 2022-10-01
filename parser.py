from sly import Parser
from lexer import CCByteLexer


class CCByteParser(Parser):
    tokens = CCByteLexer.tokens

    def __init__(self, names: dict = None):
        self.names = names or {}
        self.stack = []

    @property
    def last_item_on_stack(self):
        return self.stack[-1] if len(self.stack) > 0 else None

    @_('END')
    def statement(self, p):
        print("}")

    @_('UNDEFINED')
    def statement(self, p):
        print("undefined")

    @_('BOOLEAN')
    def statement(self, p):
        print("true")

    @_('REGISTER')
    def statement(self, p):
        print("register")

    @_('PROPERTY')
    def statement(self, p):
        print("Prop??")

    @_('FLOAT')
    def statement(self, p):
        print("Float")

    @_('NUMBER')
    def statement(self, p):
        print("Number")

    @_('CONSTANT')
    def statement(self, p):
        print("Constant??")

    @_('AND')
    def statement(self, p):
        print("&&")

    @_('OR')
    def statement(self, p):
        print("||")

    @_('SUBSTRACT')
    def statement(self, p):
        print("-")

    @_('MULTIPLY')
    def statement(self, p):
        print("*")

    @_('DIVIDE')
    def statement(self, p):
        print("/")

    @_('NOT')
    def statement(self, p):
        print("!")

    @_('POP')
    def statement(self, p):
        print("pop")

    @_('TOINT')
    def statement(self, p):
        print("ToInteger")

    @_('GETVAR')
    def statement(self, p):
        print("GetVariable")

    @_('SETVAR')
    def statement(self, p):
        print("SetVariable")

    @_('SETPROP')
    def statement(self, p):
        print("SetProperty")

    @_('REMOVESPRITE')
    def statement(self, p):
        print("RemoveSprite")

    @_('TRACE')
    def statement(self, p):
        print("Trace")

    @_('RANDOM')
    def statement(self, p):
        print("Random")

    @_('GETTIME')
    def statement(self, p):
        print("GetTime")

    @_('CALLFUNC')
    def statement(self, p):
        print("()")

    @_('RETURN')
    def statement(self, p):
        print("return")

    @_('MODULO')
    def statement(self, p):
        print("%")

    @_('NEW')
    def statement(self, p):
        print("new")

    @_('ADD2')
    def statement(self, p):
        print("+")

    @_('LESSTHAN')
    def statement(self, p):
        print("<")

    @_('EQUALS')
    def statement(self, p):
        print("==")

    @_('PUSHDUPLICATE')
    def statement(self, p):
        print("??")

    @_('GETMEMBER')
    def statement(self, p):
        print("GetMember")

    @_('SETMEMBER')
    def statement(self, p):
        print("SetMember")

    @_('INCREMENT')
    def statement(self, p):
        print("++")

    @_('DECREMENT')
    def statement(self, p):
        print("--")

    @_('CALLMETHOD')
    def statement(self, p):
        print("()")

    @_('BITAND')
    def statement(self, p):
        print("&")

    @_('BITOR')
    def statement(self, p):
        print("|")

    @_('BITXOR')
    def statement(self, p):
        print("^")

    @_('BITLSHIFT')
    def statement(self, p):
        print("<<")

    @_('BITRSHIFT')
    def statement(self, p):
        print(">>")

    @_('BITRSHIFTUNSIGNED')
    def statement(self, p):
        print(">>>")

    @_('STRICTEQUAL')
    def statement(self, p):
        print("==")

    @_('GREATERTHAN')
    def statement(self, p):
        print(">")

    @_('UNKNOWN')
    def statement(self, p):
        print("YESYESFULP")

    @_('STORE')
    def statement(self, p):
        print("StoreRegister")

    @_('DEFINEDICTIONARY')
    def statement(self, p):
        print("var ContantPool = {};")

    @_('GOTOLABEL')
    def statement(self, p):
        print(p)

    @_('DEFINEFUNCV7')
    def statement(self, p):
        print("function () {")

    @_('PUSH')
    def statement(self, p):
        print("push")

    @_('JUMP')
    def statement(self, p):
        print("jump")

    @_('GETURL2')
    def statement(self, p):
        print("GETURL2")

    @_('DEFINEFUNC')
    def statement(self, p):
        print("function () {")

    @_('IF')
    def statement(self, p):
        print("if")
