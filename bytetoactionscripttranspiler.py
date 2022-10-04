from sly import Parser
from bytelexer import ByteLexer


class ActionScriptTranspiler(Parser):
    tokens = ByteLexer.tokens

    def __init__(self, names: dict = None):
        self.names = names or {}
        self.constantPool = []
        self.stack = []
        self.nesting_level = 0
        self.scope = ["_root"]
        self.bytecount = 0

    def setParams(self, *params):
        self.scope += map(lambda x: x['param'], params)

    def error(self, t):
        print(f'[{self}] Illegal character {t}')

    def printCode(self, code):
        print("  " * self.nesting_level + f"{code}")

    def parseStructItem(self, item):
        if item.type == 'STRING':
            self.bytecount += len(item.value)
            return item.value
        elif item.type == 'FLOAT':
            self.bytecount += 5
            return str(item.value)
        elif item.type == 'NULL':
            self.bytecount += 1
            return "null"
        elif item.type == 'REGISTER':
            self.bytecount += 2
            return self.scope[item.value]
        elif item.type == 'BOOLEAN':
            self.bytecount += 2
            return "true" if item.value else "false"
        elif item.type == 'DOUBLE':
            self.bytecount += 9
            return str(item.value)
        elif item.type == 'INTEGER':
            self.bytecount += 5
            return str(item.value)
        elif item.type == 'DICTLOOKUP':
            self.bytecount += 2
            return self.constantPool[item.value]
        elif item.type == 'DICTLOOKUPLARGE':
            self.bytecount += 3
            return self.constantPool[item.value]
        return "undefined"

    def parseStruct(self, struct):
        return map(self.parseStructItem, struct)

    @_('expr expr')
    def expr(self, p):
        pass

    @_('END')
    def expr(self, p):
        self.bytecount += 1
        self.printCode("}")

    @_('SUBSTRACT')
    def expr(self, p):
        self.bytecount += 1
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} - {right}")

    @_('MULTIPLY')
    def expr(self, p):
        self.bytecount += 1
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} * {right}")

    @_('DIVIDE')
    def expr(self, p):
        self.bytecount += 1
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} / {right}")

    @_('AND')
    def expr(self, p):
        self.bytecount += 1
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} && {right}")

    @_('OR')
    def expr(self, p):
        self.bytecount += 1
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} || {right}")

    @_('NOT')
    def expr(self, p):
        self.bytecount += 1
        pass
        # TODO: Fix greater not etc.
        # self.printCode("!")

    @_('POP')
    def expr(self, p):
        self.bytecount += 1
        if len(self.stack) > 0:
            popped = self.stack.pop()
            self.printCode(popped)

    @_('TOINT')
    def expr(self, p):
        self.bytecount += 1
        value = self.stack.pop()
        self.stack.append(f"int({value})")

    @_('GETVAR')
    def expr(self, p):
        self.bytecount += 1
        # more?

    @_('SETVAR')
    def expr(self, p):
        self.bytecount += 1
        var = self.stack.pop()
        value = self.stack.pop()
        self.printCode(f"{var} = {value};")

    @_('SETPROP')
    def expr(self, p):
        self.bytecount += 1
        prop = self.stack.pop()
        value = self.stack.pop()
        self.printCode(f"{prop} = {value};")

    @_('REMOVESPRITE')
    def expr(self, p):
        self.bytecount += 1
        self.printCode("RemoveSprite")

    @_('TRACE')
    def expr(self, p):
        self.bytecount += 1
        value = self.stack.pop()
        self.stack.append(f"trace({value})")

    @_('RANDOM')
    def expr(self, p):
        self.bytecount += 1
        value = self.stack.pop()
        self.stack.append(f"random({value})")

    @_('GETTIME')
    def expr(self, p):
        self.bytecount += 1
        value = self.stack.pop()
        self.stack.append(f"GetTime({value})")

    @_('CALLFUNC')
    def expr(self, p):
        # self.bytecount += 1
        fn = self.stack.pop()
        argLength = self.stack.pop()
        args = self.stack
        self.stack = []  # TODO
        self.stack.append(f"{fn}({', '.join(args[::-1])})")
        # TODO PRINT IF NO RESULT

    @_('RETURN')
    def expr(self, p):
        self.bytecount += 1
        self.printCode("return")

    @_('MODULO')
    def expr(self, p):
        self.bytecount += 1
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} % {right}")

    @_('NEW')
    def expr(self, p):
        self.bytecount += 1
        self.printCode("new")

    @_('ADD2')
    def expr(self, p):
        self.bytecount += 1
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} + {right}")

    @_('LESSTHAN')
    def expr(self, p):
        self.bytecount += 1
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} < {right}")

    @_('EQUALS')
    def expr(self, p):
        self.bytecount += 1
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} == {right}")

    @_('PUSHDUPLICATE')
    def expr(self, p):
        self.bytecount += 1
        self.printCode("??")

    @_('GETMEMBER')
    def expr(self, p):
        self.bytecount += 1
        member = self.stack.pop()
        parent = self.stack.pop()
        self.stack.append(f"{parent}.{member}")

    @_('SETMEMBER')
    def expr(self, p):
        self.bytecount += 1
        value = self.stack.pop()
        members = self.stack
        self.stack = []  # TODO
        self.printCode(f"{'.'.join(members)} = {value};")

    @_('INCREMENT')
    def expr(self, p):
        self.bytecount += 1
        value = self.stack.pop()
        self.stack.append(f"{value} + 1")

    @_('DECREMENT')
    def expr(self, p):
        self.bytecount += 1
        value = self.stack.pop()
        self.stack.append(f"{value} - 1")

    @_('CALLMETHOD')
    def expr(self, p):
        self.bytecount += 1
        # self.printCode(self.stack)
        fn = self.stack.pop()
        obj = self.stack.pop()
        argLength = self.stack.pop()
        args = self.stack
        self.stack = []  # TODO
        self.stack.append(f"{obj}.{fn}({', '.join(args[::-1])});")
        # TODO PRINT IF NO RESULT

    @_('BITAND')
    def expr(self, p):
        self.bytecount += 1
        self.printCode("&")

    @_('BITOR')
    def expr(self, p):
        self.bytecount += 1
        self.printCode("|")

    @_('BITXOR')
    def expr(self, p):
        self.bytecount += 1
        self.printCode("^")

    @_('BITLSHIFT')
    def expr(self, p):
        self.bytecount += 1
        self.printCode("<<")

    @_('BITRSHIFT')
    def expr(self, p):
        self.bytecount += 1
        self.printCode(">>")

    @_('BITRSHIFTUNSIGNED')
    def expr(self, p):
        self.bytecount += 1
        self.printCode(">>>")

    @_('STRICTEQUAL')
    def expr(self, p):
        self.bytecount += 1
        self.printCode("==")

    @_('GREATERTHAN')
    def expr(self, p):
        self.bytecount += 1
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} > {right}")

    @_('UNKNOWN')
    def expr(self, p):
        self.bytecount += 1
        self.printCode("YESYESFULP")

    @_('STORE')
    def expr(self, p):
        self.bytecount += 1
        value = self.stack.pop()
        param = f"_loc{p.STORE}_"
        self.printCode(f"var {param} = {value};")
        self.setParams({'register': p.STORE, 'param': param})

    @_('DEFINEDICTIONARY')
    def expr(self, p):
        # self.bytecount += 1
        self.constantPool = p.DEFINEDICTIONARY
        # TODO REMOVE DEV RESTRICTION [:10]
        # self.printCode("var ConstantPool = { %s };" % ','.join(self.constantPool))
        self.printCode(
            f"var ConstantPool = {{ {', '.join(self.constantPool[:5])} , ... }};")

    @_('GOTOLABEL')
    def expr(self, p):
        # self.bytecount += 1
        self.printCode(p)

    @_('DEFINEFUNC2')
    def expr(self, p):
        # self.bytecount += 1
        values = p.DEFINEFUNC2
        paramStr = ','.join(map(lambda x: x['param'], values['params']))
        self.printCode(f"function {values['name']}({paramStr}) {{")
        self.setParams(*values['params'])
        self.nesting_level += 1

    @_('PUSH')
    def expr(self, p):
        self.bytecount += 1
        self.stack += self.parseStruct(p.PUSH)

    @_('JUMP')
    def expr(self, p):
        self.bytecount += 1
        self.printCode("jump")

    @_('GETURL2')
    def expr(self, p):
        self.bytecount += 1
        self.printCode("loadMovie()")

    @_('DEFINEFUNC')
    def expr(self, p):
        # self.bytecount += 1
        values = p.DEFINEFUNC2
        paramStr = ','.join(map(lambda x: x['param'], values['params']))
        self.printCode(f"function {values['name']}({paramStr}) {{")
        self.setParams(*values['params'])
        self.nesting_level += 1

    @_('IF')
    def expr(self, p):
        self.bytecount += 5
        expression = self.stack.pop()
        self.printCode("if (%s) {" % expression)
        self.nesting_level += 1
