def string15(s):
    count = 0
    for ch in s:
        if ("А" <= ch <= "Я") or ("а" <= ch <= "я") or ch in ("Ё", "ё"):
            count += 1
    return count
