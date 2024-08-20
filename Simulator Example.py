from SimClasses import RIGHT, LEFT, Sim, Coord

sim = Sim(640,Coord(320, 320), 5)
sim.addcommand(
#   (distance, turn radius, LEFT/RIGHT)
    (150, None, None),  # go straight
    (300, 100, RIGHT),
    (150, None, None),
)
sim.addcommand(
    (150, 30, LEFT),
    (150, 60, RIGHT)
)
