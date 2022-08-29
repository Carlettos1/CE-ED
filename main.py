"""
eq 1:
    Fc/A = hbar*c*pi^2/240a^4
    a: distancia entre placas


"""
from math import sqrt
from time import sleep
from typing import DefaultDict
DT = 1
class Placa:
    def __init__(self, largo: float, pos: tuple) -> None:
        self.largo = largo
        self.pos = pos
        pass
    def distanceTo(self, other) -> float:
        total = 0
        for i in range(len(self.pos)):
            total += abs(self.pos[0]**2 - other.pos[0]**2)
        return sqrt(total)
    def applyPression(self, pression):
        f = pression * self.largo**2
        self.pos = (self.pos[0] - f * DT, self.pos[1], self.pos[2])

def P(a: float) -> float:
    return 1/240/a**4

P1 = Placa(5, (0, 0, 0))
P2 = Placa(5, (2, 0, 0))
for i in range(1_000):
    d = P1.distanceTo(P2)
    p = P(d)
    P1.applyPression(p)
    P2.applyPression(p)
    print(f"d:{d}")
    pass