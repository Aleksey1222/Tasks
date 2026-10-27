def calc(a, b, op):
    match op:
        case 1: return a - b
        case 2: return a * b
        case 3: return a / b if b != 0 else 0.0
        case _: return a + b

for _ in range(3):
    a = float(input())
    b = float(input())
    op = int(input())
    print(calc(a, b, op))
