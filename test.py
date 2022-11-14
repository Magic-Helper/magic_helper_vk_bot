from enum import Enum

class Test(Enum):
    A = 1
    B = 2


a = Test.A
b = Test.B
a1 = Test.A


print(a == b)
print(a == a1)