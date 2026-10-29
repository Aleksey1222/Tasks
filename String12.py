def string12(s, s_sign, n):
    chunks = [s[i : i + n] for i in range(0, len(s), n)]
    return s_sign.join(chunks)
