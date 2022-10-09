from ccbuilder.baselexer import BaseLexer
from ccbuilder.util import splitBytes, byteArrayToString, hexToInt, splitBytesOn, unsignedToSigned
from ccbuilder.structlexer import StructLexer
from ccbuilder.funcoption import FuncOption
from ccbuilder.ifoption import IfOption


class ByteLexer(BaseLexer):
    tokens = {
        END, NEXTFRAME, PREVIOUSFRAME, PLAY, STOP, TOGGLEQUALITY, STOPSOUND,
        ADD, SUBSTRACT, MULTIPLY, DIVIDE, EQUAL, LESSTHAN, AND, OR, NOT,
        STRINGEQUAL, STRINGLENGTH, SUBSTRING, POP, TOINT, GETVAR, SETVAR,
        SETTARGETDYNAMIC, STRINGCONCAT, GETPROP, SETPROP, DUPLICATESPRITE,
        REMOVESPRITE, TRACE, STARTDRAG, STOPDRAG, STRINGLESSTHAN, THROW,
        CASTOBJ, IMPLEMENTS, RANDOM, STRINGLENGTH2, ORD, CHR, GETTIME,
        SUBSTRING2, ORD2, CHR2, DELETE, DELETEALL, DEFINELOCAL, CALLFUNC,
        RETURN, MODULO, NEW, DECLARELOCAL, DECLAREARRAY, DECLAREOBJECT, TYPEOF,
        TARGETOF, ENUMERATE, TYPEDADD, TYPEDLESSTHAN, TYPEDEQUAL, VALUEOF,
        TOSTRING, PUSHDUPLICATE, SWAP, GETMEMBER, SETMEMBER, INCREMENT,
        DECREMENT, CALLMETHOD, NEWMETHOD, INSTANCEOF, ENUMERATEOBJECT, BITAND,
        BITOR, BITXOR, BITLSHIFT, BITRSHIFT, BITRSHIFTUNSIGNED, STRICTEQUAL,
        GREATERTHAN, STRINGGREATERTHAN, EXTENDS, UNKNOWN, GOTOFRAME, GETURL,
        STORE, DEFINEDICTIONARY, WAITFORFRAME, SETTARGET, GOTOLABEL,
        WAITFORFRAMEDYNAMIC, DEFINEFUNC2, TRY, WITH, PUSH, JUMP, GETURL2,
        DEFINEFUNC, IF, CALLFRAME, GOTO
    }

    def getValues(self, values):
        lexer = StructLexer()
        lexed = lexer.tokenize(' '.join(values))
        return lexed

    @_(r"00")
    def END(self, t):
        return self.defaultValue(t)

    @_(r"04")
    def NEXTFRAME(self, t):
        return self.defaultValue(t)

    @_(r"05")
    def PREVIOUSFRAME(self, t):
        return self.defaultValue(t)

    @_(r"06")
    def PLAY(self, t):
        return self.defaultValue(t)

    @_(r"07")
    def STOP(self, t):
        return self.defaultValue(t)

    @_(r"08")
    def TOGGLEQUALITY(self, t):
        return self.defaultValue(t)

    @_(r"09")
    def STOPSOUND(self, t):
        return self.defaultValue(t)

    @_(r"0[a|A]")
    def ADD(self, t):
        return self.defaultValue(t)

    @_(r"0[b|B]")
    def SUBSTRACT(self, t):
        return self.defaultValue(t)

    @_(r"0[c|C]")
    def MULTIPLY(self, t):
        return self.defaultValue(t)

    @_(r"0[d|D]")
    def DIVIDE(self, t):
        return self.defaultValue(t)

    @_(r"0[e|E]")
    def EQUAL(self, t):
        return self.defaultValue(t)

    @_(r"0[f|F]")
    def LESSTHAN(self, t):
        return self.defaultValue(t)

    @_(r"10")
    def AND(self, t):
        return self.defaultValue(t)

    @_(r"11")
    def OR(self, t):
        return self.defaultValue(t)

    @_(r"12")
    def NOT(self, t):
        offset = self.getOffset()
        isFromIf = self.findBytes(0, 1, " 9d")
        t.value = {
            'offset': offset,
            'value': bool(isFromIf),
        }
        return t

    @_(r"13")
    def STRINGEQUAL(self, t):
        return self.defaultValue(t)

    @_(r"14")
    def STRINGLENGTH(self, t):
        return self.defaultValue(t)

    @_(r"15")
    def SUBSTRING(self, t):
        return self.defaultValue(t)

    @_(r"17")
    def POP(self, t):
        return self.defaultValue(t)

    @_(r"18")
    def TOINT(self, t):
        return self.defaultValue(t)

    @_(r"1[c|C]")
    def GETVAR(self, t):
        return self.defaultValue(t)

    @_(r"1[d|D]")
    def SETVAR(self, t):
        return self.defaultValue(t)

    @_(r"20")
    def SETTARGETDYNAMIC(self, t):
        return self.defaultValue(t)

    @_(r"21")
    def STRINGCONCAT(self, t):
        return self.defaultValue(t)

    @_(r"22")
    def GETPROP(self, t):
        return self.defaultValue(t)

    @_(r"23")
    def SETPROP(self, t):
        return self.defaultValue(t)

    @_(r"24")
    def DUPLICATESPRITE(self, t):
        return self.defaultValue(t)

    @_(r"25")
    def REMOVESPRITE(self, t):
        return self.defaultValue(t)

    @_(r"26")
    def TRACE(self, t):
        return self.defaultValue(t)

    @_(r"27")
    def STARTDRAG(self, t):
        return self.defaultValue(t)

    @_(r"28")
    def STOPDRAG(self, t):
        return self.defaultValue(t)

    @_(r"29")
    def STRINGLESSTHAN(self, t):
        return self.defaultValue(t)

    @_(r"2[a|A]")
    def THROW(self, t):
        return self.defaultValue(t)

    @_(r"2[b|B]")
    def CASTOBJ(self, t):
        return self.defaultValue(t)

    @_(r"2[c|C]")
    def IMPLEMENTS(self, t):
        return self.defaultValue(t)

    @_(r"30")
    def RANDOM(self, t):
        return self.defaultValue(t)

    @_(r"31")
    def STRINGLENGTH2(self, t):
        return self.defaultValue(t)

    @_(r"32")
    def ORD(self, t):
        return self.defaultValue(t)

    @_(r"33")
    def CHR(self, t):
        return self.defaultValue(t)

    @_(r"34")
    def GETTIME(self, t):
        return self.defaultValue(t)

    @_(r"35")
    def SUBSTRING2(self, t):
        return self.defaultValue(t)

    @_(r"36")
    def ORD2(self, t):
        return self.defaultValue(t)

    @_(r"37")
    def CHR2(self, t):
        return self.defaultValue(t)

    @_(r"3[a|A]")
    def DELETE(self, t):
        return self.defaultValue(t)

    @_(r"3[b|B]")
    def DELETEALL(self, t):
        return self.defaultValue(t)

    @_(r"3[c|C]")
    def DEFINELOCAL(self, t):
        return self.defaultValue(t)

    @_(r"3[d|D]")
    def CALLFUNC(self, t):
        return self.defaultValue(t)

    @_(r"3[e|E]")
    def RETURN(self, t):
        return self.defaultValue(t)

    @_(r"3[f|F]")
    def MODULO(self, t):
        return self.defaultValue(t)

    @_(r"40")
    def NEW(self, t):
        return self.defaultValue(t)

    @_(r"41")
    def DECLARELOCAL(self, t):
        return self.defaultValue(t)

    @_(r"42")
    def DECLAREARRAY(self, t):
        return self.defaultValue(t)

    @_(r"43")
    def DECLAREOBJECT(self, t):
        return self.defaultValue(t)

    @_(r"44")
    def TYPEOF(self, t):
        return self.defaultValue(t)

    @_(r"45")
    def TARGETOF(self, t):
        return self.defaultValue(t)

    @_(r"46")
    def ENUMERATE(self, t):
        return self.defaultValue(t)

    @_(r"47")
    def TYPEDADD(self, t):
        return self.defaultValue(t)

    @_(r"48")
    def TYPEDLESSTHAN(self, t):
        offset = self.getOffset()
        modifier = self.nextByteIs("12")
        t.value = {'offset': offset, 'modifier': modifier}
        return t

    @_(r"49")
    def TYPEDEQUAL(self, t):
        offset = self.getOffset()
        modifier = self.nextByteIs("12")
        t.value = {'offset': offset, 'modifier': modifier}
        return t

    @_(r"4[a|A]")
    def VALUEOF(self, t):
        return self.defaultValue(t)

    @_(r"4[b|B]")
    def TOSTRING(self, t):
        return self.defaultValue(t)

    @_(r"4[c|C]")
    def PUSHDUPLICATE(self, t):
        return self.defaultValue(t)

    @_(r"4[d|D]")
    def SWAP(self, t):
        return self.defaultValue(t)

    @_(r"4[e|E]")
    def GETMEMBER(self, t):
        return self.defaultValue(t)

    @_(r"4[f|F]")
    def SETMEMBER(self, t):
        return self.defaultValue(t)

    @_(r"50")
    def INCREMENT(self, t):
        return self.defaultValue(t)

    @_(r"51")
    def DECREMENT(self, t):
        return self.defaultValue(t)

    @_(r"52")
    def CALLMETHOD(self, t):
        return self.defaultValue(t)

    @_(r"53")
    def NEWMETHOD(self, t):
        return self.defaultValue(t)

    @_(r"54")
    def INSTANCEOF(self, t):
        return self.defaultValue(t)

    @_(r"55")
    def ENUMERATEOBJECT(self, t):
        return self.defaultValue(t)

    @_(r"60")
    def BITAND(self, t):
        return self.defaultValue(t)

    @_(r"61")
    def BITOR(self, t):
        return self.defaultValue(t)

    @_(r"62")
    def BITXOR(self, t):
        return self.defaultValue(t)

    @_(r"63")
    def BITLSHIFT(self, t):
        return self.defaultValue(t)

    @_(r"64")
    def BITRSHIFT(self, t):
        return self.defaultValue(t)

    @_(r"65")
    def BITRSHIFTUNSIGNED(self, t):
        return self.defaultValue(t)

    @_(r"66")
    def STRICTEQUAL(self, t):
        return self.defaultValue(t)

    @_(r"67")
    def GREATERTHAN(self, t):
        offset = self.getOffset()
        modifier = self.nextByteIs("12")
        t.value = {'offset': offset, 'modifier': modifier}
        return t

    @_(r"68")
    def STRINGGREATERTHAN(self, t):
        return self.defaultValue(t)

    @_(r"69")
    def EXTENDS(self, t):
        return self.defaultValue(t)

    @_(r"70")
    def UNKNOWN(self, t):
        return self.defaultValue(t)

    @_(r"81")
    def GOTOFRAME(self, t):
        return self.defaultValue(t)

    @_(r"83")
    def GETURL(self, t):
        return self.defaultValue(t)

    @_(r"87")
    def STORE(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(3)
        modifier = self.nextByteIs("4f")
        t.value = {
            'offset': offset,
            'value': hexToInt(nextBytes[2]),
            'modifier': modifier,
        }
        return t

    @_(r"88")
    def DEFINEDICTIONARY(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(2)[::-1]
        length = hexToInt(''.join(nextBytes))
        nextBytes = self.getNextBytes(length)
        params = splitBytesOn(nextBytes[2:-1])
        t.value = {
            'pool': list(map(byteArrayToString, params)),
            'offset': offset + 5,
            'length': length,
        }
        return t

    @_(r"8[a|A]")
    def WAITFORFRAME(self, t):
        return self.defaultValue(t)

    @_(r"8[b|B]")
    def SETTARGET(self, t):
        return self.defaultValue(t)

    @_(r"8[c|C]")
    def GOTOLABEL(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(2)
        length = hexToInt(nextBytes[0])
        nextBytes = self.getNextBytes(length)
        t.value = {'offset': offset, 'value': byteArrayToString(nextBytes)}
        return t

    @_(r"8[d|D]")
    def WAITFORFRAMEDYNAMIC(self, t):
        return self.defaultValue(t)

    @_(r"8[e|E]")
    def DEFINEFUNC2(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(2)
        length = hexToInt(nextBytes[0])
        nextBytes = self.getNextBytesFind(length)
        fnName = byteArrayToString(nextBytes)
        nextBytes = self.getNextBytes(1)
        paramLength = hexToInt(nextBytes[0])
        nextBytes = self.getNextBytes(2)
        regCount = hexToInt(nextBytes[1])
        nextBytes = self.getNextBytes(2)
        funcOption = FuncOption(hexToInt(nextBytes[0]))
        params = self.getParams(paramLength, length)
        nextBytes = self.getNextBytes(2)
        fnLength = hexToInt(''.join(nextBytes[::-1]))
        t.value = {
            'name': fnName,
            'paramLength': paramLength,
            'regCount': regCount,
            'params': params,
            'options': funcOption,
            'length': fnLength,
            'offset': offset + length + 3,
        }
        return t

    @_(r"8[f|F]")
    def TRY(self, t):
        return self.defaultValue(t)

    @_(r"94")
    def WITH(self, t):
        return self.defaultValue(t)

    @_(r"96")
    def PUSH(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(2)
        length = hexToInt(nextBytes[0])
        nextBytes = self.getNextBytes(length)
        t.value = {'offset': offset, 'value': self.getValues(nextBytes)}
        return t

    @_(r"99")
    def JUMP(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(4)
        length = unsignedToSigned(nextBytes[:-3:-1])
        # TODO: check bytes after length
        modifier = self.hasNextByte(length, " 9d") > 0  # oof case
        t.value = {
            'length': length,
            'offset': offset + 5,
            'modifier': modifier,
        }
        return t

    @_(r"9[a|A]")
    def GETURL2(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(3)
        t.value = {'offset': offset, 'value': nextBytes}
        return t

    @_(r"9[b|B]")
    def DEFINEFUNC(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(2)
        length = hexToInt(nextBytes[0])
        nextBytes = self.getNextBytesFind(length)
        fnName = byteArrayToString(nextBytes)
        nextBytes = self.getNextBytes(2)
        paramLength = hexToInt(nextBytes[0])
        params = self.getParams(paramLength, length)
        nextBytes = self.getNextBytes(2)
        fnLength = hexToInt(''.join(nextBytes[::-1]))
        t.value = {
            'name': fnName,
            'paramLength': paramLength,
            'params': params,
            'length': fnLength,
            'offset': offset + length + 3,
        }
        return t

    @_(r"9[d|D]")
    def IF(self, t):
        offset = self.getOffset()
        nextBytes = self.getNextBytes(4)
        length = hexToInt(f"{nextBytes[3]}{nextBytes[2]}")
        # TODO: check bytes after length
        modifier = IfOption.ifStmt
        isCase = self.findBytes(-6, 1, " 66")

        if isCase:
            modifier = IfOption.caseStmt
        else:
            hasJump = self.findBytes(length - 5, 5, " 99")
            if hasJump:
                jumpLength = unsignedToSigned(hasJump.split(' ')[:-3:-1])
                if jumpLength < 0:
                    modifier = IfOption.whileStmt

        t.value = {
            'length': length,
            'offset': offset + 5,
            'modifier': modifier,
        }
        return t

    @_(r"9[e|E]")
    def CALLFRAME(self, t):
        return self.defaultValue(t)

    @_(r"9[f|F]")
    def GOTO(self, t):
        return self.defaultValue(t)
