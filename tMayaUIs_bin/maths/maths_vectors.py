"""
Vector Maths Scripts
Tom Wood 2020
"""

# Basic Vector Maths Functions
import math
from pymel.core import datatypes as dt


# Variable Definitions.
pi = 3.14159265358979323846264338327950288419716939937510582097494459230781640


# Returns the absolute value of number supplied.
def abs(n):
    return n * sign(n)


# Average of Absolute values.
def absAvg(v):
    vn = len(v)
    posX = []
    posY = []
    posZ = []
    for s in v:
        posX.append(abs(s[0]))
        posY.append(abs(s[1]))
        posZ.append(abs(s[2]))
    return sum(posX) / vn, sum(posY) / vn, sum(posZ) / vn


# Average of Absolute values corrected around C.
def absAvgC(v, c):
    vn = len(v)
    posX = []
    posY = []
    posZ = []
    for s in v:
        posX.append(abs(s[0] - c[0]))
        posY.append(abs(s[1] - c[1]))
        posZ.append(abs(s[2] - c[2]))
    return sum(posX) / vn, sum(posY) / vn, sum(posZ) / vn


# Angle between two vectors.
def angBetween(a, b, unit="radians"):
    magA = mag(a)
    magB = mag(b)
    dotP = dot(a, b)
    angle = math.acos(dotP / (magA * magB))
    if unit == "degrees":
        return rtd(angle)
    else:
        return angle

# Finds area of circle
def area(r):
    return pi * math.pow(r, 2)


# Basic average of list of Numbers.
def avg(s):
    return sum(s) / len(s)


# Average of vectors as vector.
def avgv(vctIn):

    x = [x[0] for x in vctIn]
    y = [y[1] for y in vctIn]
    z = [z[2] for z in vctIn]

    numVcts = len(vctIn)
    return sum(x) / numVcts, sum(y) / numVcts, sum(z) / numVcts


# Bounding box of values.
def bbox(v):
    x = []
    y = []
    z = []
    for s in v:
        x.append(s[0])
        y.append(s[1])
        z.append(s[2])
    return [[min(x), min(y), min(z)], [max(x), max(y), max(z)]]


# Middle of bBox.
def bboxmid(v):
    b = bbox(v)
    bb = [(b[0][0] + b[1][0]) / 2, (b[0][1] + b[1][1]) / 2, (b[0][2] + b[1][2]) / 2]
    return bb


# Finds circumference
def circumference(r):
    return 2 * pi * r


# Finds radius around centre defined by points - Avg Distance from centre
def cradius(v, c):
    d = []
    for a in v:
        d.append(dist(a, c))
    return sum(d) / len(d)


# Full cross product by pos.
def cross(a, b):
    x = a[1] * b[2] - a[2] * b[1]
    y = a[2] * b[0] - a[0] * b[2]
    z = a[0] * b[1] - a[1] * b[0]
    return ((x, y, z))


# Cross Product
def crossa(a, b):
    vecLength = (mag(a), mag(b))
    crossProduct = vecLength[0] * vecLength[1] * math.sin(1)
    return crossProduct


# Returns the Distance between two vectors with c as the centre.
def dist(a, b):
    # Pythagoras to Calculate
    distance = math.sqrt(math.pow((a[0]) - (b[0]), 2) + math.pow((a[1]) - (b[1]), 2) + math.pow((a[2]) - (b[2]), 2))
    return distance


def scalarDist(x, y):
    distance = math.sqrt(math.pow((x) - (y), 2))
    return distance


# Dot Product
def dot(a, b):
    dotProduct = a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    return dotProduct


# Converts Degrees to Radians.
def dtr(f):
    radian = f / (180 / pi)
    return radian


# Returns magnitude of a given vector.
def mag(vec):
    magnitude = math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
    return magnitude


# Returns the median of input list.
def med(v):
    x = []
    y = []
    z = []
    medV = int(len(v) / 2)
    for s in v:
        x.append(s[0])
        y.append(s[1])
        z.append(s[2])
    xSort = sorted(x)
    ySort = sorted(y)
    zSort = sorted(z)
    return xSort[medV], ySort[medV], zSort[medV]


# Finds the normal Unit Vector to the plane
def normalToPlane(vec):
    crossls = []
    a = vec[0]
    b = vec[1]
    v = vec[2]
    u = vec[3]
    crossls.append(cross(a, b))
    crossls.append(cross(v, u))
    return uo(absAvg(crossls))


# Find the plane of 4 given points.
def plane(cardinal):
    g = vbet(cardinal[0], cardinal[1])
    h = vbet(cardinal[2], cardinal[3])
    n = cross(g, h)
    return g, h, n


# Converts Radians to Degrees.
def rtd(f):
    degree = (180 / pi) * f
    return degree


# Outputs 1 or -1 based on sign of number input
def sign(n):
    if n < 0:
        s = -1
    elif n > 0:
        s = 1
    else:
        s = 0
    return s


# Unit vector from Origin.
def uo(a):
    d = mag(a)
    if d > 0:
        uV = (((a[0]) / d), ((a[1]) / d), (a[2]) / d)
    else:
        uV = (0, 0, 0)
    return uV


# Finds unit vector of a from C.
def uoc(a, c):
    d = dist(c, a)
    uV = c[0] + ((a[0] - c[0]) / d), c[1] + ((a[1] - c[1]) / d), c[2] + ((a[2] - c[2]) / d)
    return uV


# Finds the vector in direction of supplied vector with magnitude r. NEEDS - (Vector, Float)
def uor(a, r):
    d = mag(a)
    if d != 0:
        uV = (a[0] * r / d, a[1] * r / d, a[2] * r / d)
    else:
        uV = (0, 0, 0)
    return uV

# def scalaruor(a, r):
#     d = mag(a)
#     uV = (((a[0]) * r / d), ((a[1]) * r / d), (a[2]) * r / d)
#     return uV


# Unit multiplied by given length r. NEEDS - (Vector, Vector, Float)
def ur(c, a, r):
    d = dist(c, a)
    uV = (((a[0] - c[0]) * r / d) + c[0], ((a[1] - c[1]) * r / d) + c[1], (a[2] - c[2]) * r / d + c[2])
    return (uV)


# Finds the vector of a and b
def vbet(a, b):
    return b[0] - a[0], b[1] - a[1], b[2] - a[2]


# Finds zero position of given list of vectors around C.
def zpos(v, c):
    # Loop to zero-out positions for vector maths.
    zp = []
    for t in v:
        zp.append((t[0] - c[0], t[1] - c[1], t[2] - c[2]))
    return zp


def findAxis(c, vtx, zPos, r, objPos, cType="2D"):
    # Planar across Axes
    if cType == "blah":
        n = 0
        for x in range(len(vtx)):
            mVec = dt.Vector(
                (c[0] + uor(zPos[n], r)[0]) - objPos[0],
                (c[1] + uor(zPos[n], r)[1]) - objPos[1],
                (c[2] + uor(zPos[n], r)[2]) - objPos[2]
            )
            vtx[x].setPosition(mVec)
            n += 1

        returnString = "Circularised On 2D Plane"
        # return posAxisA, negAxisA, posAxisB, negAxisB

    # FINDS VERTICES ACROSS MULTIPLE PLANES
    else:

        # Base Axes for side comparison definitions
        axes = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

        # Across axis lists.
        xplus = []
        xminus = []
        yplus = []
        yminus = []
        zplus = []
        zminus = []

        # Queries positions of Vertices as above or below Axes
        for zp in zPos:
            # Positive and Negatives across axis around Origin
            # X
            dotX = dot(zp, axes[0])
            # Y
            dotY = dot(zp, axes[1])
            # Z
            dotZ = dot(zp, axes[2])

            # Positive and Negatives across Axes: dot >= 0  for above, dot < 0 for below
            if dotX >= 0:
                xplus.append(zp)
            else:
                xminus.append(zp)
            if dotY >= 0:
                yplus.append(zp)
            else:
                yminus.append(zp)
            if dotZ >= 0:
                zplus.append(zp)
            else:
                zminus.append(zp)

        # AVERAGE OF VECTORS AROUND X AXIS
        if xplus and xminus:
            xplus = (
                sum([x[0] for x in xplus]) / len(xplus),
                sum([y[1] for y in xplus]) / len(xplus),
                sum([z[2] for z in xplus]) / len(xplus)
            )
            xminus = (
                sum([x[0] for x in xminus]) / len(xminus),
                sum([y[1] for y in xminus]) / len(xminus),
                sum([z[2] for z in xminus]) / len(xminus)
            )
        else:
            xplus, xminus = None, None

        # AVERAGE OF VECTORS AROUND Y AXIS
        if yplus and yminus:
            yplus = (
                sum([x[0] for x in yplus]) / len(yplus),
                sum([y[1] for y in yplus]) / len(yplus),
                sum([z[2] for z in yplus]) / len(yplus)
            )
            yminus = (
                sum([x[0] for x in yminus]) / len(yminus),
                sum([y[1] for y in yminus]) / len(yminus),
                sum([z[2] for z in yminus]) / len(yminus)
            )
        else:
            yplus, yminus = None, None

        # AVERAGE OF VECTORS AROUND Z AXIS
        if zplus and zminus:
            zplus = (
                sum([x[0] for x in zplus]) / len(zplus),
                sum([y[1] for y in zplus]) / len(zplus),
                sum([z[2] for z in zplus]) / len(zplus)
            )
            zminus = (
                sum([x[0] for x in zminus]) / len(zminus),
                sum([y[1] for y in zminus]) / len(zminus),
                sum([z[2] for z in zminus]) / len(zminus)
            )
        else:
            zplus, zminus = None, None

        # AXES TO USE
        xAxVal = max([x[0] for x in zPos]) - min([x[0] for x in zPos])
        yAxVal = max([y[1] for y in zPos]) - min([y[1] for y in zPos])
        zAxVal = max([z[2] for z in zPos]) - min([z[2] for z in zPos])
        acrossVal = [xAxVal, yAxVal, zAxVal]

        if min(acrossVal) == xAxVal:
            posAxisA = zplus
            negAxisA = zminus
            posAxisB = yplus
            negAxisB = yminus
            print("ZY")

        elif min(acrossVal) == yAxVal:
            posAxisA = xplus
            negAxisA = xminus
            posAxisB = zplus
            negAxisB = zminus
            print("XZ")

        elif min(acrossVal) == zAxVal:
            posAxisA = xplus
            negAxisA = xminus
            posAxisB = yplus
            negAxisB = yminus
            print("XY")
        else:
            raise ValueError("Can't determine Axes for Circle Creation")

        return posAxisA, negAxisA, posAxisB, negAxisB


def circType(zPos):
        # Sum of X vals
        xA = sum([x[0] for x in zPos])
        # Sum of Y vals
        yA = sum([y[1] for y in zPos])
        # Sum of Z vals
        zA = sum([z[2] for z in zPos])

        symmetry = [xA, yA, zA]

        axV = []
        for ax in symmetry:
            if ax != 0.0:
                axV.append(1)
            else:
                axV.append(0)

        if sum(axV) == 0 or sum(axV) == 1:
            print("2D Circle")
            cType = "2D"

        else:
            print("3D Circle")
            cType = "3D"

        return cType

def vertsByQuadrant(axisA, axisB, verts, zpos):
    indexList = []
    n = 0
    qOne = []
    qTwo = []
    qThree = []
    qFour = []

    for v in zpos:
        print(verts[n])
        dotA = dot(axisA, v)
        # angleA = angBetween(axisA, v, unit="degrees")
        dotB = dot(axisB, v)
        # angleB = angBetween(axisB, v, unit="degrees")
        if dotA > 0 and dotB > 0:
            qOne.append(verts[n])
        elif dotA > 0 and dotB < 0:
            qTwo.append(verts[n])
        elif dotA < 0 and dotB < 0:
            qThree.append(verts[n])
        elif dotA < 0 and dotB > 0:
            qFour.append(verts[n])
        print(dotA)
        # print(angleA)
        print(dotB)
        # print(angleB)
        n += 1

    return axisA, axisB, qOne, qTwo, qThree, qFour

# def quaternionCalcs(I,J,K,W):
#     # IJK define a Normal vector as the axis of rotation. W defines a constant representing the term required
#     # for Vector to be Unit.
