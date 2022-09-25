"""
Scripts for selection queries in Maya
Tom Wood 2020
"""

import maya.cmds as cd
import pymel.core as pm
from tMayaUIs_bin.maths import maths_vectors as vct

# Returns flattened selection
def sel():
    objs = pm.ls(sl=True, fl=True)
    return objs


# Returns xform of objects inputted - can use qXform(sel())
def qXform(objs):
    v = []
    if len(objs) > 1:
        for x in objs:
            selectionPosition = pm.xform(x, t=True, a=True, q=True)
            selectionPositionList = (selectionPosition)
            v.append(selectionPositionList)
        return v
    else:
        v = pm.xform(objs, t=True, q=True)
        return v


# Converts objects to verts and stores V
def convToVerts(objs):
    return pm.ls(pm.polyListComponentConversion(objs, tv=True), fl=True)


# Gets the position of inputted verts
def vPos(verts):
    v = []
    for x in verts:
        selectionPosition = pm.pointPosition(x, w=True)
        selectionPositionList = (selectionPosition)
        v.append(selectionPositionList)
    return v


# Queries seltype and returns either objects or vertex positions based on poly or not.
def seltype():
    s = sel()
    cv = convToVerts(s)
    if not cv:
        print("Objs")
        return s, qXform(s)
    else:
        print("Vertices")
        return cv, vPos(cv)

def centreAndBbox():
    s=sel()
    v=qXform(s)
    c = vct.bBoxMid(v)
    b = vct.bBox(v)
