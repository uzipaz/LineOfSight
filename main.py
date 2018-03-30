import sys
import pygame
from pygame.locals import QUIT
import numpy as np

from bsp import BSP
from geometry import LineSegment, Point

def sign(x): return (x > 0) - (x < 0)

def generateRandom(n, Range, a=3, isPowerLaw=False):
    """
    Generate a random number
    :param n: int, Number of numbers to return
    :param Range: float, maximum range of a number to be generated
    :param a: float, for use in powerlaw distribution
    :param isPowerLaw: boolean, generate with powerlaw distribution if true else generate with uniform distribution
    :return: integer or list of numbers depending on argument n
    """
    if not isPowerLaw:
        if n > 1:
            return list(np.random.uniform(0, Range, n))
        else:
            return np.random.uniform(0, Range)

    else:
        if n > 1:
            return list(np.random.power(a, n) * Range)
        else:
            return np.random.power(a) * Range


def generateRandomScene(
        n,
        width,
        height,
        MinLength=10,
        MaxLength=50,
        isUniform=True):
    """
    Randomnly generates a list of non intersecting line segments
    :param n: int, Number of line segments
    :param width: int, our area width
    :param height: int, our area height
    :param MinLength: float, Minimum possible length of a line segment
    :param MaxLength: float, Maximum possible length of a line segment
    :param isUniform: boolean, whether the position of line segments should be generated with uniform distributed random number or with powerlaw distribution
    :return: a list of line segments
    """
    Lines = []
    for i in range(n):
        Done = False
        while not Done:
            P2x = -1
            P2y = -1
            c = 0
            if isUniform:
                P1x = int(round(np.random.uniform(0, width)))
                P1y = int(round(np.random.uniform(0, height)))
                Distance = np.random.uniform(MinLength, MaxLength)


                while not 0 <= P2x <= width:
                    c = np.random.uniform(-1, 1)
                    P2x = P1x + int(round(c * Distance))

                while not 0 <= P2y <= height:
                    P2y = P1y + \
                        int(round(sign(np.random.uniform(-1, 1)) * (1 - (abs(c))) * Distance))

            else:
                P1x = int(round(np.random.power(3.0) * width))
                P1y = int(round(np.random.power(3.0) * height))
                Distance = np.random.uniform(MinLength, MaxLength)

                while not 0 <= P2x <= width:
                    c = np.random.uniform(-1, 1)
                    P2x = P1x + int(round(c * Distance))

                while not 0 <= P2y <= height:
                    P2y = P1y + \
                        int(round(sign(np.random.uniform(-1, 1)) * (1 - (abs(c))) * Distance))
            r = round(generateRandom(1, 1))
            if r == 0:
                r = -1

            NewLine = LineSegment(Point(P1x, P1y), Point(P2x, P2y), r)
            IsIntersection = False
            for line in Lines:
                if NewLine.split(line) is not None:
                    IsIntersection = True
                    break

            if not IsIntersection:
                Lines.append(NewLine)
                Done = True

    return Lines

def generatePoints(n, width, height, isUniform=True):
    """
    Randomnly generates a list of points
    :param n: int, Number of points
    :param width: int, area width
    :param height: int, area height
    :param isUniform: boolean, whether the position of line segments should be generated with random number of uniform distribution or powerlaw distribution
    :return: list of points
    """
    Points = []
    for i in range(n):
        if isUniform:
            Points.append(Point(int(round(generateRandom(1, width))),
                                int(round(generateRandom(1, height)))))
        else:
            Points.append(Point(int(round(generateRandom(1, width, isPowerLaw=True))), int(
                round(generateRandom(1, height, isPowerLaw=True)))))

    return Points

def main():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    bsptree = BSP()
    isUniform = True
    bsptree.tree.data = generateRandomScene(
        512, SCREEN_WIDTH, SCREEN_HEIGHT, isUniform=isUniform)

    points = generatePoints(40, SCREEN_WIDTH, SCREEN_HEIGHT, isUniform=isUniform)

    # set up pygame
    pygame.init()

    # set up the window
    windowSurface = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('BSP')

    # set up the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    ORANGE = (255, 127, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)

    # draw the white background onto the surface
    windowSurface.fill(BLACK)

    # draw lines onto the surface
    for l in bsptree.tree.data:
        pygame.draw.line(windowSurface, WHITE,
                         (l.p1.x, l.p1.y), (l.p2.x, l.p2.y), 2)

    for point in points:
        pygame.draw.circle(windowSurface, ORANGE, (point.x, point.y), 4, 4)

    print('Generating tree')
    bsptree.generateTree(bsptree.tree, UseHeuristic='even')

    pygame.draw.circle(
        windowSurface, YELLOW, (int(
            bsptree.tree.data[0].getMidPoint().x), int(
            bsptree.tree.data[0].getMidPoint().y)), 4, 4)

    LoS = bsptree.checkLoS(points)

    for iFrom, From in enumerate(LoS):
        for iTo, To in enumerate(LoS):
            if iFrom != iTo and LoS[iFrom][iTo] == 'T':
                pygame.draw.line(
                    windowSurface,
                    GREEN,
                    (points[iFrom].x,
                     points[iFrom].y),
                    (points[iTo].x,
                     points[iTo].y))

    print(bsptree.tree.printTree())
    print(bsptree.countNodes(bsptree.tree))

    # draw the window onto the screen
    pygame.display.update()

    # run the game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()