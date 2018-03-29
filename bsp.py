import sys
import math
import pygame
import numpy as np
from pygame.locals import QUIT


def sign(x): return (x > 0) - (x < 0)
DoubleTolerance = 1e-5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def Print(self):
        print(self.x, ' ', self.y)

    def getDistance(self, OtherPoint):
        return math.sqrt(math.pow((self.x - OtherPoint.x), 2) +
                         math.pow((self.y - OtherPoint.y), 2))


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def dotProduct(self, vector):
        return self.x * vector.x + self.y * vector.y


class LineSegment:
    def __init__(self, p1, p2, Normal=1, Name=''):
        self.p1 = p1
        self.p2 = p2
        self.Name = Name

        Dx = p2.x - p1.x
        Dy = p2.y - p1.y
        self.Normal = Normal
        self.NormalV = Vector(Dy, -Dx)
        if Normal == -1:
            self.NormalV = Vector(-Dy, Dx)

    def getMidPoint(self):
        return Point(
            ((self.p2.x + self.p1.x) / 2),
            ((self.p2.y + self.p1.y) / 2))

    def getLength(self):
        return self.p1.getDistance(self.p2)

    def Print(self):
        self.p1.Print()
        self.p2.Print()
        print(self.Normal, '\n')

    def compare(self, OtherLine):
        DotProduct1 = self.NormalV.dotProduct(
            Vector(
                (OtherLine.p1.x - self.p1.x),
                (OtherLine.p1.y - self.p1.y)))
        if abs(DotProduct1) < DoubleTolerance:
            DotProduct1 = 0

        DotProduct2 = self.NormalV.dotProduct(
            Vector(
                (OtherLine.p2.x - self.p1.x),
                (OtherLine.p2.y - self.p1.y)))
        if abs(DotProduct2) < DoubleTolerance:
            DotProduct2 = 0

        if (sign(DotProduct1) == 1 and sign(DotProduct2) == -
                1) or (sign(DotProduct1) == -1 and sign(DotProduct2) == 1):
            # Lines Partition
            return 'P'

        elif (DotProduct1 + DotProduct2) == 0:
            # Lines Collinear
            return 'C'

        elif sign(DotProduct1 + DotProduct2) == 1:
            # Lines no Partition, in Front
            return 'F'

        elif sign(DotProduct1 + DotProduct2) == -1:
            # Lines no Partition, in Back
            return 'B'

    def split(self, OtherLine):
        numer = (self.NormalV.x * (OtherLine.p1.x - self.p1.x)) + \
            (self.NormalV.y * (OtherLine.p1.y - self.p1.y))
        denom = ((-self.NormalV.x) * (OtherLine.p2.x - OtherLine.p1.x)) + \
            ((-self.NormalV.y) * (OtherLine.p2.y - OtherLine.p1.y))

        if denom != 0.0:
            t = numer / denom
        else:
            return None

        if 0 <= t <= 1.0:
            IntersectPoint = Point()
            IntersectPoint.x = OtherLine.p1.x + \
                t * (OtherLine.p2.x - OtherLine.p1.x)
            IntersectPoint.y = OtherLine.p1.y + \
                t * (OtherLine.p2.y - OtherLine.p1.y)
            return LineSegment(
                OtherLine.p1, IntersectPoint, (OtherLine.Name + '1')), LineSegment(
                IntersectPoint, OtherLine.p2, OtherLine.Normal, (OtherLine.Name + '2'))
        else:
            return None


class BinaryTree:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None

    def printTree(self):
        queue = [self]
        PrintString = ''

        while len(queue) > 0:
            tree = queue.pop(0)

            List = []
            for line in tree.data:
                List.append(line.Name)
            PrintString += str(List)
            if tree.left is not None:
                List = []
                for line in tree.left.data:
                    List.append(line.Name)
                PrintString += (' Left: ' + str(List))
                queue.append(tree.left)
            else:
                PrintString += (' Left: ' + ' / ')

            if tree.right is not None:
                List = []
                for line in tree.right.data:
                    List.append(line.Name)
                PrintString += (' Right: ' + str(List))
                queue.append(tree.right)
            else:
                PrintString += (' Right: ' + ' / ')

            PrintString += '\n'
        return PrintString


class BSP:
    def __init__(self):
        self.tree = BinaryTree()
        self.tree.data = []

    def readLinesFromFile(self, filename):
        with open(filename, 'r') as f:
            for line in f.readlines():
                if line[0] != '#':
                    data = [x for x in line.split('\t')]
                    points = [int(x) for x in data[0].split(',')]
                    self.tree.data.append(LineSegment(Point(points[0], points[1]), Point(
                        points[2], points[3]), int(data[1]), data[2][0:len(data[2]) - 1]))

    def readPointsFromFile(self, filename):
        with open(filename, 'r') as f:
            data = []
            for line in f.readlines():
                if line[0] != '#':
                    point = [int(x) for x in line.split(',')]
                    data.append(Point(point[0], point[1]))
            return data

    def heuristicMinimumPartition(self, ListLineSegments):
        MinIndex = 0
        MinPartition = 99999999
        for index, LineSegment in enumerate(ListLineSegments):
            PartitionCount = 0
            for OtherIndex, OtherLineSegment in enumerate(ListLineSegments):
                if index != OtherIndex:
                    CompareResult = LineSegment.compare(OtherLineSegment)
                    if CompareResult == 'P':
                        PartitionCount += 1

            if PartitionCount < MinPartition:
                MinPartition = PartitionCount
                MinIndex = index

        return MinIndex

    def heuristicEvenDivide(self, ListLineSegments):
        BestIndex = 0
        MinDivide = 99999999
        MinNodes = 99999999
        for index, LineSegment in enumerate(ListLineSegments):
            LeftCount = 0
            RightCount = 0
            for OtherIndex, OtherLineSegment in enumerate(ListLineSegments):
                if index != OtherIndex:
                    CompareResult = LineSegment.compare(OtherLineSegment)
                    if CompareResult == 'P':
                        LeftCount += 1
                        RightCount += 1
                    elif CompareResult == 'F':
                        LeftCount += 1
                    elif CompareResult == 'B':
                        RightCount += 1

            if abs(LeftCount - RightCount) < MinDivide:
                MinNodes = LeftCount + RightCount
                MinDivide = abs(LeftCount - RightCount)
                BestIndex = index

            elif abs(LeftCount - RightCount) == MinDivide:
                if LeftCount + RightCount < MinNodes:
                    MinNodes = LeftCount + RightCount
                    BestIndex = index

        return BestIndex

    def generateTree(self, tree, UseHeuristic='even'):
        BestIndex = 0
        if UseHeuristic == 'min':
            BestIndex = self.heuristicMinimumPartition(tree.data)
        elif UseHeuristic == 'even':
            BestIndex = self.heuristicEvenDivide(tree.data)

        DataList = []
        DataListLeft = []
        DataListRight = []
        H = tree.data.pop(BestIndex)
        DataList.append(H)

        for L in tree.data:
            result = H.compare(L)
            if result == 'P':
                SplitLines = H.split(L)

                for SplitLine in SplitLines:
                    SplitCompare = H.compare(SplitLine)
                    if SplitCompare == 'F':
                        DataListLeft.append(SplitLine)
                    elif SplitCompare == 'B':
                        DataListRight.append(SplitLine)
                    else:
                        print('Error!!', SplitCompare)

            elif result == 'C':
                DataList.append(L)

            elif result == 'F':
                DataListLeft.append(L)

            elif result == 'B':
                DataListRight.append(L)

        tree.data = DataList
        if len(DataListLeft) > 0:
            tree.left = BinaryTree()
            tree.left.data = DataListLeft
            if len(DataListLeft) > 1:
                self.generateTree(tree.left, UseHeuristic)

        if len(DataListRight) > 0:
            tree.right = BinaryTree()
            tree.right.data = DataListRight
            if len(DataListRight) > 1:
                self.generateTree(tree.right, UseHeuristic)

    def countNodes(self, tree):
        count = len(tree.data)
        if tree.left is not None:
            count += self.countNodes(tree.left)
        if tree.right is not None:
            count += self.countNodes(tree.right)
        return count

    def checkLoS(self, points):
        LoS = []
        for point in points:
            LoS.append(['X'] * len(points))

        for FromIndex, FromPoint in enumerate(points):
            for ToIndex, ToPoint in enumerate(points):
                # if LoS is not determined
                if (FromIndex != ToIndex) and (LoS[FromIndex][ToIndex] == 'X'):
                    # Assume there is LoS
                    LoS[FromIndex][ToIndex] = 'T'
                    LoS[ToIndex][FromIndex] = 'T'

                    SightSegment = LineSegment(
                        points[FromIndex], points[ToIndex])

                    # Point to root node
                    stack = [self.tree]
                    IsIntersection = False
                    # NumOfIntersections = 0
                    NumOfTraversals = 0
                    while len(stack) != 0 and IsIntersection == False:
                        TreePointer = stack.pop()
                        NumOfTraversals += 1

                        compareLoS = TreePointer.data[0].compare(SightSegment)
                        if compareLoS == 'P':
                            for line in TreePointer.data:
                                # NumOfIntersections += 1
                                if SightSegment.split(line) is not None:
                                    IsIntersection = True
                                    break

                            if IsIntersection:
                                LoS[FromIndex][ToIndex] = 'F'
                                LoS[ToIndex][FromIndex] = 'F'
                            else:
                                if TreePointer.left is not None:
                                    stack.append(TreePointer.left)
                                if TreePointer.right is not None:
                                    stack.append(TreePointer.right)

                        elif compareLoS == 'F':
                            if TreePointer.left is not None:
                                stack.append(TreePointer.left)

                        elif compareLoS == 'B':
                            if TreePointer.right is not None:
                                stack.append(TreePointer.right)

                    distance = points[FromIndex].getDistance(points[ToIndex])
                    if IsIntersection:
                        print(('Distance: %0.1f' % distance) +
                              ', # of traversals(F): ' + str(NumOfTraversals))
                    else:
                        print(('Distance: %0.1f' % distance) +
                              ', # of traversals(T): ' + str(NumOfTraversals))

        return LoS


def generateRandom(n, Range, a=3, isPowerLaw=False):
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
        MinDistance=10,
        MaxDistance=30,
        isUniform=True):
    Lines = []
    for i in range(n):
        Done = False
        while not Done:
            P1x = 0
            P1y = 0
            P2x = -1
            P2y = -1
            if isUniform:
                P1x = int(round(np.random.uniform(0, width)))
                P1y = int(round(np.random.uniform(0, height)))
                Distance = np.random.uniform(MinDistance, MaxDistance)

                while not 0 <= P2x <= width:
                    c = np.random.uniform(-1, 1)
                    P2x = P1x + int(round(c * Distance))

                while not 0 <= P2y <= height:
                    P2y = P1y + \
                        int(round(sign(np.random.uniform(-1, 1)) * (1 - (abs(c))) * Distance))

            else:
                P1x = int(round(np.random.power(3.0) * width))
                P1y = int(round(np.random.power(3.0) * height))
                Distance = np.random.uniform(MinDistance, MaxDistance)

                while not 0 <= P2x <= width:
                    c = np.random.uniform(-1, 1)
                    P2x = P1x + int(round(c * Distance))

                while not 0 <= P2y <= height:
                    P2y = P1y + \
                        int(round(sign(np.random.uniform(-1, 1)) * (1 - (abs(c))) * Distance))
            r = round(generateRandom(1, 1))
            if r == 0:
                r = -1
            # NewLine = LineSegment(Point(int(round(NumbersX[0])), int(round(NumbersY[0]))), Point(int(round(NumbersX[1])), int(round(NumbersY[1]))), r)
            NewLine = LineSegment(Point(P1x, P1y), Point(P2x, P2y), r)
            # if NewLine.getLength() >= MinDistance and NewLine.getLength() <=
            # MaxDistance:
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
    bsptree = BSP()
    # bsptree.readLinesFromFile(sys.argv[1])
    p = True
    bsptree.tree.data = generateRandomScene(
        1024, SCREEN_WIDTH, SCREEN_HEIGHT, isUniform=p)

    # with open('environment.txt', 'w') as of:
    #	count = 65
    #	for line in bsptree.tree.data:
    #		of.write(str(line.p1.x) + ',' + str(line.p1.y) + ',' + str(line.p2.x) + ',' + str(line.p2.y) + '\t' + str(line.Normal) + '\t' + chr(count) + '\n')
    #		count += 1

    # points = bsptree.readPointsFromFile(sys.argv[2])
    points = generatePoints(40, SCREEN_WIDTH, SCREEN_HEIGHT, isUniform=p)

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
