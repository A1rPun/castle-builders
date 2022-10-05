def splitBytes(splitter):
    return splitter.strip().split(" ")


def byteArrayToString(byteArray):
    return bytes.fromhex(''.join(byteArray)).decode("utf-8")


def hexToInt(hexString):
    return int(hexString, 16)


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

    newList.append(chunk)
    return newList
