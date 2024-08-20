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

    def __neg__(self):
        return Coord(-self.x, -self.y)

    def __mul__(self, other):
        if type(other) == float or type(other) == int:
            return Coord(self.x*other, self.y*other)
        raise Exception(f"Cannot multiply Coord {self.x, self.y} with {other}")

    def __imul__(self, other):
        if type(other) == float or type(other) == int:
            self.x *= other
            self.y *= other
            return self
        raise Exception(f"Cannot multiply Coord {self.x, self.y} with {other}")

    def __truediv__(self, other):
        if type(other) == float or type(other) == int:
            return Coord(self.x/other, self.y/other)
        raise Exception(f"Cannot divide Coord {self.x, self.y} with {other}")

    def __itruediv__(self, other):
        if type(other) == float or type(other) == int:
            self.x /= other
            self.y /= other
            return self
        raise Exception(f"Cannot divide Coord {self.x, self.y} with {other}")

    def __floordiv__(self, other):
        if type(other) == float or type(other) == int:
            return Coord(self.x//other, self.y//other)
        raise Exception(f"Cannot divide Coord {self.x, self.y} with {other}")

    def __ifloordiv__(self, other):
        if type(other) == float or type(other) == int:
            self.x //= other
            self.y //= other
            return self
        raise Exception(f"Cannot divide Coord {self.x, self.y} with {other}")

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
        self._obstaclelist = []
        Thread(target=self._run).start()

    def addcommand(self, *args):
        for moves in args:
            self._movelist.append(moves)

    def addobstacle(self, *args):
        for obstacles in args:
            self._obstaclelist.append(obstacles)

    def move(self, command: tuple, screen: pygame.Surface):
        BACKWARDS = False
        length, radius, handed = command
        if length < 0:
            length = -length
            BACKWARDS = True
            handed = -handed
        if not radius:
            for i in range(length):
                if not BACKWARDS:
                    self._current += (cos(self._heading), sin(self._heading))
                else:
                    self._current -= (cos(self._heading), sin(self._heading))
                screen.set_at(self._current.int(), (255, 255, 255))
            return

        displacement = Coord(
            radius * cos(self._heading - handed * pi / 2),
            radius * sin(self._heading - handed * pi / 2)
        )
        if BACKWARDS:
            displacement = -displacement
        temp = self._current - displacement
        for _ in range(length):
            displacement = displacement.rotate(handed/radius)
            self._current = temp + displacement
            screen.set_at(self._current.int(), (255, 255, 255))
        self._heading = self._heading + handed * length / radius
        return

    def draw(self, obstacle: tuple, screen: pygame.Surface):
        color, centre, radius = obstacle
        pygame.draw.circle(screen, color, centre, radius)

    def _run(self):
        pygame.init()
        pygame.display.set_caption("Simulator")
        screen = pygame.display.set_mode((self._size, self._size))
        while True:
            if self._movelist:
                self.move(self._movelist[0], screen)
                self._movelist.pop(0)
                pygame.display.flip()
            if self._obstaclelist:
                self.draw(self._obstaclelist[0], screen)
                self._obstaclelist.pop(0)
                pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()