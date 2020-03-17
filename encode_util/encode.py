def encode(string):
    key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    out = ''
    ch = ['' for i in range(3)]
    enc = ['' for i in range(4)]
    i = 0

    # ord: char->ASCII
    # chr: ASCII->char
    while i < len(string):
        for j in range(len(ch)):
            if i >= len(string):
                ch[j] = '\0'
            else:
                ch[j] = string[i]

            i = i + 1

        enc[0] = chr(ord(ch[0]) >> 2)
        enc[1] = chr(((ord(ch[0]) & 3) << 4) | (ord(ch[1]) >> 4))
        enc[2] = chr(((ord(ch[1]) & 15) << 2) | (ord(ch[2]) >> 6))
        enc[3] = chr(ord(ch[2]) & 63)

        if ch[1] == '\0':
            enc[2] = chr(64)
            enc[3] = chr(64)
        elif ch[2] == '\0':
            enc[3] = chr(64)

        out += key[ord(enc[0])] + key[ord(enc[1])] + key[ord(enc[2])] + key[ord(enc[3])]
        for j in range(len(ch)): ch[j] = '\0'
        for j in range(len(enc)): enc[j] = '\0'

    return out