def splitBytes(string):
    return string.strip().split(" ")


def byteArrayToString(byteArray):
    return bytes.fromhex(''.join(byteArray)).decode("utf-8")


def byteLength(string):
    return int(string, 16)


def toByte(byte):
    return "%0.2x" % byte
