def string6(c):
    if "0" <= c <= "9":
        return "digit"
    elif "A" <= c <= "Z":
        return "upper"
    elif "a" <= c <= "z":
        return "lower"
    return "unknown"
