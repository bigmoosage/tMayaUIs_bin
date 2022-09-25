"""
Custom curves for maya.
Tom Wood 2020
"""

# Collection of Custom Curves for Creation in Maya and Python via Maya Cmds.
import pymel.core as pm
import maya.cmds as cd
from pymel.core import nodetypes as nt


def circleCage(name, *args):
    pm.circle(n="crv_circleCageUpCirc01", r=10, nr=[0, 1, 0], ch=0)
    bottomCircle = pm.circle(n="crv_circleCageBotCirc01", r=10, nr=[0, 1, 0], ch=0)
    pm.xform(bottomCircle, t=[0, 20, 0])
    pm.makeIdentity(bottomCircle, a=1, t=1)

    frontCurve = pm.curve(
        n="crv_circleCageFrontCrv01",
        d=3,
        p=[
            (0, 20, 10),
            (0, 16.666667, 11),
            (0, 10, 12),
            (0, 3.333333, 11),
            (0, 0, 10)
        ]
    )

    backCurve = pm.duplicate(frontCurve)
    backCurve = pm.rename(backCurve, "crv_circleCageBackCrv01")
    pm.xform(backCurve, ro=[0, 180, 0])
    pm.makeIdentity(backCurve, a=1, r=1)


# Create arrow curve.
def arrow(name, *args):
    curveMake = pm.curve(
        n=name,
        d=1,
        p=[
            (2, -3, 0),
            (-2, -3, 0),
            (-2, 0, 0),
            (-4, 0, 0),
            (0, 5, 0),
            (4, 0, 0),
            (2, 0, 0),
            (2, -3, 0)
        ]
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    pm.rename(shapeNode, curveMake + "shape")
    return curveMake


# Create box curve.
def box(name, *args):
    curveMake = pm.curve(
        n=name,
        d=1,
        p=[
            (-1, 1, 1),
            (1, 1, 1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, 1, 1),
            (-1, -1, 1),
            (-1, -1, -1),
            (-1, 1, -1),
            (-1, 1, 1),
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (1, 1, -1),
            (1, -1, -1),
            (1, -1, 1),
            (-1, -1, 1),
            (-1, -1, -1),
            (1, -1, -1)]
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    pm.rename(shapeNode, curveMake + "shape")
    return curveMake


# Create cardinalArrow curve.
def cardinalArrow(name, *args):
    curveMake = pm.curve(
        name=name,
        d=1,
        p=[
            (-2.0, 0.0, -2.0),
            (0.0, 0.0, -4.0),
            (2.0, 0.0, -2.0),
            (1.0, 0.0, -2.0),
            (1.0, 0.0, -1.0),
            (2.0, 0.0, -1.0),
            (2.0, 0.0, -2.0),
            (4.0, 0.0, 0.0),
            (2.0, 0.0, 2.0),
            (2.0, 0.0, 1.0),
            (1.0, 0.0, 1.0),
            (1.0, 0.0, 2.0),
            (2.0, 0.0, 2.0),
            (0.0, 0.0, 4.0),
            (-2.0, 0.0, 2.0),
            (-1.0, 0.0, 2.0),
            (-1.0, 0.0, 1.0),
            (-2.0, 0.0, 1.0),
            (-2.0, 0.0, 2.0),
            (-4.0, 0.0, 0.0),
            (-2.0, 0.0, -2.0),
            (-2.0, 0.0, -1.0),
            (-1.0, 0.0, -1.0),
            (-1.0, 0.0, -2.0),
            (-2, 0.0, -2.0),
        ]
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    control = pm.rename(shapeNode, curveMake + "Shape01")
    return curveMake


# Create cardinalArrow02 curve.
def cardinalArrow02(name, *args):
    curveMake = pm.curve(
        name=name,
        d=1,
        p=[
            (-2.0, 0.0, -3.0),
            (0.0, 0.0, -5.0),
            (2.0, 0.0, -3.0),
            (1.0, 0.0, -3.0),
            (1.0, 0.0, -1.0),
            (3.0, 0.0, -1.0),
            (3.0, 0.0, -2.0),
            (5.0, 0.0, 0.0),
            (3.0, 0.0, 2.0),
            (3.0, 0.0, 1.0),
            (1.0, 0.0, 1.0),
            (1.0, 0.0, 3.0),
            (2.0, 0.0, 3.0),
            (0.0, 0.0, 5.0),
            (-2.0, 0.0, 3.0),
            (-1.0, 0.0, 3.0),
            (-1.0, 0.0, 1.0),
            (-3.0, 0.0, 1.0),
            (-3.0, 0.0, 2.0),
            (-5.0, 0.0, 0.0),
            (-3.0, 0.0, -2.0),
            (-3.0, 0.0, -1.0),
            (-1.0, 0.0, -1.0),
            (-1.0, 0.0, -3.0),
            (-2.0, 0.0, -3.0),
        ]
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    control = pm.rename(shapeNode, curveMake + "Shape01")
    return curveMake


# Create circleArrow curve.
def circleArrow(name, *args):
    mainCurve = threePointArc(name, 3, 8, (0, 0, -2), (-2, 0, 0), (0, 0, 2))
    outerArc = threePointArc(name + 'OuterArc', 3, 8, (0, 0, -4), (-4, 0, 0), (0, 0, 4))
    rightArrow = linearCurve(name + 'RightArrow', [(0, 0, -4), (0, 0, -5), (2, 0, -3), (0, 0, -1), (0, 0, -2)])
    leftArrow = linearCurve(name + 'LeftArrow', [(0, 0, 4), (0, 0, 5), (2, 0, 3), (0, 0, 1), (0, 0, 2)])
    toDelete = [outerArc, rightArrow, leftArrow]
    shapes = [outerArc.getShape(), rightArrow.getShape(), leftArrow.getShape()]
    for shp in shapes:
        pm.parent(shp, mainCurve, shape=True, r=True)

    pm.delete(toDelete)

    pm.select(mainCurve)

    return mainCurve


# Create diamond curve.
def diamond(name, *args):
    curveMake = pm.curve(
        n=name,
        d=1,
        p=[
            (0, 1, 0),
            (0, 0, 1),
            (0, -1, 0),
            (0, 0, -1),
            (0, 1, 0),
            (-1, 0, 0),
            (0, -1, 0),
            (1, 0, 0),
            (0, 1, 0),
            (-1, 0, 0),
            (0, 0, 1),
            (1, 0, 0),
            (0, 0, -1),
            (-1, 0, 0)
        ]
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    control = pm.rename(shapeNode, curveMake + "shape")
    return curveMake


# Create droplet curve.
def droplet(name, *args):
    curveMake = pm.curve(
        name=name,
        d=3,
        p=[
            (1.0, 0.0, 0.0),
            (0.0, 0.0, -1.0),
            (-1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
            (1.0, 0.0, 0.0),
        ]
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    control = pm.rename(shapeNode, curveMake + "Shape01")
    return curveMake


# Create halfCircleArrow curve.
def halfCircleArrow(name, *args):
    mainCurve = circleArrow(name)

    transform = nt.Transform(mainCurve)

    arcone = twoPointArc(name + 'ArcOne', 3, 4, 2, (-2, 0, 0), (0, 2, 0), (0, 0, -3))
    arctwo = twoPointArc(name + 'ArcTwo', 3, 4, 4, (-4, 0, 0), (0, 4, 0), (0, 0, -3))
    arrow = linearCurve(name + 'Arrow', [(0, 4, 0,), (0, 5, 0,), (2, 3, 0,), (0, 1, 0,), (0, 2, 0,)])

    toDelete = [arcone, arctwo, arrow]

    shapes = [arcone.getShape(), arctwo.getShape(), arrow.getShape()]

    for shp in shapes:
        pm.parent(shp, mainCurve, shape=True, r=True)

    pm.xform(mainCurve, translation=[4, 0, 0])

    pm.makeIdentity(mainCurve, a=True, t=True)

    pm.xform(mainCurve, rp=[0, 0, 0])

    pm.xform(transform, ro=[0, -90, 0])

    pm.makeIdentity(transform, r=1, a=True)

    pm.delete(toDelete)

    pm.select(mainCurve)

    return mainCurve


# Create house curve.
def house(name, *args):
    houseCurve = pm.curve(
        n=name,
        d=1,
        p=[
            (-3, 0, 0),
            (-4, 5, 0),
            (-5, 5, 0),
            (-3, 7, 0),
            (-3, 9, 0),
            (-2, 9, 0),
            (-2, 8, 0),
            (0, 10, 0),
            (5, 5, 0),
            (4, 5, 0),
            (3, 0, 0),
            (-3, 0, 0),
        ]
    )
    doorCurve = pm.curve(
        n="crv_door01",
        d=1,
        p=[
            (-1, 0, 0),
            (-1, 3, 0),
            (1, 3, 0),
            (1, 0, 0)
        ]
    )
    windowCurveL = pm.curve(
        n="crv_windowL01",
        d=1,
        p=[
            (-3, 4, 0),
            (-3, 6, 0),
            (-1, 6, 0),
            (-1, 4, 0),
            (-3, 4, 0)
        ]
    )
    windowCurveR = pm.curve(
        n="crv_windowR01",
        d=1,
        p=[
            (3, 4, 0),
            (3, 6, 0),
            (1, 6, 0),
            (1, 4, 0),
            (3, 4, 0)
        ]
    )
    houseShapes = pm.listRelatives(doorCurve, windowCurveL, windowCurveR, s=True)
    pm.parent(houseShapes[0], houseShapes[1], houseShapes[2], houseCurve, s=True, r=True)
    pm.delete(doorCurve, windowCurveL, windowCurveR)
    pm.select(cl=True)
    return houseCurve


# Create joint curve.
def joint(name, *args):
    c = []
    cSh = []
    normal = {0: [1, 0, 0], 1: [0, 0, 1], 2: [0, 1, 0]}
    for x in range(0, 3, 1):
        circle = pm.circle(n=name, nr=normal.get(x), ch=False)
        c.append(circle[0])
        cSh.append(circle[0].getShape())

    pm.parent(cSh[1], cSh[2], c[0], s=True, r=True)
    pm.rename(cSh[1], c[0] + "shape1")
    pm.rename(cSh[2], c[0] + "shape2")
    pm.delete(c[1], c[2])
    pm.select(c[0])
    return c[0]


# linearCurve method.
def linearCurve(name, ps, *args):
    curveMake = pm.curve(
        name=name,
        d=1,
        p=ps
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    control = pm.rename(shapeNode, curveMake + "Shape01")

    return curveMake


# Create line circle curve.
def lineCircle(name, *args):
    curveMake = pm.curve(
        name=name,
        d=1,
        p=[
            (0, 0, 0),
            (0, 0, 3)
        ]
    )
    endCirc = pm.circle(
        name=name + 'EndCircle',
        ch=False,
        radius=1
    )
    pm.xform(endCirc, translation=[0, 0, 4])
    pm.xform(endCirc, rotation=[0, 90, 0])
    pm.makeIdentity(a=True, t=True, r=True)

    pm.parent(endCirc[0].getShape(), curveMake, shape=True, r=True)

    pm.delete(endCirc)

    pm.select(curveMake)

    return curveMake


# Create Locator curve.
def loccrv(name, *args):
    curveMake = pm.curve(
        name=name,
        d=1,
        p=[
            (1, 0, 0),
            (-1, 0, 0),
            (0, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, 0),
            (0, 0, 1),
            (0, 0, -1)
        ]
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    pm.rename(shapeNode, curveMake + "Shape01")
    return curveMake


# Create man curve.
def man(name, *args):
    main = pm.curve(
        n=name,
        d=1,
        p=[
            (1, 2, 0),
            (0.7, 3, 0),
            (0.7, 4, 0),
            (-0.7, 4, 0),
            (-0.7, 3, 0),
            (-1, 2, 0),
            (1, 2, 0)
        ]
    )
    curves = [pm.curve(
        n="crv_lLeg01",
        d=1,
        p=[
            (0.1, 0, 0),
            (0.8, 0, 0),
            (1, 2, 0),
            (0, 2, 0),
            (0.1, 0, 0)
        ]
    ), pm.curve(
        n="crv_rLeg01",
        d=1,
        p=[
            (-0.1, 0, 0),
            (-0.8, 0, 0),
            (-1, 2, 0),
            (0, 2, 0),
            (-0.1, 0, 0)
        ]
    ), pm.curve(
        n="crv_rarm01",
        d=1,
        p=[
            (-0.7, 4, 0),
            (-0.7, 3, 0),
            (-1.2, 2, 0),
            (-1.8, 2.4, 0),
            (-0.7, 4, 0)
        ]
    ), pm.curve(
        n="crv_larm01",
        d=1,
        p=[
            (0.7, 4, 0),
            (0.7, 3, 0),
            (1.2, 2, 0),
            (1.8, 2.4, 0),
            (0.7, 4, 0)
        ]
    ), pm.circle(
        n="crv_head01",
        center=[0, 5, 0],
        ch=False
    ), pm.curve(
        n="crv_smile01",
        d=3,
        p=[
            (0.6, 4.6, 0),
            (0.5, 4.5, 0),
            (0, 4.2, 0),
            (-0.5, 4.5, 0),
            (-0.6, 4.6, 0)
        ]
    ), pm.circle(
        n="crv_eye01",
        center=[0, 5.2, 0],
        r=0.2,
        ch=False
    )
    ]
    for c in curves:
        shape = pm.listRelatives(c, s=True)
        pm.parent(shape, main, s=True, r=True)
        pm.delete(c)
        pm.select(main)
    return main


# Create mountain curve.
def mountain(name, *args):
    curveMake = pm.curve(
        n=name,
        d=1,
        p=[
            (-4, 0, 0),
            (-3, 4, 0),
            (-1, 2, 0),
            (1, 6, 0),
            (3, 0, 0),
            (-4, 0, 0)
        ]
    )
    mountainCurvePart01 = pm.curve(
        n="crv_mountPart01",
        d=1,
        p=[
            (-2, 3, 0),
            (-1, 5, 0),
            (0, 4, 0)
        ]
    )
    mountainCurvePart02 = pm.curve(
        n="crv_mountPart02",
        d=1,
        p=[
            (-1, 0, 0),
            (1, 3, 0),
            (2, 0, 0)
        ]
    )
    mountainShapes = pm.listRelatives(mountainCurvePart01, mountainCurvePart02, s=True)
    pm.parent(mountainShapes[0], mountainShapes[1], curveMake, s=True, r=True)
    pm.delete(mountainCurvePart01, mountainCurvePart02)
    pm.select(curveMake)
    return curveMake


# Create offArrow curve.
def offArrow(name, *args):
    curveMake = pm.curve(
        name=name,
        d=1,
        p=[
            (-1.0, 0.0, 0.4),
            (-0.6, 0.0, -0.4),
            (0.0, 0.0, -0.4),
            (0.2, 0.0, -0.6),
            (1.0, 0.0, 0.0),
            (0.2, 0.0, 0.6),
            (0.0, 0.0, 0.4),
            (-1.0, 0.0, 0.4),
        ]
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    control = pm.rename(shapeNode, curveMake + "Shape01")
    return curveMake


# Create oneAxisFinger curve.
def oneAxisFinger(name, *args):
    curveMake = pm.curve(
        name=name,
        d=1,
        p=[
            (-1.0, 0.0, -1.0),
            (0.0, 0.0, -2.0),
            (1.0, 0.0, -2.0),
            (1.0, 0.0, -1.0),
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 1.0),
            (1.0, 0.0, 2.0),
            (0.0, 0.0, 2.0),
            (-1.0, 0.0, 1.0),
            (-1.0, 0.0, -1.0),
        ]
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    control = pm.rename(shapeNode, curveMake + "Shape01")
    return curveMake


# Create puzzla curve.
def puzzle(name, *args):
    curveMake = pm.curve(
        n=name,
        d=1,
        p=[
            (0, -5, 0),
            (1, -5, 0),
            (1, -3, 0),
            (3, -3, 0),
            (3, -1, 0),
            (1, -1, 0),
            (1, 1, 0),
            (3, 1, 0),
            (3, 3, 0),
            (1, 3, 0),
            (1, 5, 0),
            (-1, 5, 0),
            (-1, 3, 0),
            (-3, 3, 0),
            (-3, 1, 0),
            (-1, 1, 0),
            (-1, -1, 0),
            (-3, -1, 0),
            (-3, -3, 0),
            (-1, -3, 0),
            (-1, -5, 0),
            (0, -5, 0)
        ]
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    pm.rename(shapeNode, curveMake + "shape")
    return curveMake


# Create road curve.
def road(name, *args):
    roadCurveMain = pm.curve(
        n=name,
        d=1,
        p=[
            (-8, 0, 0),
            (-8, 0, 20)
        ]
    )
    roadCurvePart01 = pm.curve(
        n="crv_roadP01",
        d=1,
        p=[
            (8, 0, 0),
            (8, 0, 20)
        ]
    )
    roadCurvePart02 = pm.curve(
        n="crv_road01",
        d=1,
        p=[
            (-1, 0, 13),
            (-1, 0, 17),
            (1, 0, 17),
            (1, 0, 13),
            (-1, 0, 13)
        ]
    )
    roadCurvePart03 = pm.curve(
        n="crv_roadP01",
        d=1,
        p=[
            (-1, 0, 7),
            (-1, 0, 3),
            (1, 0, 3),
            (1, 0, 7),
            (-1, 0, 7)
        ]
    )
    roadShapes = pm.listRelatives(roadCurvePart01, roadCurvePart02, roadCurvePart03, s=True)
    pm.parent(roadShapes[0], roadShapes[1], roadShapes[2], roadCurveMain, s=True, r=True)
    pm.delete(roadCurvePart01, roadCurvePart02, roadCurvePart03)
    pm.scale(0.375, 0.375, 0.375, roadCurveMain, r=True)
    return roadCurveMain


# Create rocket curve.
def rocket(name, *args):
    curveMake = pm.curve(
        n=name,
        d=1,
        p=[
            (-5, 0, 0),
            (-5, 3, 0),
            (-2, 6, 0),
            (-2, 20, 0),
            (0, 25, 0),
            (2, 20, 0),
            (2, 6, 0),
            (5, 3, 0),
            (5, 0, 0),
            (2, 3, 0),
            (1, 2, 0),
            (2, 0, 0),
            (-2, 0, 0),
            (-1, 2, 0),
            (-2, 3, 0),
            (-5, 0, 0)
        ]
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    pm.rename(shapeNode, curveMake + "shape")
    return curveMake


# Create target curve.
def target(name, *args):
    c = []
    cSh = []
    for x in range(0, 3, 1):
        circle = pm.circle(n="crv_" + name + "0" + str(x + 1), nr=[0, 1, 0], ch=False)
        c.append(circle[0])
        cSh.append(circle[0].getShape())
    pm.scale(c[1], 0.6, 0.6, 0.6, r=True, os=True)
    pm.scale(c[2], 0.2, 0.2, 0.2, r=True, os=True)
    pm.makeIdentity(c[1], c[2], a=True, t=True, r=True, s=True)
    pm.rename(cSh[1], c[0] + "shape1")
    pm.rename(cSh[2], c[0] + "shape2")
    pm.parent(cSh[1], cSh[2], c[0], s=True, r=True)
    pm.delete(c[1], c[2])
    pm.select(c[0])

    return c


# Create tetrahedron curve.
def tetrahedron(name, *args):
    curveMake = pm.curve(
        n=name,
        d=1,
        p=[
            (-1, 0, 1),
            (-1, 0, -1),
            (1, 0, 0),
            (-0.3333, 1, 0),
            (-1, 0, -1),
            (-1, 0, 1),
            (-0.3333, 1, 0),
            (-1, 0, 1),
            (1, 0, 0)
        ]
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    pm.rename(shapeNode, curveMake + "shape")
    return curveMake


# Create threeDCircleArrow curve.
def threeDCircleArrow(name, *args):
    mainCurve = circleArrow(name)
    two = circleArrow(name)
    transform = nt.Transform(mainCurve)
    pm.setAttr(two + '.rotateX', 90)
    pm.makeIdentity(two, a=True, r=True)

    shapes = two.getShapes()

    for shp in shapes:
        pm.parent(shp, mainCurve, shape=True, r=True)

    pm.delete(two)
    pm.xform(transform, ro=[0, -90, 0])
    pm.xform(mainCurve, piv=[-4, 0, 0])

    pm.makeIdentity(transform, a=True, r=True)

    pm.select(mainCurve)

    return mainCurve


# Create Three Point Arc.
def threePointArc(name, deg, span, p1, p2, p3):
    arc01 = pm.createNode("makeThreePointCircularArc")
    pm.setAttr(arc01 + ".d", deg)
    pm.setAttr(arc01 + ".s", span)
    pm.setAttr(arc01 + ".pt1", p1)
    pm.setAttr(arc01 + ".pt2", p2)
    pm.setAttr(arc01 + ".pt3", p3)
    crvShape = pm.createNode("nurbsCurve", name=name + 'Shape01')
    pm.connectAttr(arc01 + '.outputCurve', crvShape + '.create')
    crvXform = pm.listRelatives(crvShape, p=True)
    pm.delete(crvXform, constructionHistory=True)

    return crvXform[0]


# Create tree curve.
def tree(name, *args):
    curveMake = pm.curve(
        n=name,
        d=1,
        p=[
            (-1, 0, 0),
            (-1, 2, 0),
            (-4, 2, 0),
            (-2, 4, 0),
            (-3, 4, 0),
            (-1, 6, 0),
            (-2, 6, 0),
            (0, 8, 0),
            (2, 6, 0),
            (1, 6, 0),
            (3, 4, 0),
            (2, 4, 0),
            (4, 2, 0),
            (1, 2, 0),
            (1, 0, 0),
            (-1, 0, 0)
        ]
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    pm.rename(shapeNode, curveMake + "shape")
    return curveMake


# Create twoEndArrow curve.
def twoEndArrow(name, *args):
    curveMake = pm.curve(
        name=name,
        d=1,
        p=[
            (0.0, 0.0, -1.0),
            (1.0, 0.0, -1.0),
            (1.0, 0.0, -2.0),
            (3.0, 0.0, 0.0),
            (1.0, 0.0, 2.0),
            (1.0, 0.0, 1.0),
            (-1.0, 0.0, 1.0),
            (-1.0, 0.0, 2.0),
            (-3.0, 0.0, 0.0),
            (-1.0, 0.0, -2.0),
            (-1.0, 0.0, -1.0),
            (0.0, 0.0, -1.0),
        ]
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    control = pm.rename(shapeNode, curveMake + "Shape01")
    return curveMake


# Create Two Point Arc.
def twoPointArc(name, deg, span, r, p1, p2, dv):
    arc01 = pm.createNode("makeTwoPointCircularArc")
    pm.setAttr(arc01 + ".d", deg)
    pm.setAttr(arc01 + ".s", span)
    pm.setAttr(arc01 + ".r", r)
    pm.setAttr(arc01 + ".pt1", p1)
    pm.setAttr(arc01 + ".pt2", p2)
    pm.setAttr(arc01 + ".dv", dv)
    crvShape = pm.createNode("nurbsCurve", name=name + 'Shape01')
    pm.connectAttr(arc01 + '.outputCurve', crvShape + '.create')
    crvXform = pm.listRelatives(crvShape, p=True)
    pm.delete(crvXform, constructionHistory=True)

    return crvXform[0]


# Create cardinalArrow03 curve.
def cardinalArrow03(name, *args):
    curveMake = pm.curve(
        name=name,
        d=1,
        p=[
            (-1.0, 0.0, 3.0),
            (-2.0, 0.0, 3.0),
            (0.0, 0.0, 5.0),
            (2.0, 0.0, 3.0),
            (1.0, 0.0, 3.0),
            (3.0, 0.0, 1.0),
            (3.0, 0.0, 2.0),
            (5.0, 0.0, 0.0),
            (3.0, 0.0, -2.0),
            (3.0, 0.0, -1.0),
            (1.0, 0.0, -3.0),
            (2.0, 0.0, -3.0),
            (0.0, 0.0, -5.0),
            (-2.0, 0.0, -3.0),
            (-1.0, 0.0, -3.0),
            (-3.0, 0.0, -1.0),
            (-3.0, 0.0, -2.0),
            (-5.0, 0.0, 0.0),
            (-3.0, 0.0, 2.0),
            (-3.0, 0.0, 1.0),
            (-1.0, 0.0, 3.0),
        ]
    )
    shapeNode = pm.listRelatives(curveMake, shapes=True)
    control = pm.rename(shapeNode, curveMake + "Shape01")
    return curveMake
