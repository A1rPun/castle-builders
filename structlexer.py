from baselexer import BaseLexer
from util import splitBytes


class StructLexer(BaseLexer):
    tokens = {STRING, FLOAT, NULL, UNDEFINED, REGISTER, BOOLEAN,
              DOUBLE, INTEGER, DICTLOOKUP, DICTLOOKUPLARGE}

    @_(r"00")
    def STRING(self, t):
        # nextBytes = self.getNextBytes(1)
        # t.value = int(nextBytes[0], 16)
        return t

    @_(r"01")
    def FLOAT(self, t):
        nextBytes = self.getNextBytes(4)[::-1]
        t.value = float.fromhex(''.join(nextBytes))
        return t

    NULL = r'02'
    UNDEFINED = r'03'

    @_(r"04")
    def REGISTER(self, t):
        nextBytes = self.getNextBytes(1)
        t.value = int(nextBytes[0], 16)
        return t

    @_(r"05")
    def BOOLEAN(self, t):
        nextBytes = self.getNextBytes(1)
        t.value = nextBytes[0] == "01"
        return t

    @_(r"06")
    def DOUBLE(self, t):
        nextBytes = self.getNextBytes(8)[::-1]
        t.value = float.fromhex(''.join(nextBytes))
        return t

    @_(r"07")
    def INTEGER(self, t):
        nextBytes = self.getNextBytes(4)[::-1]
        t.value = int(''.join(nextBytes), 16)
        return t

    @_(r"08")
    def DICTLOOKUP(self, t):
        nextBytes = self.getNextBytes(1)
        t.value = int(nextBytes[0], 16)
        return t

    @_(r"09")
    def DICTLOOKUPLARGE(self, t):
        nextBytes = self.getNextBytes(2)[::-1]
        t.value = int(''.join(nextBytes), 16)
        return t
