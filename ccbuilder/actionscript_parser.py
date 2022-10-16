from sly import Parser
from ccbuilder.byte_lexer import ByteLexer
from ccbuilder.util import boolToStr, stripQuote
from ccbuilder.funcoption import FuncOption
from ccbuilder.ifoption import IfOption
from ccbuilder.scopeoption import ScopeOption
from ccbuilder.action_get_property import ActionGetProperty


class Code():
    def __init__(self, offset, indent, code):
        self.offset = offset
        self.indent = indent
        self.code = code
        self.value = None

    def text(self, debug):
        nesting = '  ' * self.indent
        if debug:
            return f"[{str(self.offset).rjust(8, '0')}] {nesting}{self.code}"
        else:
            return f"{nesting}{self.code}"


class ActionScriptParser(Parser):
    tokens = ByteLexer.tokens
    # debugfile = 'parser.out'

    def __init__(self, debug=False):
        self.debug = debug
        self.constantPool = []
        self.stack = []
        self.nesting_level = 0
        self.stackFrame = []
        self.labels = []
        self.codes = []
        self.switch = False
        self.justReturned = False
        self.currentOffset = 0

    def setParams(self, *params):
        self.stackFrame += params

    def getParam(self, register):
        param = None

        for item in self.stackFrame:
            if item['register'] == register:
                param = item['param']
                break

        return param

    def endScope(self, offset):
        self.currentOffset = offset
        for i in reversed(range(0, len(self.labels))):
            label = self.labels[i]
            if label['jump'] <= offset:
                self.removeLabel(label, i, offset)

        self.labels = list(filter(lambda x: x['jump'] > offset, self.labels))

    def setLabel(self, offset, jump, opType, value=None):
        self.labels.append({
            'type': opType,
            'offset': offset,
            'jump': jump,
            'value': value,
        })

    def removeLabel(self, label, index, offset):
        labelType = label['type']
        if labelType == ScopeOption.functionEnd:
            self.stackFrame = []
            self.labels = []
            self.nesting_level -= 1
            self.addCode("}")
        elif labelType == ScopeOption.ifEnd:
            self.nesting_level -= 1
            self.addCode("}")
            if index + 1 < len(self.labels) and self.labels[index+1]['type'] == ScopeOption.jumpEnd:
                self.addCode("else", "{")
                self.nesting_level += 1
        elif labelType == ScopeOption.switchEnd:
            lastJump = self.labels[-1]
            if lastJump['type'] == ScopeOption.jumpEnd and not lastJump['jump'] == label['jump']:
                if not self.justReturned:
                    self.addCode("break;")
                    self.nesting_level -= 1
                    self.addCode("default:")
                    self.nesting_level += 1
                label['jump'] = lastJump['jump']
            else:
                self.nesting_level -= 2
                self.addCode("}")
        elif labelType == ScopeOption.caseEnd:
            if self.switch:
                self.switch = False
            elif self.justReturned:
                self.nesting_level -= 1
            else:
                self.addCode("break;")
                self.nesting_level -= 1

            self.addCode(f"case {label['value']}:")
            self.nesting_level += 1
        elif labelType == ScopeOption.jumpEnd:
            inSwitch = False
            for a in self.labels:
                if a['type'] == ScopeOption.switchEnd and a['jump'] == label['jump']:
                    inSwitch = True
            if not inSwitch:
                self.nesting_level -= 1
                self.addCode("}")
        elif labelType == ScopeOption.ternaryEnd:
            expr = self.codes[-3].code[4:-1]
            rhs = self.popStack()
            lhs = self.popStack()
            self.stack.append(f"{expr} ? {lhs} : {rhs}")
            self.codes = self.codes[:-3]
        self.justReturned = False

    def error(self, t):
        print(f'[{self}] Illegal character {t}')

    def addCode(self, *codes):
        for code in codes:
            self.codes.append(
                Code(self.currentOffset, self.nesting_level, code))

    def insertCode(self, offset, *codes):
        insertIndex = 0
        for code in reversed(self.codes):
            if code.offset > offset:
                code.indent += 1
                insertIndex -= 1
            else:
                break
        if insertIndex < 0:
            for code in codes:
                self.codes.insert(insertIndex, Code(
                    offset, self.nesting_level, code))

    def getCode(self):
        return '\n'.join(map(lambda x: x.text(self.debug), self.codes))

    def parseStructItem(self, item):
        if item.type == 'STRING':
            return f"\"{item.value}\""
        elif item.type == 'FLOAT':
            return str(item.value)
        elif item.type == 'NULL':
            return "null"
        elif item.type == 'UNDEFINED':
            return "undefined"
        elif item.type == 'REGISTER':
            return self.getParam(item.value) if item.value > 0 else None
        elif item.type == 'BOOLEAN':
            return boolToStr(item.value)
        elif item.type == 'DOUBLE':
            return str(item.value)
        elif item.type == 'INTEGER':
            return str(item.value)
        elif item.type == 'DICTLOOKUP':
            return self.constantPool[item.value]
            # return f"\"{self.constantPool[item.value]}\""
        elif item.type == 'DICTLOOKUPLARGE':
            return self.constantPool[item.value]
            # return f"\"{self.constantPool[item.value]}\""
        return None

    def popStack(self):
        return self.stack.pop() if len(self.stack) else "$$pop()"

    # TODO: Fix WARNING: shift/reduce conflicts
    @_('expr expr')
    def expr(self, p):
        pass

    @_('END')
    def expr(self, p):
        self.endScope(p.END['offset'])

    @_('SUBSTRACT')
    def expr(self, p):
        self.endScope(p.SUBSTRACT['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        self.stack.append(f"{lhs} - {rhs}")

    @_('MULTIPLY')
    def expr(self, p):
        self.endScope(p.MULTIPLY['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        self.stack.append(f"{lhs} * {rhs}")

    @_('DIVIDE')
    def expr(self, p):
        self.endScope(p.DIVIDE['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        self.stack.append(f"{lhs} / {rhs}")

    @_('AND')
    def expr(self, p):
        self.endScope(p.AND['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        self.stack.append(f"{lhs} and {rhs}")

    @_('OR')
    def expr(self, p):
        self.endScope(p.OR['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        self.stack.append(f"{lhs} or {rhs}")

    @_('NOT')
    def expr(self, p):
        self.endScope(p.NOT['offset'])
        if not p.NOT['value']:
            test = self.popStack()
            self.stack.append(f"!{test}")

    @_('POP')
    def expr(self, p):
        self.endScope(p.POP['offset'])
        self.addCode(f"{self.popStack()};")

    @_('TOINT')
    def expr(self, p):
        self.endScope(p.TOINT['offset'])
        value = self.popStack()
        self.stack.append(f"int({value})")

    @_('GETVAR')
    def expr(self, p):
        self.endScope(p.GETVAR['offset'])
        var = stripQuote(self.popStack())
        self.stack.append(var)

    @_('SETVAR')
    def expr(self, p):
        self.endScope(p.SETVAR['offset'])
        value = self.popStack()
        var = stripQuote(self.popStack())
        # self.stack.append(f"{var} = {value}")
        self.addCode(f"{var} = {value};")

    @_('SETPROP')
    def expr(self, p):
        self.endScope(p.SETPROP['offset'])
        value = self.popStack()
        prop = self.popStack()
        discard = self.popStack()
        self.addCode(f"{ActionGetProperty(int(prop)).name} = {value};")

    @_('REMOVESPRITE')
    def expr(self, p):
        self.endScope(p.REMOVESPRITE['offset'])
        url = self.popStack()
        self.addCode(f"removeMovieClip({url});")

    @_('TRACE')
    def expr(self, p):
        self.endScope(p.TRACE['offset'])
        value = self.popStack()
        self.stack.append(f"trace({value})")

    @_('RANDOM')
    def expr(self, p):
        self.endScope(p.RANDOM['offset'])
        value = self.popStack()
        self.stack.append(f"random({value})")

    @_('GETTIME')
    def expr(self, p):
        self.endScope(p.GETTIME['offset'])
        value = self.popStack()
        self.stack.append(f"getTimer({value})")

    @_('DEFINELOCAL')
    def expr(self, p):
        self.endScope(p.DEFINELOCAL['offset'])
        value = self.popStack()
        var = stripQuote(self.popStack())
        self.addCode(f"var {var} = {value};")

    @_('CALLFUNC')
    def expr(self, p):
        self.endScope(p.CALLFUNC['offset'])
        fn = stripQuote(self.popStack())
        argLength = int(float(self.popStack()))
        args = []
        for i in range(0, argLength):
            args.append(str(self.popStack()))
        self.stack.append(f"{fn}({','.join(args)})")

    @_('RETURN')
    def expr(self, p):
        self.endScope(p.RETURN['offset'])
        value = self.popStack()
        self.justReturned = True
        self.addCode(f"return {value};")

    @_('MODULO')
    def expr(self, p):
        self.endScope(p.MODULO['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        self.stack.append(f"{lhs} % {rhs}")

    @_('NEW')
    def expr(self, p):
        self.endScope(p.NEW['offset'])
        className = stripQuote(self.popStack())
        argLength = int(float(self.popStack()))
        args = []
        for i in range(0, argLength):
            args.append(str(self.popStack()))
        self.stack.append(f"new {className}({','.join(args)})")

    @_('TYPEDADD')
    def expr(self, p):
        self.endScope(p.TYPEDADD['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        self.stack.append(f"{lhs} + {rhs}")

    @_('TYPEDLESSTHAN')
    def expr(self, p):
        values = p.TYPEDLESSTHAN
        self.endScope(values['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        op = ">=" if values['modifier'] else "<"
        self.stack.append(f"{lhs} {op} {rhs}")

    @_('TYPEDEQUAL')
    def expr(self, p):
        values = p.TYPEDEQUAL
        self.endScope(values['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        op = "!=" if values['modifier'] else "=="
        self.stack.append(f"{lhs} {op} {rhs}")

    @_('PUSHDUPLICATE')
    def expr(self, p):
        self.endScope(p.PUSHDUPLICATE['offset'])
        value = self.popStack()
        self.stack.append(value)
        self.stack.append(value)

    @_('GETMEMBER')
    def expr(self, p):
        self.endScope(p.GETMEMBER['offset'])
        member = self.popStack()
        parent = self.popStack()
        # if member[0] == '"':
        #     self.stack.append(f"{parent}[{member}]")
        # else:
        self.stack.append(f"{parent}.{stripQuote(member)}")

    @_('SETMEMBER')
    def expr(self, p):
        self.endScope(p.SETMEMBER['offset'])
        value = self.popStack()
        member = stripQuote(self.popStack())
        obj = self.popStack()
        self.addCode(f"{obj}.{member} = {value};")

    @_('INCREMENT')
    def expr(self, p):
        self.endScope(p.INCREMENT['offset'])
        value = self.popStack()
        self.stack.append(f"{value} + 1")

    @_('DECREMENT')
    def expr(self, p):
        self.endScope(p.DECREMENT['offset'])
        value = self.popStack()
        self.stack.append(f"{value} - 1")

    @_('CALLMETHOD')
    def expr(self, p):
        self.endScope(p.CALLMETHOD['offset'])
        method = stripQuote(self.popStack())
        obj = self.popStack()
        argLength = int(float(self.popStack()))
        args = []
        for i in range(0, argLength):
            args.append(str(self.popStack()))
        self.stack.append(f"{obj}.{method}({','.join(args)})")

    @_('BITAND')
    def expr(self, p):
        self.endScope(p.BITAND['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        self.stack.append(f"{lhs} & {rhs}")

    @_('BITOR')
    def expr(self, p):
        self.endScope(p.BITOR['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        self.stack.append(f"{lhs} | {rhs}")

    @_('BITXOR')
    def expr(self, p):
        self.endScope(p.BITXOR['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        self.stack.append(f"{lhs} ^ {rhs}")

    @_('BITLSHIFT')
    def expr(self, p):
        self.endScope(p.BITLSHIFT['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        self.stack.append(f"{lhs} << {rhs}")

    @_('BITRSHIFT')
    def expr(self, p):
        self.endScope(p.BITRSHIFT['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        self.stack.append(f"{lhs} >> {rhs}")

    @_('BITRSHIFTUNSIGNED')
    def expr(self, p):
        self.endScope(p.BITRSHIFTUNSIGNED['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        self.stack.append(f"{lhs} >>> {rhs}")

    @_('STRICTEQUAL')
    def expr(self, p):
        self.endScope(p.STRICTEQUAL['offset'])

    @_('GREATERTHAN')
    def expr(self, p):
        values = p.GREATERTHAN
        self.endScope(values['offset'])
        rhs = self.popStack()
        lhs = self.popStack()
        op = "<=" if values['modifier'] else ">"
        self.stack.append(f"{lhs} {op} {rhs}")

    @_('UNKNOWN')
    def expr(self, p):
        self.endScope(p.UNKNOWN['offset'])
        # TODO: Invert statements?

    @_('STORE')
    def expr(self, p):
        self.endScope(p.STORE['offset'])
        register = p.STORE['value']
        value = self.popStack()

        if register == 0 and not p.STORE['modifier']:
            self.addCode(f"switch ({value})", "{")
            self.nesting_level += 1
            self.switch = True
            self.setParams({'register': register, 'param': value})
        elif register == 0:
            self.stack.append(value)
        else:
            param = self.getParam(register)
            if param:
                self.stack.append(f"{param} = {value}")
            else:
                param = f"_loc{register}_"
                self.stack.append(f"var {param} = {value}")
                self.setParams({'register': register, 'param': param})

    @_('DEFINEDICTIONARY')
    def expr(self, p):
        self.endScope(p.DEFINEDICTIONARY['offset'])
        self.constantPool = p.DEFINEDICTIONARY['pool']

    @_('GOTOLABEL')
    def expr(self, p):
        self.endScope(p.GOTOLABEL['offset'])
        self.addCode(p)

    @_('DEFINEFUNC2')
    def expr(self, p):
        values = p.DEFINEFUNC2
        self.endScope(values['offset'])
        paramStr = ','.join(map(lambda x: x['param'], values['params']))
        self.addCode(f"function {values['name']}({paramStr})", "{")

        register = 1
        if values['options'] & FuncOption.preload_this:
            self.setParams({'register': register, 'param': "this"})
            register += 1

        if values['options'] & FuncOption.preload_root:
            self.setParams({'register': register, 'param': "_root"})
            register += 1

        self.setParams(*values['params'])
        self.setLabel(values['offset'], values['offset'] +
                      values['length'], ScopeOption.functionEnd)
        self.nesting_level += 1

    @_('PUSH')
    def expr(self, p):
        self.endScope(p.PUSH['offset'])
        for item in p.PUSH['value']:
            value = self.parseStructItem(item)
            if not value == None:
                self.stack.append(value)

    @_('JUMP')
    def expr(self, p):
        values = p.JUMP
        offset = values['offset']
        self.endScope(offset)

        if self.switch:
            self.setLabel(offset, values['jump'], ScopeOption.switchEnd)
        elif len(self.stack) > 0:
            self.setLabel(offset, values['jump'], ScopeOption.ternaryEnd)
        elif values['length'] < 0:
            expr = list(filter(lambda x: x.offset >=
                        values['jump'], self.codes))
            expr[0].code = f"while ({expr[0].code[4:-1]})"
        else:
            self.setLabel(offset, values['jump'], ScopeOption.jumpEnd)

    @_('GETURL2')
    def expr(self, p):
        self.endScope(p.GETURL2['offset'])
        window = self.popStack()
        url = self.popStack()
        self.addCode(f"loadMovie({url},{window});")

    @_('DEFINEFUNC')
    def expr(self, p):
        values = p.DEFINEFUNC
        self.endScope(values['offset'])
        paramStr = ','.join(map(lambda x: x['param'], values['params']))
        self.addCode(f"function {values['name']}({paramStr})", "{")
        self.setParams(*values['params'])
        self.setLabel(values['offset'], values['offset'] +
                      values['length'], ScopeOption.functionEnd)
        self.nesting_level += 1

    @_('IF')
    def expr(self, p):
        values = p.IF
        self.endScope(values['offset'])
        expr = self.popStack()
        modifier = values['modifier']
        option = ScopeOption.ifEnd
        previousLabel = self.labels[-1]

        if previousLabel['type'] == ScopeOption.jumpEnd and previousLabel['jump'] == values['jump']:
            self.codes[-2].code = f"else if ({expr})"
            self.labels.pop()
        elif modifier == IfOption.caseStmt:
            option = ScopeOption.caseEnd
        elif modifier == IfOption.doWhileStmt:
            option = ScopeOption.whileEnd
            self.insertCode(values['jump'], "do", "{")
            self.addCode("}", f"while ({expr});")
        else:
            self.addCode(f"if ({expr})", "{")
            self.nesting_level += 1

        self.setLabel(values['offset'], values['jump'], option, expr)

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
