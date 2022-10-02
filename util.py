def splitBytes(splitter):
    return splitter.strip().split(" ")


def byteArrayToString(byteArray):
    return bytes.fromhex(''.join(byteArray)).decode("utf-8")


def byteLength(string):
    return int(string, 16)


def toByte(byte):
    return "%0.2x" % byte


def splitBytesOn(byteArray, splitter="00"):
    newList = []
    chunk = []
    for byte in byteArray:
        if byte == splitter:
            newList.append(chunk)
            chunk = []
        else:
            chunk.append(byte)
    return newList
