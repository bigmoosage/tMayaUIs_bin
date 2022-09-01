"""

Wrapper for vector maths on selection in Maya.

"""

import math

import maya.cmds as cd
# Maya Mods
import pymel.core as pm
import pymel.core.datatypes as dt
from pymel.core import nodetypes as nt
from random import uniform

# My Mods
from tMayaUIs_bin.maths import maths_vectors

pi = 3.1415926535


class VCT:

    def __init__(self, vcts=None):
        # BASIC VECTORS IF KEYWARG INPUT IS TWO VECTORS IN A LIST [u(x,y,z), v(x,y,z)]
        if vcts is not None and hasattr(vcts, "__iter__"):

            if len(vcts) == 2:
                print('Two Vectors In')
                self.u = vcts[0]
                self.v = vcts[1]
                self.vct = [self.u, self.v]

            else:
                print('Vectors List In')
                self.vct = []
                for vec in vcts:
                    self.vct.append(vec)

        elif pm.ls(sl=True):

            self.sel = pm.ls(sl=True, fl=True)

            # Vectors for two objects in selection.
            if len(self.sel) == 2 and all(hasattr(obj, 'getTranslation') for obj in self.sel):
                print("Two Objects")
                self.u = pm.ls(sl=True)[0].getTranslation()
                self.v = pm.ls(sl=True)[1].getTranslation()
                self.dot = dt.dot(self.u, self.v)
                self.dist = dt.dist(dt.Array([self.u]), dt.Array([self.v]), axis=0)[0]

            elif len(self.sel) == 1:

                if hasattr(self.sel[0], 'getShape'):

                    if pm.objectType(self.sel[0].getShape()) == 'mesh':
                        print('Stored all vtxs of object.')
                        self.obj = self.sel[0]
                        self.objshp = self.sel[0].getShape()
                        self.vtx = self.objshp.vtx
                        self.vct = []
                        for vtx in self.vtx:
                            self.vct.append(vtx.getPosition(space='world'))
                    else:
                        raise Exception('One object selected and it HAS NO VERTS!')

            elif all(hasattr(s, 'connectedVertices') is True for s in self.sel) and self.sel[0].find('.vtx') != -1:
                print('Verts')
                self.vtx = self.sel
                self.vct = []
                for vtx in self.vtx:
                    self.vct.append(vtx.getPosition(space='world'))

            elif all(hasattr(s, 'connectedVertices') is True for s in self.sel) and self.sel[0].find('.e[') != -1:
                print('Edges')
                self.vtx = []
                for v in self.sel:
                    vert = v.connectedVertices()
                    for vert in vert:
                        if vert not in self.vtx:
                            self.vtx.append(vert)
                self.vct = []
                for vtx in self.vtx:
                    self.vct.append(vtx.getPosition(space='world'))

            elif all(hasattr(s, 'connectedVertices') is True for s in self.sel) and self.sel[0].find('.f[') != -1:
                print('Faces')
                self.vtx = []
                for v in self.sel:
                    vert = pm.ls(pm.polyListComponentConversion(v, tv=True), fl=True)
                    for vt in vert:
                        if vt not in self.vtx:
                            self.vtx.append(vt)
                self.vct = []
                for vtx in self.vtx:
                    self.vct.append(vtx.getPosition(space='world'))

            elif hasattr(self.sel[-1], 'getShape'):
                self.vtx = self.sel[:-1]
                self.vct = []
                for vtx in self.vtx:
                    self.vct.append(vtx.getPosition(space='world'))

            else:
                raise Exception('One object selected and it HAS NO VERTS!')

        else:
            raise Exception('Select something, input list of vectors as arg or kwarg vcts=[u,v].')

        # Personal Definitions for Methods.
        if hasattr(self, 'vct'):
            self.ogPos = self.vct
            self.C = dt.Vector(maths_vectors.bboxmid(self.vct))
            self.R = maths_vectors.cradius(self.vct, self.C)
            self.zpos = []
            for vPos in self.vct:
                self.zpos.append(vPos - self.C)
            self.obj = nt.Transform(cd.listRelatives(self.vtx[0].split(".vtx[")[0], parent=True)[0])
            pm.makeIdentity(self.obj, a=True, t=1, r=1, s=1)
            pm.delete(self.obj, ch=True)
            self.objPos = self.obj.getTranslation()
            self.objRot = self.obj.getRotation(quaternion=True)

    def __repr__(self):
        reprString = '%s Vertices from %s' % (len(self.vtx), self.obj)
        return reprString

    @classmethod
    def update(cls):
        """
        Updates the positions of Vertices.
        :return:
        """
        cls()

    def reset(self):
        """
        Resets selected verts back to the position stored on class initialisation.
        :return:
        """
        for pos in range(len(self.vtx)):
            pm.move(
                round(self.ogPos[pos][0], 4),
                round(self.ogPos[pos][1], 4),
                round(self.ogPos[pos][2], 4),
                self.vtx[pos],
                xyz=True, a=True
            )

    def noise(self, amount):
        """
        Randomly translates vertices multiplied by amount value.
        :param amount : Float or Float Vector (0.2 or (0.2,0.2,0.2)):
        :return:
        """
        if hasattr(amount, '__iter__') and len(amount) == 3:
            noiseVal = amount
        elif isinstance(amount, float) or isinstance(amount, int):
            noiseVal = [amount, amount, amount]
        else:
            raise TypeError("Needs either 3 Iterable values or one single number value as arg.")

        for pos in range(len(self.vtx)):
            rand = (uniform(-1, 1) * noiseVal[0], uniform(-1, 1) * noiseVal[1], uniform(-1, 1) * noiseVal[2])
            pm.move(
                self.vct[pos][0] + rand[0],
                self.vct[pos][1] + rand[1],
                self.vct[pos][2] + rand[2],
                self.vtx[pos],
                xyz=True, a=True
            )

    def dot(self):
        self.dot = dt.dot(self.u, self.v)
        return self.dot

    def dist(self):
        self.dist = dt.dist(dt.Array([self.u]), dt.Array([self.v]), axis=0)[0]
        return self.dist

    def newZpos(self, v, vlist):
        zpos = []
        for vct in vlist:
            zpos.append(dt.Point(vct - v))
        return zpos

    # Spherises Verts
    @classmethod
    def spherise(cls, *args):
        """
        Simple Spherise. Takes Positions of Vertices, their centre as their average position and radius from
        averaged magnitude from that centre. Multiplies its unit vectors by the Radius around
        the centre.
        @:return "Spherised"
        """
        self = cls()
        for x in range(len(self.vtx)):
            self.vtx[x].setPosition(
                [
                    (self.C[0] + maths_vectors.uor(self.zpos[x], self.R)[0]),
                    (self.C[1] + maths_vectors.uor(self.zpos[x], self.R)[1]),
                    (self.C[2] + maths_vectors.uor(self.zpos[x], self.R)[2])
                ],
                space='world'
            )
        return "Spherised"

    # Spherise around given point
    @classmethod
    def spheriseAroundPoint(cls, *args):
        """
        Spherises the inputted verts around a specific selected object (USE LOCATOR):
        """
        self = cls()
        centre = cd.xform(cd.ls(sl=True)[-1], q=True, t=True)
        radius = maths_vectors.cradius(self.vct, centre)
        for x in range(len(self.vtx)):
            # centre[2] +
            self.vtx[x].setPosition(
                [
                    centre[0] + maths_vectors.uor(maths_vectors.vbet(centre, self.vct[x]), radius)[0],
                    centre[1] + maths_vectors.uor(maths_vectors.vbet(centre, self.vct[x]), radius)[1],
                    centre[2] + maths_vectors.uor(maths_vectors.vbet(centre, self.vct[x]), radius)[2]
                ],
                space='world'
            )
        return "Spherised around point"

    # Circularises Verts
    @classmethod
    def circularise(cls, op, obj=False, *args):
        """
        Circularises the inputted verts:

        Queries whether vertices are planar or symmetrical across axes:

            2D Case: Vertices are planar across two axes
                'Spherises' Vertices:
                    Vertex Position = Unit Vector around Average position (Centre, c) * Average Magnitude (Radius, r)

            3D Case: Verts are Non-Planar

                1st Phase:
                    Finds axes for Plane to build circle depending on average of points in selection:
                        Gets Vectors above and below each axis by getting their dot product to World Axis.
                        Picks Axes to use based on greatest difference of vectors across each axis (ZY, XZ or XY)
                        Finds Vectors defining those Axes:
                            vBetweenA is a vector between the positive and negative averages of first Axis
                            vBetweenB is a vector between the positive and negative averages of second Axis
                            normalToPlane is a normal vector from Axis Plane defined by vBetweenA and vBetweenB

                2nd Phase:
                    Finds Unit Vectors uA, uN and uB:
                        uA is a Unit Vector on the plane
                        uN is a Unit Normal Vector perpendicular to the plane and A
                        uB is a Unit Vector perpendicular to A and the Normal

                3rd Phase:
                    Gets angle between Vector in and first axis
                    Gets dot between Vector and second axis
                    Based on angle between Vector and whether vector is above or below second axis:
                        Vertex is moved according to parametric equation of 3D circle:
                            x(theta)=c1+rcos(theta)*a1+rsin(theta)*b1
                            y(theta)=c2+rcos(theta)*a2+rsin(theta)*b2
                            z(theta)=c3+rcos(theta)*a3+rsin(theta)*b3
                        Which circularises.
        """
        self = cls()
        print(self)
        if obj is True:
            if "CIRCLELOC01" not in cd.ls(type="transform"):
                cd.spaceLocator(n="CIRCLELOC01")

            locatorPos = nt.Transform("CIRCLELOC01")
            print(self.C)
            self.C = locatorPos.getTranslation()
            print(self.C)
            print(self.R)
            self.R = maths_vectors.cradius(self.vct, self.C)
            print(self.R)
            self.zpos = []
            for vPos in self.ogPos:
                self.zpos.append(vPos - self.C)

        # Takes the zero position and the centre
        # cType = maths_circles.circleType(self.zpos)

        # Sum of X vals
        xA = sum([x[0] for x in self.zpos])

        # Sum of Y vals
        yA = sum([y[1] for y in self.zpos])

        # Sum of Z vals
        zA = sum([z[2] for z in self.zpos])

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

        # Planar across Axes
        if cType == "2D":
            n = 0
            for x in range(len(self.vtx)):
                mVec = dt.Vector(
                    (self.C[0] + maths_vectors.uor(self.zpos[n], self.R)[0]) - self.objPos[0],
                    (self.C[1] + maths_vectors.uor(self.zpos[n], self.R)[1]) - self.objPos[1],
                    (self.C[2] + maths_vectors.uor(self.zpos[n], self.R)[2]) - self.objPos[2]
                )
                self.vtx[x].setPosition(mVec)
                n += 1

            returnString = "Circularised On 2D Plane"
            print(returnString)
            return returnString

        # FINDS VERTICES ACROSS MULTIPLE PLANES
        elif cType == "3D":

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
            for zp in self.zpos:
                # Positive and Negatives across axis around Origin
                # X
                dotX = maths_vectors.dot(zp, axes[0])
                # Y
                dotY = maths_vectors.dot(zp, axes[1])
                # Z
                dotZ = maths_vectors.dot(zp, axes[2])

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
            xAxVal = max([x[0] for x in self.zpos]) - min([x[0] for x in self.zpos])
            yAxVal = max([y[1] for y in self.zpos]) - min([y[1] for y in self.zpos])
            zAxVal = max([z[2] for z in self.zpos]) - min([z[2] for z in self.zpos])
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

            # cType = maths_vectors.circType(self.zpos)
            # posAxisA, negAxisA, posAxisB, negAxisB = maths_vectors.findAxis(
            #     self.C,
            #     self.vtx,
            #     self.zpos,
            #     self.R,
            #     self.objPos,
            #     cType=cType
            # )

            # FINDS VECTORS BETWEEN THE AXES
            if obj is False:
                vBetweenA = maths_vectors.vbet(posAxisA, negAxisA)
                vBetweenB = maths_vectors.vbet(posAxisB, negAxisB)

            elif obj is True:
                vBetweenA = maths_vectors.vbet(self.zpos[0], self.C)
                vBetweenB = maths_vectors.vbet(self.zpos[-1], self.C)
            else:
                raise Exception
            # Normal (90deg) Vector to plane Defined by A and B axes.
            normalToPlane = maths_vectors.cross(vBetweenA, vBetweenB)

            # UNIT VECTORS TO ORIGIN
            # Unit Vector to A
            uA = maths_vectors.uo(vBetweenA)
            # Unit Normal
            uN = maths_vectors.uo(normalToPlane)
            # Secondary Unit Vector perpendicular to uA and Planes Normal Vector
            uB = maths_vectors.uo(maths_vectors.cross(uA, uN))
            n = 0

            if op == "rel":
                for vert in self.vtx:
                    angBetUA = maths_vectors.angBetween(self.zpos[n], uA)
                    dotUB = maths_vectors.dot(self.zpos[n], uB)
                    if dotUB >= 0:
                        theta = angBetUA
                        pm.xform(vert, t=[
                            (self.C[0] + self.R * math.cos(theta) * uA[0] + self.R * math.sin(theta) * uB[0]),
                            (self.C[1] + self.R * math.cos(theta) * uA[1] + self.R * math.sin(theta) * uB[1]),
                            (self.C[2] + self.R * math.cos(theta) * uA[2] + self.R * math.sin(theta) * uB[2])
                        ]
                                 )
                    elif dotUB < 0:
                        theta = angBetUA * -1
                        pm.xform(vert, t=[
                            (self.C[0] + self.R * math.cos(theta) * uA[0] + self.R * math.sin(theta) * uB[0]),
                            (self.C[1] + self.R * math.cos(theta) * uA[1] + self.R * math.sin(theta) * uB[1]),
                            (self.C[2] + self.R * math.cos(theta) * uA[2] + self.R * math.sin(theta) * uB[2])
                        ]
                                 )
                    else:
                        pm.xform(vert, t=[
                            (self.C[0] + self.R * math.cos(0) * uA[0] + self.R * math.sin(0) * uB[0]),
                            (self.C[1] + self.R * math.cos(0) * uA[1] + self.R * math.sin(0) * uB[1]),
                            (self.C[2] + self.R * math.cos(0) * uA[2] + self.R * math.sin(0) * uB[2])
                        ]
                                 )
                    n += 1

            elif op == "abs":
                numOfVerts = len(self.vtx)
                increment = (2 * pi) / numOfVerts
                incList = [increment * x for x in range(numOfVerts)]
                n = 0

                uA
                uB

                for vert in self.vtx:


                    n += 1


    # Linearise Verts
    @classmethod
    def linearise(cls, equal, *args):
        """
        Linearises verts by
        :return:
        """
        self = cls()
        numVerts = len(self.vtx)
        firstIndex = None
        firstV = None
        lastV = None
        lastIndex = None
        startP = min([(t[0] + t[1] + t[2]) for t in self.vct])
        for n in range(numVerts):
            if self.vct[n][0] + self.vct[n][1] + self.vct[n][2] == startP:
                firstV = self.vtx[n]
                firstPos = self.vct[n]
                firstIndex = n
        distances = sorted([maths_vectors.dist(self.vct[firstIndex], self.vct[nv]) for nv in range(numVerts)])
        orderedVerts = []
        orderedPos = []
        for d in distances:
            for n in range(numVerts):
                if maths_vectors.dist(self.vct[firstIndex], self.vct[n]) == d:
                    orderedVerts.append(self.vtx[n])
                    orderedPos.append(self.vct[n])

        nZpos = self.newZpos(firstPos, orderedPos)
        if equal is True:
            distInc = [1.00 / (numVerts - 1) * n for n in range(numVerts)]
            n = 0
            for vert in orderedVerts:
                pm.xform(
                    vert,
                    t=(nZpos[-1] * distInc[n]) + orderedPos[0]
                )
                n += 1

        elif equal is False:
            print(orderedVerts[0])
            print(orderedVerts[-1])
            lineLen = maths_vectors.mag(nZpos[-1])
            n = 0
            for vert in orderedVerts:
                pm.xform(
                    vert,
                    t=(nZpos[-1] * (distances[n] / lineLen)) + orderedPos[0]
                )
                n += 1

        else:
            raise TypeError("\"equal\" keywarg must be bool.")

    @classmethod
    def equal(cls, axis, *args):
        """
        Distributes vertices along line of Specific Axis.
        """
        self = cls()
        if axis == 0:
            ax = [1, 0, 0]
        elif axis == 1:
            ax = [0, 1, 0]
        elif axis == 2:
            ax = [0, 0, 1]
        else:
            raise TypeError("Axis must be 0, 1, 2")
        numVerts = len(self.vtx)
        axPos = sorted([self.vct[n][axis] for n in range(numVerts)])
        minP = min(axPos)
        maxP = max(axPos)
        orderedVerts = []
        for p in axPos:
            for n in range(numVerts):
                if self.vct[n][axis] == p:
                    orderedVerts.append(self.vtx[n])
        oPos = [v.getPosition() for v in orderedVerts]
        d = maxP - minP

        incr = d / (numVerts - 1)

        perP = [incr * x for x in range(numVerts - 1)]

        print(len(orderedVerts))
        print(len(perP))

        n = 0
        for vert in orderedVerts:
            if vert != orderedVerts[-1]:
                indexX = n * (1 - ax[0])
                indexY = n * (1 - ax[1])
                indexZ = n * (1 - ax[2])
                pm.move(
                    oPos[indexX][0] + (perP[n] * ax[0]),
                    oPos[indexY][1] + (perP[n] * ax[1]),
                    oPos[indexZ][2] + (perP[n] * ax[2]),
                    vert, xyz=True
                )
                n += 1

    # Make Planar
    @classmethod
    def planarise(cls, *args):
        self = cls()

        circType = maths_vectors.circType(self.zpos)

        posAxisA, negAxisA, posAxisB, negAxisB = maths_vectors.findAxis(
            self.C,
            self.vtx,
            self.zpos,
            self.R,
            self.objPos,
            cType=circType
        )

        # FINDS VECTORS BETWEEN THE AXES
        a = maths_vectors.vbet(posAxisA, negAxisA)
        b = maths_vectors.vbet(posAxisB, negAxisB)

        # Normal (90deg) Vector to plane Defined by A and B axes.
        normalToPlane = maths_vectors.cross(b, a)
        unitNormal = dt.Vector(maths_vectors.uo(normalToPlane))

        n = 0
        for vert in self.vtx:
            v = self.zpos[n]
            d = v[0] * unitNormal[0] + v[1] * unitNormal[1] + v[2] * unitNormal[2]
            newPoint = v - (d * unitNormal)
            pm.xform(
                vert,
                t=newPoint + self.C,
                ws=True
            )
            n += 1

        # VN1 = pm.MeshVertex(self.vtx[0]).getNormals()[0]
        # VN2 = pm.MeshVertex(self.vtx[-1]).getNormals()[0]

        # return self.C, a + self.C, b + self.C, normalToPlane + self.C, unitNormal + self.C, tVec + self.C
        return self.vtx


    @classmethod
    def testing(cls, *args):
        self = cls()
        circType = maths_vectors.circType(self.zpos)

        posAxisA, negAxisA, posAxisB, negAxisB = maths_vectors.findAxis(
            self.C,
            self.vtx,
            self.zpos,
            self.R,
            self.objPos,
            cType=circType
        )
        # FINDS VECTORS BETWEEN THE AXES
        a = maths_vectors.vbet(posAxisA, negAxisA)
        b = maths_vectors.vbet(posAxisB, negAxisB)

        # Normal (90deg) Vector to plane Defined by A and B axes.
        normalToPlane = maths_vectors.cross(a, b)

        # UNIT VECTORS TO ORIGIN
        # Unit Vector to A
        uA = maths_vectors.uo(a)
        # Unit Normal
        uN = dt.Vector(maths_vectors.uo(normalToPlane))
        # Secondary Unit Vector perpendicular to uA and Planes Normal Vector
        uB = maths_vectors.uo(maths_vectors.cross(uA, uN))

        return maths_vectors.vertsByQuadrant(uA, uB, self.vtx, self.zpos)


# vector $ap = <<A.translateX,A.translateY,A.translateZ>>;
# vector $bp = <<B.translateX,B.translateY,B.translateZ>>;
# vector $C = <<C.translateX,C.translateY,C.translateZ>>;
#
# vector $ehP = cross($bp,$ap);
#
# eh.translateX= $ehP.x;
# eh.translateY= $ehP.y;
# eh.translateZ= $ehP.z;
#
# vector $P = <<loc.translateX,loc.translateY,loc.translateZ>>;
#
# vector $vtp = <<$P.x-$ehP.x,$P.y-$ehP.y,$P.z-$ehP.z>>;
# loc1.translateX = $vtp.x;
# loc1.translateY = $vtp.y;
# loc1.translateZ = $vtp.z;
