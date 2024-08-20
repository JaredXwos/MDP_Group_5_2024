from SimClasses import Coord, Sim, LEFT
from math import acos, sqrt


def inversepathing(goal: Coord):
    return (goal.x ** 2 + goal.y ** 2) / goal.x * 2


Goal = Coord(300, 300)
Current = Coord(320, 320)
radius = inversepathing(Goal-Current)
Centre = Coord(Current.x + radius, Current.y)
print(Centre.x)
sim = Sim(640, Coord(320, 320), 5)
sim.addobstacle(
    ((255, 255, 255), Goal.int(), 5),
    ((255, 255, 255), Current.int(), 5),
    ((255, 255, 255), Centre.int(), 5),
)
sim.addcommand((int(-radius*6), -radius, LEFT))
