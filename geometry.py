import math

def sign(x): return (x > 0) - (x < 0)
DoubleTolerance = 1e-5

class Point:
    """2D cartesian coordinate representation of point"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def Print(self):
        print(self.x, ' ', self.y)

    def getDistance(self, OtherPoint):
        return math.sqrt(math.pow((self.x - OtherPoint.x), 2) +
                         math.pow((self.y - OtherPoint.y), 2))

class Vector:
    """A quite basic 2D vector class"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def dotProduct(self, vector):
        """returns vector dot product of this vector with vector as function argument"""
        return self.x * vector.x + self.y * vector.y


class LineSegment:
    """2D line segment class"""
    def __init__(self, p1, p2, Normal=1, Name=''):
        """Arguments: p1 (type: Point), p2 (type: Point), Normal (type: Int), Name (type: String),
        arg 'Normal' represents one of two possible directions of normal vector of our line segment, arg 'Name
        is any arbitrary name for the purpose of identifying nodes when printing binary trees"""
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
        """returns middle point of our line segment"""
        return Point(
            ((self.p2.x + self.p1.x) / 2),
            ((self.p2.y + self.p1.y) / 2))

    def getLength(self):
        """returns length of our line segment """
        return self.p1.getDistance(self.p2)

    def Print(self):
        """prints point coordinates and direction of normal vector"""
        self.p1.Print()
        self.p2.Print()
        print(self.Normal, '\n')

    def compare(self, OtherLine):
        """Compares two line segments for space partitioning, returns a character that identify the comparison of the two lines
        if 'OtherLine' exists completely on side or other of our line segment (imagined as an infinite line segment), then it will return either 'F' or 'B' depending on the direction of 'OtherLine' to our line segment
        if our line segment (infinite) intersects the 'Otherline' and thus causes the 'Otherline' to split into two, it returns 'P'
        if both line segments are collinear, returns 'C'
        """
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

        if (sign(DotProduct1) == 1 and sign(DotProduct2) == -1) \
                or (sign(DotProduct1) == -1 and sign(DotProduct2) == 1):
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
        """
        :param OtherLine: LineSegment
        :return: returns two LineSegments if LineSegment in 'self' (as an infinite line segment) partitions 'otherLine' in space partitioning,
        otherwise returns None
        """
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