def splitBytes(splitter):
    return splitter.strip().split(" ")


def byteArrayToString(byteArray):
    return bytes.fromhex(''.join(byteArray)).decode("utf-8")


def hexToInt(hexString):
    return int(hexString, 16)


def toByte(byte):
    return "%0.2x" % byte


def boolToStr(boolean):
    return "true" if bool(boolean) else "false"


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


def unsignedToSigned(byteArray, bits=16):
    # TODO: better 16bit unsigned to signed conversion plz
    number = hexToInt(''.join(byteArray))
    return number if number < 32768 else (65536 - number) * -1


def stripQuote(quotedStr):
    return quotedStr[1:-1] if quotedStr[0] == '"' else quotedStr
