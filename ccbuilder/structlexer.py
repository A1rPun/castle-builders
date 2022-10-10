import struct
from ccbuilder.baselexer import BaseLexer
from ccbuilder.util import splitBytes, hexToInt, unsignedToSigned


class StructLexer(BaseLexer):
    tokens = {STRING, FLOAT, NULL, UNDEFINED, REGISTER, BOOLEAN,
              DOUBLE, INTEGER, DICTLOOKUP, DICTLOOKUPLARGE}

    @_(r"00")
    def STRING(self, t):
        # TODO: FIX
        return t

    @_(r"01")
    def FLOAT(self, t):
        nextBytes = self.getNextBytes(4)[::-1]
        # TODO: FIX
        t.value = float.fromhex(''.join(nextBytes))
        return t

    NULL = r'02'
    UNDEFINED = r'03'

    @_(r"04")
    def REGISTER(self, t):
        nextBytes = self.getNextBytes(1)
        t.value = hexToInt(nextBytes[0])
        return t

    @_(r"05")
    def BOOLEAN(self, t):
        nextBytes = self.getNextBytes(1)
        t.value = nextBytes[0] == "01"
        return t

    @_(r"06")
    def DOUBLE(self, t):
        nextBytes = self.getNextBytes(4)[::-1]
        restBytes = self.getNextBytes(4)[::-1]
        byteString = ''.join(nextBytes + restBytes)
        t.value = struct.unpack("d", struct.pack("Q",int("0x"+byteString, 16)))[0]
        return t

    @_(r"07")
    def INTEGER(self, t):
        nextBytes = self.getNextBytes(4)[::-1]
        t.value = unsignedToSigned(nextBytes, 32)
        return t

    @_(r"08")
    def DICTLOOKUP(self, t):
        nextBytes = self.getNextBytes(1)
        t.value = hexToInt(nextBytes[0])
        return t

    @_(r"09")
    def DICTLOOKUPLARGE(self, t):
        nextBytes = self.getNextBytes(2)[::-1]
        t.value = hexToInt(''.join(nextBytes))
        return t
