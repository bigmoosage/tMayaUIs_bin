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
from functools import partial

# My Mods
from tMayaUIs_bin.maths import maths_vectors

pi = 3.1415926535


class VCT:

    def __init__(self, vcts=None):

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
            raise Exception('Select something, input list of vectors as arg or kwarg (vcts=[]).')

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

def UI(*args):
    myNewWindow = cd.window(title="Noise UI")
    cd.columnLayout(adj=True)
    cd.button(c=partial(cd.deleteUI, myNewWindow))
    cd.setParent('..')
    cd.showWindow(myNewWindow)