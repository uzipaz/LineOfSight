from geometry import LineSegment, Point

class BinaryTree:
    """Binary tree class"""
    def __init__(self):
        """Constructor, declares variables for left and right sub-tree and data for the current node"""
        self.left = None
        self.right = None
        self.data = []

    def printTree(self):
        """Prints the all tree nodes 'Name' attribute in a binary tree format"""
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
    """Binary Space Partition class, optimally generates BSP tree from a list of line segments by using a heuristic"""
    def __init__(self):
        """Constructor, initializes binary tree"""
        self.tree = BinaryTree()

    def readLinesFromFile(self, filename):
        """Not in use currently"""
        with open(filename, 'r') as f:
            for line in f.readlines():
                if line[0] != '#':
                    data = [x for x in line.split('\t')]
                    points = [int(x) for x in data[0].split(',')]
                    self.tree.data.append(LineSegment(Point(points[0], points[1]), Point(
                        points[2], points[3]), int(data[1]), data[2][0:len(data[2]) - 1]))

    def readPointsFromFile(self, filename):
        """Not in use currently"""
        with open(filename, 'r') as f:
            data = []
            for line in f.readlines():
                if line[0] != '#':
                    point = [int(x) for x in line.split(',')]
                    data.append(Point(point[0], point[1]))
            return data

    def heuristicMinimumPartition(self, ListLineSegments):
        """Returns the index of the line segment in 'ListLineSegments' which causes the least amount of partitions with other line segments in the list"""
        MinIndex = 0
        MinPartition = 99999999
        for index, ALineSegment in enumerate(ListLineSegments):
            PartitionCount = 0
            for OtherIndex, OtherLineSegment in enumerate(ListLineSegments):
                if index != OtherIndex:
                    CompareResult = ALineSegment.compare(OtherLineSegment)
                    if CompareResult == 'P':
                        PartitionCount += 1

            if PartitionCount < MinPartition:
                MinPartition = PartitionCount
                MinIndex = index

        return MinIndex

    def heuristicEvenDivide(self, ListLineSegments):
        """Returns the index of the line segment in 'ListLineSegments' which produces the most balanced tree"""
        BestIndex = 0
        MinDivide = 99999999
        MinNodes = 99999999
        for index, ALineSegment in enumerate(ListLineSegments):
            LeftCount = 0
            RightCount = 0
            for OtherIndex, OtherLineSegment in enumerate(ListLineSegments):
                if index != OtherIndex:
                    CompareResult = ALineSegment.compare(OtherLineSegment)
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
        """
        Generates the binary space partition tree recursively using the specified heuristic at each sub-tree
        :param tree: BinaryTree, value should be self.tree on the first call, this argument exists so we can traverse the tree recursively
        :param UseHeuristic: string, either 'even' for balanced tree or 'min' for least number of nodes
        :return: nothing
        """
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
        """returns the number of nodes in the entire tree by traversing the tree"""
        count = len(tree.data)
        if tree.left is not None:
            count += self.countNodes(tree.left)
        if tree.right is not None:
            count += self.countNodes(tree.right)
        return count

    def checkLoS(self, points):
        """Determine line of sight between all points in the list by constructing a line segment for the two points
        in question and comparing it for intersection with line segments in the BSP tree
        :param points: a list of Point objects
        :return: a list of lists, n by n, an entry at [i][j] tells wether point i and point j have line of sight with each other
        """
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
