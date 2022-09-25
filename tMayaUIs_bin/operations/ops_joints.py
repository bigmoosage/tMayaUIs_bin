"""
Joint Operations
"""

import pymel.core as pm
from pymel.core import datatypes as dt
from pymel.core import nodetypes as nt

from tMayaUIs_bin.manip import dt_namingConvention as nc
from tMayaUIs_bin.maths import maths_vectors as vct
from tMayaUIs_bin.operations import ops_select


def createEqualJoints(jntNum, root=None, end=None, chain=True, oneMore=False, prefix="jnt_", radius=1):
    """
    @selection - list of joints"
    """

    jointsInScene = pm.ls(type="joint")
    selection = ops_select.sel()
    if root is not None and end is not None and all(j in jointsInScene for j in [root, end]):
        root = nt.Joint(root)
        end = nt.Joint(end)
        pass

    elif len(selection) == 2 \
            and selection[0] in jointsInScene \
            and selection[1] in jointsInScene \
            and isinstance(jntNum, int):
        root = nt.Joint(selection[0])
        end = nt.Joint(selection[1])
        print("Joints - Passed.")
        pass
    else:
        raise TypeError("Select two Joints or use kwargs root and end to input joints.")

    rootV = root.getTranslation()
    endV = end.getTranslation()

    V = dt.Vector(vct.vbet(rootV, endV))

    jntName = prefix
    iNum = jntNum + 1
    inc = 1.0 / iNum

    increment = [inc * y for y in range(iNum) if y != 0]
    iterInt = 0

    jointsList = [root]
    pm.select(root, r=True)
    for nJnt in increment:
        if chain is False:
            pm.select(cl=True)
        newPos = (V * nJnt) + rootV
        # pm.select(cl=True)
        if nJnt == increment[-1]:
            newJoint = pm.joint(n="%s%s01" % (jntName, nc.alphabet()[iterInt+1]), p=newPos, radius=radius)
            jointsList.append(newJoint)
            if chain is True:
                pm.parent(end, newJoint)
        else:
            newJoint = pm.joint(n="%s%s01" % (jntName, nc.alphabet()[iterInt+1]), p=newPos, radius=radius)
            jointsList.append(newJoint)
        # pm.select(cl=True)
        iterInt += 1
    jointsList.append(end)
    pm.select(cl=True)
    if oneMore is True:
        if prefix == "bn_sp":
            name = "be_spEnd01"
        else:
            name = "%s%s01" % (jntName, nc.alphabet()[iterInt + 2])
        upperJoint = pm.joint(n=name, p=(V * (1 + increment[0])) + rootV, radius=radius)
        if chain is True:
            pm.parent(upperJoint, end)
        jointsList.append(upperJoint)

    pm.rename(end, "%s%s01" % (prefix, nc.alphabet()[iterInt+1]))

    # if all(j.getTranslation[0] == 0 for j in jointsList) and all(j.getTranslation[2] == 0 for j in jointsList):
    #     pm.joint(root, edit=True, orientJoint='none', zeroScaleOrient=True, children=True)
    # else:
    #     pm.joint(root, edit=True, orientJoint='zyx', secondaryAxisOrient="yup", zeroScaleOrient=True, children=True)

    return jointsList


def selectBound():
    joints = []
    pm.select(hi=True)
    for jnt in pm.ls(type="joint"):
        if pm.objectType(jnt) == "joint" and jnt.split("_")[0] == "bn":
            joints.append(jnt)
    pm.select(joints)


def createControlJoints(nrbRadius=1):
    def visOff(obj):
        pm.setAttr("{}.overrideEnabled".format(obj.getShape()), 1)
        pm.setAttr("{}.overrideVisibility".format(obj.getShape()), 0)

    selection = ops_select.sel()
    pm.select(cl=True)
    faceLocators = []
    if "refShader_jointPosition_surfaceShaderSG01" not in pm.ls(type="shadingEngine"):
        surfaceShader = pm.shadingNode("surfaceShader", asShader=True, n="refShader_jointPosition_surfaceShader01")
        pm.setAttr("{}.outColor".format(surfaceShader), 1, 1, 0)
        shaderGroup = pm.sets(n="refShader_jointPosition_surfaceShaderSG01", renderable=True, noSurfaceShader=True,
                              empty=True)
        pm.connectAttr("{}.outColor".format(surfaceShader), "{}.surfaceShader".format(shaderGroup))
    else:
        shaderGroup = "refShader_jointPosition_surfaceShaderSG01"
    for obj in pm.ls(dag=True):
        if obj == "grp_facialLocators01":
            pm.delete(obj)
    mainGroup = pm.group(n="grp_facialLocators01", em=True)
    for crv in selection:
        if pm.objectType(crv.getShape()) == 'nurbsCurve':
            pm.select(cl=True)
            locGrp = pm.group(n="locGrp_" + "_".join(crv.split("_")[1:]), em=True)
            pm.parent(locGrp, mainGroup)
            name = "_".join(crv.split("_")[1:])
            uVal = 0
            if len(crv.split("_")) > 1 and crv.split("_")[1] in ["l", "r"]:
                locN = 3
            else:
                locN = 5
            for x in range(locN):
                loc = pm.spaceLocator(n="mLoc_{}{}{}".format(name[:-2], nc.alphabet()[x], nc.countString()[0]))
                pm.setAttr("{}.localScaleX".format(loc), 0.1)
                pm.setAttr("{}.localScaleY".format(loc), 0.1)
                pm.setAttr("{}.localScaleZ".format(loc), 0.1)
                visOff(loc)
                motionPath = pm.pathAnimation(loc, crv, n="mp_" + str(loc), fractionMode=True)
                pm.setAttr(motionPath + ".uValue", uVal)
                pm.delete(motionPath + "_uValue")
                adder = (1.0 / (float(locN) - 1.0))
                uVal += adder
                pm.parent(loc, locGrp)
                faceLocators.append(loc)
                jntOff = pm.joint(n="jntOff_{}{}{}".format(name[:-2], nc.alphabet()[x], nc.countString()[0]), rad=0.2)
                jntCtrl = pm.joint(n="bn_{}{}{}".format(name[:-2], nc.alphabet()[x], nc.countString()[0]), rad=0.4)
                ns = pm.sphere(ch=False, radius=nrbRadius)
                nshp = ns[0].getShape()
                pm.parent(nshp, jntCtrl, r=True, shape=True)
                pm.sets(shaderGroup, e=True, forceElement=jntCtrl)
                pm.delete(ns)
                pm.delete(pm.parentConstraint(loc, jntOff))


def jointsOnCurve(nJnt):
    if len(pm.ls(sl=True)) == 1 and pm.objectType(pm.ls(sl=True)[0].getShape()) == 'nurbsCurve':
        crv = pm.ls(sl=True)[0]
    else:
        raise TypeError("Select Curve.")

    increment = [1.0 / float(nJnt) * float(x) for x in range(nJnt)]
    increment.append(1.0)
    joints = []
    for jn in range(nJnt):
        pm.select(cl=True)
        # print(increment[jn])
        joint = pm.joint(n="jnt_onCurve_%s01" % (nc.alphabet()[jn]))
        if jn == 0:
            startJoint = joint
        joints.append(joint)
        motionPath = pm.pathAnimation(joint, crv, n="mp_" + str(crv), fractionMode=True)
        pm.delete(motionPath + "_uValue")
        pm.setAttr(motionPath + ".uValue", increment[jn])
        pm.delete(motionPath)

    pm.select(cl=True)
    endJoint = pm.joint(n="jntEnd_onCurve_end01")
    joints.append(endJoint)
    motionPath = pm.pathAnimation(endJoint, crv, n="mp_" + str(crv), fractionMode=True)
    pm.delete(motionPath + "_uValue")
    pm.setAttr(motionPath + ".uValue", 1)
    pm.delete(motionPath)

    for j in range(len(joints)):
        if j != len(joints) - 1:
            pm.parent(joints[j + 1], joints[j])

    # if all(j.getTranslation[0] == 0 for j in joints) and all(j.getTranslation[2] == 0 for j in joints):
    #     pm.joint(startJoint, edit=True, orientJoint='none', zeroScaleOrient=True, children=True)
    # else:
    #     pm.joint(startJoint, edit=True, orientJoint='zyx', secondaryAxisOrient="yup", zeroScaleOrient=True, children=True)


def rmvInflu():
    pm.select(hi=True)
    for s in ops_select.sel():
        for conn in pm.listConnections(s):
            if pm.nodeType(conn) == 'skinCluster':
                skin = conn
                print(skin)
                break
        if pm.objectType(s) == "joint":
            print(s)
            pm.skinCluster("skinCluster2", e=True, ri=s)


def jointInPos(radius=1, nrbs=True):
    selection = ops_select.sel()
    pm.select(cl=True)
    if "refShader_jointPosition_surfaceShaderSG01" not in pm.ls(type="shadingEngine"):
        surfaceShader = pm.shadingNode("surfaceShader", asShader=True, n="refShader_jointPosition_surfaceShader01")
        pm.setAttr("{}.outColor".format(surfaceShader), 1, 1, 0)
        shaderGroup = pm.sets(n="refShader_jointPosition_surfaceShaderSG01", renderable=True, noSurfaceShader=True,
                              empty=True)
        pm.connectAttr("{}.outColor".format(surfaceShader), "{}.surfaceShader".format(shaderGroup))
    else:
        shaderGroup = "refShader_jointPosition_surfaceShaderSG01"

    jntCtrl = pm.joint(n="bn_jointNrbs01", radius=0.25)

    if nrbs == True:
        nsphere = pm.sphere(n="nrbsSphere_jointNrbs01", r=radius, ch=False)
        nshp = nsphere[0].getShape()
        pm.parent(nshp, jntCtrl, r=True, shape=True)
        pm.sets(shaderGroup, e=True, forceElement=jntCtrl)
        pm.delete(nsphere)

    if len(selection) == 1:
        try:
            pm.xform(jntCtrl, t=selection[0].getPosition())
        except AttributeError:
            print("No \'getPosition\'")
        try:
            pm.delete(pm.parentConstraint(selection[0], jntCtrl))
        except AttributeError:
            print("No \'getTranslation\'")

    else:
        pm.warning("If you wanted to move to a given position, select just one object or vert etc.")

    pm.select(selection[0])


def dupeAndSwap(x=-1, y=1, z=1):
    jntSel = ops_select.sel()
    if all(pm.objectType(jnt) == "joint" for jnt in jntSel):

        for jnt in jntSel:

            pm.select(cl=True)

            jntPos = jnt.getTranslation()
            jntOrientation = jnt.getOrientation()
            jntName = jnt.split("_")

            if jntName[1] == "l":
                jntName[1] = "r"
                newName = "_".join(jntName)

            elif jntName[1] == "r":
                jntName[1] = "l"
                newName = "_".join(jntName)

            else:
                newName = "jnt_swapped01"

            dupedJoint = pm.joint(n=newName, p=[jntPos[0] * x, jntPos[1] * y, jntPos[2] * z])
            dupedJoint.setRadius(jnt.getRadius())
            dupedJoint.setOrientation(jntOrientation)


def jointOnVertex(radius=1):
    vertSel = ops_select.sel()
    pm.select(cl=True)
    iterNum = 0
    for vert in vertSel:
        vpos = vert.getPosition()

        pm.joint(n="jnt_onVert{}{}".format(nc.alphabet()[iterNum], nc.countString()[0]), p=vpos, radius=radius)

        pm.select(cl=True)

        iterNum += 1
