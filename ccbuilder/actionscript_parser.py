from sly import Parser
from ccbuilder.bytelexer import ByteLexer


class ActionScriptParser(Parser):
    tokens = ByteLexer.tokens

    def __init__(self, names: dict = None):
        self.names = names or {}
        self.constantPool = []
        self.stack = []
        self.nesting_level = 0
        self.register = []
        self.scopes = []
        self.bytecount = 0
        self.code = ""

    def setParams(self, *params):
        self.register += params

    def getParam(self, register):
        param = "_root"

        for item in self.register:
            if item['register'] == register:
                param = item['param']
                break

        return param

    def endScope(self, newScope):
        newScopes = []
        for scope in self.scopes:
            if scope <= newScope:
                self.nesting_level -= 1
                self.printCode("}")
            else:
                newScopes.append(scope)
        self.scopes = newScopes

    def setScope(self, newScope):
        self.scopes.append(newScope)
        self.nesting_level += 1

    def error(self, t):
        print(f'[{self}] Illegal character {t}')

    def printCode(self, code):
        self.code += "  " * self.nesting_level + f"{code}" + "\n"
        # print("   " * self.nesting_level + f"{code}")

    def parseStructItem(self, item):
        if item.type == 'STRING':
            return f"\"{item.value}\""
        elif item.type == 'FLOAT':
            return str(item.value)
        elif item.type == 'NULL':
            return "null"
        elif item.type == 'REGISTER':
            return self.getParam(item.value)
        elif item.type == 'BOOLEAN':
            return "true" if item.value else "false"
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
        return map(self.parseStructItem, struct)

    @_('expr expr')
    def expr(self, p):
        pass

    @_('END')
    def expr(self, p):
        self.endScope(p.END['offset'])

    @_('SUBSTRACT')
    def expr(self, p):
        self.endScope(p.SUBSTRACT['offset'])
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} - {right}")

    @_('MULTIPLY')
    def expr(self, p):
        self.endScope(p.MULTIPLY['offset'])
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} * {right}")

    @_('DIVIDE')
    def expr(self, p):
        self.endScope(p.DIVIDE['offset'])
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} / {right}")

    @_('AND')
    def expr(self, p):
        self.endScope(p.AND['offset'])
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} && {right}")

    @_('OR')
    def expr(self, p):
        self.endScope(p.OR['offset'])
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} || {right}")

    @_('NOT')
    def expr(self, p):
        self.endScope(p.NOT['offset'])
        test = self.stack.pop()
        self.stack.append(f"!{test}")
        # TODO: Not doesnt always fits the context so make it context aware

    @_('POP')
    def expr(self, p):
        self.endScope(p.POP['offset'])
        if len(self.stack) > 0:
            self.printCode(f"{self.stack.pop()};")

    @_('TOINT')
    def expr(self, p):
        self.endScope(p.TOINT['offset'])
        value = self.stack.pop()
        self.stack.append(f"int({value})")

    @_('GETVAR')
    def expr(self, p):
        self.endScope(p.GETVAR['offset'])

    @_('SETVAR')
    def expr(self, p):
        self.endScope(p.SETVAR['offset'])
        value = self.stack.pop()
        var = self.stack.pop()
        self.printCode(f"{var} = {value};")

    @_('SETPROP')
    def expr(self, p):
        self.endScope(p.SETPROP['offset'])
        prop = self.stack.pop()
        value = self.stack.pop()
        self.printCode(f"{prop} = {value};")

    @_('REMOVESPRITE')
    def expr(self, p):
        self.endScope(p.REMOVESPRITE['offset'])
        self.printCode("RemoveSprite")

    @_('TRACE')
    def expr(self, p):
        self.endScope(p.TRACE['offset'])
        value = self.stack.pop()
        self.stack.append(f"trace({value})")

    @_('RANDOM')
    def expr(self, p):
        self.endScope(p.RANDOM['offset'])
        value = self.stack.pop()
        self.stack.append(f"random({value})")

    @_('GETTIME')
    def expr(self, p):
        self.endScope(p.GETTIME['offset'])
        value = self.stack.pop()
        self.stack.append(f"GetTime({value})")

    @_('CALLFUNC')
    def expr(self, p):
        self.endScope(p.CALLFUNC['offset'])
        fn = self.stack.pop()
        argLength = int(float(self.stack.pop()))
        args = []
        for i in range(0, argLength):
            args.append(self.stack.pop())
        self.stack.append(f"{fn}({','.join(args[::-1])})")

    @_('RETURN')
    def expr(self, p):
        self.endScope(p.RETURN['offset'])
        value = self.stack.pop()
        self.printCode(f"return {value};")

    @_('MODULO')
    def expr(self, p):
        self.endScope(p.MODULO['offset'])
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} % {right}")

    @_('NEW')
    def expr(self, p):
        self.endScope(p.NEW['offset'])
        className = self.stack.pop()
        argLength = int(float(self.stack.pop()))
        args = []
        for i in range(0, argLength):
            args.append(self.stack.pop())
        self.stack.append(f"new {className}({','.join(args)})")

    @_('ADD2')
    def expr(self, p):
        self.endScope(p.ADD2['offset'])
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} + {right}")

    @_('LESSTHAN')
    def expr(self, p):
        values = p.LESSTHAN
        self.endScope(values['offset'])
        right = self.stack.pop()
        left = self.stack.pop()
        op = ">=" if values['modifier'] else "<"
        self.stack.append(f"{left} {op} {right}")

    @_('EQUALS')
    def expr(self, p):
        values = p.EQUALS
        self.endScope(values['offset'])
        right = self.stack.pop()
        left = self.stack.pop()
        op = "!=" if values['modifier'] else "=="
        self.stack.append(f"{left} {op} {right}")

    @_('PUSHDUPLICATE')
    def expr(self, p):
        self.endScope(p.PUSHDUPLICATE['offset'])
        self.printCode("??")

    @_('GETMEMBER')
    def expr(self, p):
        self.endScope(p.GETMEMBER['offset'])
        member = self.stack.pop()
        parent = self.stack.pop()
        self.stack.append(f"{parent}.{member}")
        # TODO: if member is string = parent[member]
        # self.stack.append(f"{parent}[{member}]")

    @_('SETMEMBER')
    def expr(self, p):
        self.endScope(p.SETMEMBER['offset'])
        value = self.stack.pop()
        members = self.stack
        self.stack = []  # TODO
        self.printCode(f"{'.'.join(members)} = {value};")

    @_('INCREMENT')
    def expr(self, p):
        self.endScope(p.INCREMENT['offset'])
        value = self.stack.pop()
        self.stack.append(f"{value} + 1")

    @_('DECREMENT')
    def expr(self, p):
        self.endScope(p.DECREMENT['offset'])
        value = self.stack.pop()
        self.stack.append(f"{value} - 1")

    @_('CALLMETHOD')
    def expr(self, p):
        self.endScope(p.CALLMETHOD['offset'])
        fn = self.stack.pop()
        obj = self.stack.pop()
        argLength = int(float(self.stack.pop()))
        args = []
        for i in range(0, argLength):
            args.append(self.stack.pop())
        self.stack.append(f"{obj}.{fn}({','.join(args[::-1])})")

    @_('BITAND')
    def expr(self, p):
        self.endScope(p.BITAND['offset'])
        self.printCode("&")

    @_('BITOR')
    def expr(self, p):
        self.endScope(p.BITOR['offset'])
        self.printCode("|")

    @_('BITXOR')
    def expr(self, p):
        self.endScope(p.BITXOR['offset'])
        self.printCode("^")

    @_('BITLSHIFT')
    def expr(self, p):
        self.endScope(p.BITLSHIFT['offset'])
        self.printCode("<<")

    @_('BITRSHIFT')
    def expr(self, p):
        self.endScope(p.BITRSHIFT['offset'])
        self.printCode(">>")

    @_('BITRSHIFTUNSIGNED')
    def expr(self, p):
        self.endScope(p.BITRSHIFTUNSIGNED['offset'])
        self.printCode(">>>")

    @_('STRICTEQUAL')
    def expr(self, p):
        self.endScope(p.STRICTEQUAL['offset'])
        self.printCode("==")

    @_('GREATERTHAN')
    def expr(self, p):
        values = p.GREATERTHAN
        self.endScope(values['offset'])
        right = self.stack.pop()
        left = self.stack.pop()
        op = "<=" if values['modifier'] else ">"
        self.stack.append(f"{left} {op} {right}")

    @_('UNKNOWN')
    def expr(self, p):
        self.endScope(p.UNKNOWN['offset'])
        # TODO: Invert statements?

    @_('STORE')
    def expr(self, p):
        self.endScope(p.STORE['offset'])
        value = self.stack.pop()
        param = f"_loc{p.STORE['value']}_"
        self.printCode(f"var {param} = {value};")
        self.setParams({'register': p.STORE['value'], 'param': param})

    @_('DEFINEDICTIONARY')
    def expr(self, p):
        self.endScope(p.DEFINEDICTIONARY['offset'])
        self.constantPool = p.DEFINEDICTIONARY['pool']
        if len(self.constantPool) > 0:
            self.printCode(
                f"// var ConstantPool = {{ {', '.join(self.constantPool)} , ... }};")

    @_('GOTOLABEL')
    def expr(self, p):
        self.endScope(p.GOTOLABEL['offset'])
        self.printCode(p)

    @_('DEFINEFUNC2')
    def expr(self, p):
        values = p.DEFINEFUNC2
        self.endScope(values['offset'])
        paramStr = ','.join(map(lambda x: x['param'], values['params']))
        self.printCode(f"function {values['name']}({paramStr})")
        self.printCode("{")
        self.setParams(*values['params'])
        self.setScope(values['offset'] + values['functionLength'])

    @_('PUSH')
    def expr(self, p):
        self.endScope(p.PUSH['offset'])
        self.stack += self.parseStruct(p.PUSH['value'])

    @_('JUMP')
    def expr(self, p):
        self.endScope(p.JUMP['offset'])
        self.printCode("jump")

    @_('GETURL2')
    def expr(self, p):
        self.endScope(p.GETURL2['offset'])
        window = self.stack.pop()
        url = self.stack.pop()
        self.printCode(f"loadMovie(\"{url}\",{window});")

    @_('DEFINEFUNC')
    def expr(self, p):
        values = p.DEFINEFUNC
        self.endScope(values['offset'])
        paramStr = ','.join(map(lambda x: x['param'], values['params']))
        self.printCode(f"function {values['name']}({paramStr})")
        self.printCode("{")
        self.setParams(*values['params'])
        self.setScope(values['offset'] + values['functionLength'])

    @_('IF')
    def expr(self, p):
        values = p.IF
        self.endScope(values['offset'])
        expression = self.stack.pop()
        self.printCode(f"if ({expression})")
        self.printCode("{")
        self.setScope(values['offset'] + values['value'])
