import pygame

# import the pygame module, so you can use it
import pygame
from math import atan2, cos, sin, pi

SIZE = 640
RIGHT = 1
LEFT = -1
movementlist = [
    (200, 80, LEFT),
    (150, 0, RIGHT),
    (200, 30, LEFT)
]


def move(
        length: int,
        radius: float,
        handed: int,
        current: (float, float),
        heading: float,
        screen: pygame.Surface
) -> (tuple, float):
    if not radius:
        for i in range(length):
            curx, cury = current
            current = (
                curx + cos(heading),
                cury + sin(heading)
            )
            screen.set_at([int(i) for i in current], (255, 255, 255))
        return current, heading
    displacement = radius * cos(heading - handed * pi / 2), radius * sin(heading - handed * pi / 2)
    curx = current[0] - displacement[0]
    cury = current[1] - displacement[1]
    for i in range(length):
        disx, disy = displacement
        displacement = (
            disx * cos(handed / radius) - disy * sin(handed / radius),
            disx * sin(handed / radius) + disy * cos(handed / radius),
        )
        current = (
            curx + disx,
            cury + disy
        )
        screen.set_at([int(i) for i in current], (255, 255, 255))
    heading = heading + handed*length/radius
    return current, heading


# define a main function
def main():
    pygame.init()
    pygame.display.set_caption("Simulator")
    screen = pygame.display.set_mode((SIZE, SIZE))

    # move
    current = SIZE/2, SIZE/2
    heading = 5
    for length, radius, handed in movementlist:

        print(heading)
        current, heading = move(length, radius, handed, current, heading, screen)
    pygame.display.flip()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
