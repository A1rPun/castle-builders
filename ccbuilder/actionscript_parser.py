from sly import Parser
from ccbuilder.bytelexer import ByteLexer
from ccbuilder.util import boolToStr
from ccbuilder.funcoption import FuncOption
from ccbuilder.ifoption import IfOption


class ActionScriptParser(Parser):
    tokens = ByteLexer.tokens

    def __init__(self, names: dict = None):
        self.names = names or {}
        self.constantPool = []
        self.stack = []
        self.nesting_level = 0
        self.stackFrame = []
        self.scopes = []
        self.code = ""
        self.switch = False
        self.quux = 0

    def setParams(self, *params):
        self.stackFrame += params

    def getParam(self, register):
        param = None

        for item in self.stackFrame:
            if item['register'] == register:
                param = item['param']
                break

        return param

    def procScope(self, scope):
        if scope['type'] == 'function':
            self.stackFrame = []
            self.nesting_level -= 1
            self.printCode("}")
        if scope['type'] == 'if' or scope['type'] == 'while':
            self.nesting_level -= 1
            self.printCode("}")
        if scope['type'] == 'switch':
            self.nesting_level -= 2
            self.printCode("}")

    def endScope(self, newScope):
        self.quux = newScope
        newScopes = []
        for scope in self.scopes[::-1]:
            if scope['length'] <= newScope:
                self.procScope(scope)
            else:
                newScopes.append(scope)
        self.scopes = newScopes[::-1]

    def setScope(self, newScope):
        self.scopes.append(newScope)

    def error(self, t):
        print(f'[{self}] Illegal character {t}')

    def printCode(self, code):
        # self.code += f"[{str(self.quux).rjust(8, '0')}] " + ("  " * self.nesting_level) + f"{code}" + "\n"
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
        return map(self.parseStructItem, struct)

    @_('expr expr')
    def expr(self, p):
        pass

    @_('END')
    def expr(self, p):
        self.endScope(p.END['offset'])
        # print(f"End byte on {p.END['offset']}")

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
        else:
            self.printCode(f"$$pop();")

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

    @_('DEFINELOCAL')
    def expr(self, p):
        self.endScope(p.DEFINELOCAL['offset'])
        value = self.stack.pop()
        var = self.stack.pop()
        self.printCode(f"var {var} = {value};")

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

    @_('TYPEDADD')
    def expr(self, p):
        self.endScope(p.TYPEDADD['offset'])
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(f"{left} + {right}")

    @_('TYPEDLESSTHAN')
    def expr(self, p):
        values = p.TYPEDLESSTHAN
        self.endScope(values['offset'])
        right = self.stack.pop()
        left = self.stack.pop()
        op = ">=" if values['modifier'] else "<"
        self.stack.append(f"{left} {op} {right}")

    @_('TYPEDEQUAL')
    def expr(self, p):
        values = p.TYPEDEQUAL
        self.endScope(values['offset'])
        right = self.stack.pop()
        left = self.stack.pop()
        op = "!=" if values['modifier'] else "=="
        self.stack.append(f"{left} {op} {right}")

    @_('PUSHDUPLICATE')
    def expr(self, p):
        self.endScope(p.PUSHDUPLICATE['offset'])
        value = self.stack.pop()
        self.stack.append(value)
        self.stack.append(value)

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
        register = p.STORE['value']
        value = self.stack.pop()
        param = self.getParam(register)

        if register == 0 and not p.STORE['modifier']:
            self.printCode(f"switch ({value})")
            self.printCode("{")
            self.nesting_level += 1
            self.switch = True
            self.setParams({'register': register, 'param': value})
        elif param:
            self.printCode(f"{param} = {value};")
        else:
            param = f"_loc{register}_"
            self.printCode(f"var {param} = {value};")
            self.setParams({'register': register, 'param': param})

    @_('DEFINEDICTIONARY')
    def expr(self, p):
        self.endScope(p.DEFINEDICTIONARY['offset'])
        self.constantPool = p.DEFINEDICTIONARY['pool']
        # self.printCode(f"// var ConstantPool = {{ {' '.join(self.constantPool)} }};")

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

        register = 1
        if values['options'] & FuncOption.preload_parent:
            self.setParams({'register': register, 'param': "this"})
            register += 1

        if values['options'] & FuncOption.preload_global:
            self.setParams({'register': register, 'param': "_root"})

        self.setParams(*values['params'])
        self.setScope({
            'type': 'function',
            'offset': values['offset'],
            'length': values['offset'] + values['length'],
        })
        self.nesting_level += 1

    @_('PUSH')
    def expr(self, p):
        self.endScope(p.PUSH['offset'])
        self.stack += self.parseStruct(p.PUSH['value'])

    @_('JUMP')
    def expr(self, p):
        values = p.JUMP
        offset = values['offset']
        bloatedScopes = self.scopes[::-1]
        self.quux = offset

        for i in range(0, len(bloatedScopes)):
            scope = bloatedScopes[i]

            if scope['type'] == 'switch' and offset == scope['length']:
                scope['length'] = offset + values['length']
                self.printCode("break;")  # TODO: fix switch with only default
                self.nesting_level -= 1
                self.printCode("default:")
                self.nesting_level += 1
            elif scope['type'] == 'case' and offset == scope['length']:
                if not self.switch:
                    self.printCode("break;")
                    self.nesting_level -= 1

                self.printCode(f"case {scope['case']}:")
                self.nesting_level += 1
            elif scope['type'] == 'if':
                # if len(self.stack) > 0:
                #     val = self.stack.pop()
                #     self.printCode(f"? {val} : ")
                # else:

                if offset == scope['length']:
                    scope['length'] += values['length']
                    if values['modifier']:
                        self.ifElseIf = True
                    else:
                        self.nesting_level -= 1
                        self.printCode("}")
                        self.printCode("else")
                        self.printCode("{")
                        self.nesting_level += 1

        if self.switch:
            self.switch = False
            self.setScope({
                'type': 'switch',
                'offset': offset,
                'length': offset + values['length'],
            })

    @_('GETURL2')
    def expr(self, p):
        self.endScope(p.GETURL2['offset'])
        window = self.stack.pop()
        url = self.stack.pop()
        self.printCode(f"loadMovie({url},{window});")

    @_('DEFINEFUNC')
    def expr(self, p):
        values = p.DEFINEFUNC
        self.endScope(values['offset'])
        paramStr = ','.join(map(lambda x: x['param'], values['params']))
        self.printCode(f"function {values['name']}({paramStr})")
        self.printCode("{")
        self.setParams(*values['params'])
        self.setScope({
            'type': 'function',
            'offset': values['offset'],
            'length': values['offset'] + values['length'],
        })
        self.nesting_level += 1

    @_('IF')
    def expr(self, p):
        values = p.IF
        self.endScope(values['offset'])
        expression = self.stack.pop()
        modifier = values['modifier']
        scope = {
            'offset': values['offset'],
            'length': values['offset'] + values['length'],
        }
        print(modifier)
        if modifier == IfOption.caseStmt:
            self.setScope({
                'type': "case",
                'case': expression,
                **scope,
            })
        elif modifier == IfOption.elseIfStmt:
            self.nesting_level -= 1
            self.printCode("}")
            self.printCode(f"else if ({expression})")
            self.printCode("{")
            self.nesting_level += 1
            # scope?
        elif modifier == IfOption.whileStmt:
            self.printCode(f"while ({expression})")
            self.printCode("{")
            self.nesting_level += 1
            scope['type'] = "while"
            self.setScope(scope)
        else:
            self.printCode(f"if ({expression})")
            self.printCode("{")
            self.nesting_level += 1
            scope['type'] = "if"
            self.setScope(scope)

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
        pas
    s

    @_('CHR')
    def expr(self, p):
        pas
    s

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
