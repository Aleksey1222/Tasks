import os

s = input()
try:
    with open(s, "w", encoding="utf-8"):
        pass
    print(True)
except OSError:
    print(False)