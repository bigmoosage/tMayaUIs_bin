"""
Scripts for circle maths in maya
Tom Wood 2020
"""

# Used Modules.
import math

import pymel.core as pm
import select
from tomLib.maths import maths_vectors as vct

# Maths variable Definitions
pi = 3.14159265359


# Finds centre of points based on bounding box
def ccentre(v, ctype):
    if ctype == "bb":
        return vct.bboxmid(v)
    elif ctype == "avg":
        return vct.avgv(v)
    elif ctype == "med":
        return vct.med(v)
    else:
        print("Second argument needs String: bb, avg or med.")


# Finds radius of centre defined by points - Avg Distance from centre
def cradius(v, c):
    d = []
    for a in v:
        d.append(vct.dist(a, c))
    return sum(d) / len(d)


# Finds Points around origin
def zpos(v, c):
    # Loop to zero-out positions for vector maths.
    zp = []
    for t in v:
        zp.append((t[0] - c[0], t[1] - c[1], t[2] - c[2]))
    return zp


def axissides(zeroPosition):

    axes = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

    xplus = []
    xminus = []

    for zp in zeroPosition:
        dot = vct.dot(zp, axes[0])
        if dot >= 0:
            xplus.append(zp)
        else:
            xminus.append(zp)

    zplus = []
    zminus = []

    for zp in zeroPosition:
        dot = vct.dot(zp, axes[2])
        if dot >= 0:
            zplus.append(zp)
        else:
            zminus.append(zp)

    yplus = []
    yminus = []

    for zp in zeroPosition:
        dot = vct.dot(zp, axes[1])
        if dot >= 0:
            yplus.append(zp)
        else:
            yminus.append(zp)
    if xplus:
        xplus = vct.avgv(xplus)
    if xminus:
        xminus = vct.avgv(xminus)
    if zplus:
        zplus = vct.avgv(zplus)
    if zminus:
        zminus = vct.avgv(zminus)
    if yplus:
        yplus = vct.avgv(yplus)
    if yminus:
        yminus = vct.avgv(yminus)

    if xplus == zplus or xplus == zminus or xminus == zminus or xminus == zplus:
        print("Across XY Plane")
        # print("XA")
        # print("YB")
        return xplus, xminus, yplus, yminus
    else:
        print("Across ZX Plane")
        # print("XA")
        # print("ZB")
        return xplus, xminus, zplus, zminus


def cplane(v, c):
    fa = axissides(v, c)
    pl = vct.plane(fa)
    a = vct.uo(pl[0])
    b = vct.uo(vct.cross(a, pl[2]))
    n = vct.uo(pl[2])

    return a, b, n


def pcircle(s, v, c):
    cp = cplane(v, c)
    allT = zpos(v, c)
    a = cp[0]
    b = cp[1]
    r = cradius(v, c)

    n = 0
    for obj in s:
        an = vct.angBetween(allT[n], a)
        if vct.dot(allT[n], b) > 0:
            theta = an
            pm.move((c[0] + r * math.cos(theta) * a[0] + r * math.sin(theta) * b[0]),
                    (c[1] + r * math.cos(theta) * a[1] + r * math.sin(theta) * b[1]),
                    (c[2] + r * math.cos(theta) * a[2] + r * math.sin(theta) * b[2]),
                    obj,
                    xyz=True)
        elif vct.dot(allT[n], b) < 0:
            theta = an * -1
            pm.move((c[0] + r * math.cos(theta) * a[0] + r * math.sin(theta) * b[0]),
                    (c[1] + r * math.cos(theta) * a[1] + r * math.sin(theta) * b[1]),
                    (c[2] + r * math.cos(theta) * a[2] + r * math.sin(theta) * b[2]),
                    obj,
                    xyz=True)
        else:
            pm.move((c[0] + r * math.cos(0) * a[0] + r * math.sin(0) * b[0]),
                    (c[1] + r * math.cos(0) * a[1] + r * math.sin(0) * b[1]),
                    (c[2] + r * math.cos(0) * a[2] + r * math.sin(0) * b[2]),
                    obj,
                    xyz=True)
        n = n + 1


# Takes the zero position and the centre to output the type of circle
def circleType(zeroPositions):

    xA = sum([x[0] for x in zeroPositions])

    yA = sum([y[1] for y in zeroPositions])

    zA = sum([z[2] for z in zeroPositions])

    symmetry = [xA, yA, zA]

    print(symmetry)

    axV = []
    for ax in symmetry:
        if ax != 0.0:
            axV.append(1)
        else:
            axV.append(0)

    if sum(axV) == 0 or sum(axV) == 1:
        print("2D Circle")
        return "2D"

    else:
        print("3D Circle")
        return "3D"


def flatcircle(s, vp, c, obj):
    sel = s
    zp = zpos(vp, c)
    r = cradius(vp, c)
    n = 0
    for s in sel:
        px = (c[0] + vct.uor(zp[n], r)[0]) - obj[0]
        py = (c[1] + vct.uor(zp[n], r)[1]) - obj[1]
        pz = (c[2] + vct.uor(zp[n], r)[2]) - obj[2]
        pm.xform(s, t=(px, py, pz))
        n = n + 1


def circularise(ctype):
    sel = select.seltype()
    s = sel[0]
    v = sel[1]
    c = ccentre(v, ctype)
    ct = circleType(v)
    if ct == 1:
        obj = pm.xform(s[0].split(".vtx")[0], q=True, t=True)
        flatcircle(s, v, c, obj)
    else:
        pcircle(s, v, c)


def spherise(*args):
    if args:
        if len(args) != 3 or not isinstance(args[0], str):
            print("If any Arguments: Needs, object(str), Centre Type (string - avg, bb or med), detail(float)")
        else:
            pass
    if len(args) == 3:
        obj = args[0]
        detail = args[2]
        ctype = args[1]
    else:
        ctype = "avg"
        detail = 0
        obj = []
    sel = select.seltype()
    sl = sel[0]
    v = sel[1]
    if obj:
        c = select.qXform(obj)
    else:
        c = ccentre(v, ctype)
    zp = zpos(v, c)
    r = cradius(v, c)
    n = 0
    if detail:
        for s in sl:
            rdif = r - vct.mag(zp[n])
            r = r - rdif * detail
            px = c[0] + vct.uor(zp[n], r)[0]
            py = c[1] + vct.uor(zp[n], r)[1]
            pz = c[2] + vct.uor(zp[n], r)[2]
            pm.move(px, py, pz, s, xyz=True)
            n = n + 1
    else:
        for s in sl:
            px = c[0] + vct.uor(zp[n], r)[0]
            py = c[1] + vct.uor(zp[n], r)[1]
            pz = c[2] + vct.uor(zp[n], r)[2]
            pm.move(px, py, pz, s, xyz=True)
            n = n + 1
