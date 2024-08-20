from math import cos, sin, pi
import pygame
from threading import Thread

LEFT = -1
RIGHT = 1


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if type(other) == Coord:
            return Coord(self.x + other.x, self.y + other.y)
        if (
            type(other) == tuple and
            len(other) > 1 and
            type(other[0]) == float and
            type(other[1]) == float
        ):
                return Coord(self.x + other[0], self.y + other[1])
        raise Exception(f"Cannot add coord {self.x, self.y} with {other}")

    def __sub__(self, other):
        if type(other) == Coord:
            return Coord(self.x - other.x, self.y - other.y)
        if (
            type(other) == tuple and
            len(other) > 1 and
            type(other[0]) == float and
            type(other[1]) == float
        ):
                return Coord(self.x - other[0], self.y - other[1])
        raise Exception(f"Cannot subtract {other} from coord {self.x, self.y}")

    def __iadd__(self, other):
        if type(other) == Coord:
            self.x += other.x
            self.y += other.y
            return self
        if (
                type(other) == tuple and
                len(other) > 1 and
                type(other[0]) == float and
                type(other[1]) == float
        ):
            self.x += other[0]
            self.y += other[1]
            return self
        raise Exception(f"Cannot add coord {self.x, self.y} with {other}")

    def __isub__(self, other):
        if type(other) == Coord:
            self.x -= other.x
            self.y -= other.y
            return self
        if (
                type(other) == tuple and
                len(other) > 1 and
                type(other[0]) == float and
                type(other[1]) == float
        ):
            self.x -= other[0]
            self.y -= other[1]
            return self
        raise Exception(f"Cannot add coord {self.x, self.y} with {other}")

    def int(self):
        return int(self.x), int(self.y)

    def rotate(self, angle):
        return Coord(
            self.x * cos(angle) - self.y * sin(angle),
            self.x * sin(angle) + self.y * cos(angle),
        )


class Sim:
    def __init__(self, size: int, current: Coord, heading: float):
        self._size = size
        self._current = current
        self._heading = heading
        self._movelist = []
        Thread(target=self._run).start()

    def addcommand(self, *args):
        for moves in args:
            self._movelist.append(moves)

    def move(self, command: tuple, screen: pygame.Surface):
        length, radius, handed = command
        if not radius:
            for i in range(length):
                self._current += (cos(self._heading), sin(self._heading))
                screen.set_at(self._current.int(), (255, 255, 255))
            return

        displacement = Coord(
            radius * cos(self._heading - handed * pi / 2),
            radius * sin(self._heading - handed * pi / 2)
        )
        temp = self._current - displacement
        for _ in range(length):
            displacement = displacement.rotate(handed/radius)
            self._current = temp + displacement
            screen.set_at(self._current.int(), (255, 255, 255))
        self._heading = self._heading + handed * length / radius
        return

    def _run(self):
        pygame.init()
        pygame.display.set_caption("Simulator")
        screen = pygame.display.set_mode((self._size, self._size))
        while True:
            if self._movelist:
                self.move(self._movelist[0], screen)
                self._movelist.pop(0)
                pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()