"""
nSpine Creator
"""

import math

import maya.cmds as cd
import pymel.core as pm
from pymel.core import datatypes as dt
from pymel.core import nodetypes as nt

from tMayaUIs_bin.objects import obj_curves
from tMayaUIs_bin.operations import ops_joints
from tMayaUIs_bin.operations import ops_operations


# Create Bound Chain from two Joints
def createNSpine(hip, chest):
    if len(hip) == 3 and len(chest) == 3:
        if all(isinstance(v, float) for v in hip) and all(isinstance(v, float) for v in hip):
            startV = dt.Vector(hip)
            endV = dt.Vector(chest)
        else:
            raise TypeError("Check Values are floats.")
    else:
        raise TypeError("Check both args are 3 numbers as tuple or list.")

    result = pm.promptDialog(
        title='Number of Joints',
        message='ODD Num Joints:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel',
        style='integer')

    if result == 'OK':
        nJoints = int(pm.promptDialog(query=True, text=True))
        if nJoints % 2 != 0:
            pass
        else:
            raise ValueError("Needs odd number of joints.")
    else:
        print("Cancelled.")
        return

    # Group Hierarchy
    spineHolder = cd.group(n="grp_holder01", em=True)
    globalTransform = cd.group(n="grp_globalXform01", em=True)
    controlGrp = cd.group(n="grp_controls01", em=True)
    jointGrp = cd.group(n="grp_joints01", em=True)
    ikGrp = cd.group(n="grp_iks01", em=True)
    noXform = cd.group(n="grp_noXform01", em=True)

    cd.parent(controlGrp, jointGrp, ikGrp, globalTransform)
    cd.parent(noXform, globalTransform, spineHolder)

    cd.select(cl=True)
    jCtrlHip = pm.joint(p=startV, n="jntCtrl_hips01", radius=3)
    cd.select(cl=True)
    jCtrlChest = pm.joint(p=endV, n="jntCtrl_chest01", radius=3)
    cd.select(cl=True)
    jDrvStart = pm.joint(p=startV, n="jDrv_spA01", radius=1)
    cd.select(cl=True)
    jDrvChest = pm.joint(p=endV, n="jDrv_Chest01", radius=1)
    cd.select(cl=True)
    bndStart = pm.joint(p=startV, n="bn_spA01", radius=2)
    cd.select(cl=True)
    bndEnd = pm.joint(p=endV, n="bn_spChest01", radius=2)
    cd.select(cl=True)

    driverChain = ops_joints.createEqualJoints(nJoints, root=jDrvStart, end=jDrvChest, chain=True, oneMore=True,
                                               prefix="jDrv_sp", radius=1)
    pm.select(cl=True)
    boundChain = ops_joints.createEqualJoints(nJoints, root=bndStart, end=bndEnd, chain=False, oneMore=False,
                                              prefix="bn_sp", radius=2)

    positions = [nt.Joint(j).getTranslation(space="world") for j in driverChain]
    spikCurve = pm.curve(p=positions, d=3, n="crv_spik_spine01")
    splineIk = pm.ikHandle(n="spik_spine01", curve=spikCurve, startJoint=driverChain[0], endEffector=driverChain[-1],
                           ccv=False,
                           pcv=False, rootOnCurve=True, sol="ikSplineSolver")
    print(splineIk)

    for jnt in range(len(boundChain)):
        pm.pointConstraint(driverChain[jnt], boundChain[jnt])

    pm.select(cl=True)
    pm.skinCluster(jCtrlHip, jCtrlChest, spikCurve, n='skin_spineCrv01', dr=4.0)

    # Aim Locators
    aimGroups = []
    locators = []
    for jnt in range(len(boundChain)):
        locator = cd.spaceLocator(n="aimLoc_%s" % boundChain[jnt].split("_")[1])
        locators.append(locator)
        locGrp = cd.group(locator, n="grpOffset_%s" % boundChain[jnt].split("_")[1])
        aimGroups.append(locGrp)
        cd.move(0, 0, 5, "aimLoc_%s" % boundChain[jnt].split("_")[1])
        pm.delete(pm.parentConstraint(driverChain[jnt], locGrp))
        pm.parent(locGrp, driverChain[jnt])

    # Aim Constraints
    for x in range(len(boundChain)):
        pm.aimConstraint(locators[x], boundChain[x], offset=[0, 0, 0], weight=1, aimVector=[0, 0, 1],
                         upVector=[0, 1, 0], worldUpType="object", worldUpObject=driverChain[x + 1])

    # Create Controls
    chestControl = obj_curves.box("ctrl_chest01")
    hipControl = obj_curves.box("ctrl_hip01")
    cogControl = obj_curves.arrow("ctrl_cog01")

    pm.delete(pm.parentConstraint(driverChain[-2], chestControl))
    pm.delete(pm.parentConstraint(driverChain[0], hipControl))

    pm.makeIdentity("ctrl_chest01", t=1, r=1, s=1, a=1)

    midPoint = (jCtrlHip.getTranslation() + jCtrlChest.getTranslation()) / 2

    pm.scale(pm.move(midPoint[0], midPoint[1], midPoint[2] - 5, pm.rotate(cogControl, 0, 0, 180)), 0.6, 1.0, 0)
    pm.makeIdentity("ctrl_cog01", t=1, r=1, s=1, a=1)
    pm.xform("ctrl_cog01", pivots=jCtrlHip.getTranslation())
    pm.parent("ctrl_hip01", "ctrl_cog01")
    pm.parent("ctrl_chest01", "ctrl_cog01")

    # Connect Joint Controls to Crv Controls
    pm.parentConstraint(hipControl, jCtrlHip)
    pm.parentConstraint(chestControl, jCtrlChest)

    # Add to holder groups
    pm.parent(splineIk[0], ikGrp)
    pm.parent(cogControl, controlGrp)
    pm.parent(jCtrlHip, jCtrlChest, driverChain[0], jointGrp)
    pm.parent(spikCurve, noXform)
    for j in boundChain:
        pm.parent(j, jointGrp)

    # NODES
    hipPlus = cd.createNode("plusMinusAverage", n="util_plus_hipsCog01")
    chestPlus = cd.createNode("plusMinusAverage", n="util_plus_chestCog01")
    hipChestAvg = cd.createNode("plusMinusAverage", n="util_avg_hipsChest")
    cd.setAttr("%s.operation" % hipChestAvg, 3)

    cd.connectAttr("%s.rotateY" % hipControl, "%s.input1D[0]" % hipPlus)
    cd.connectAttr("%s.rotateY" % cogControl, "%s.input1D[1]" % hipPlus)
    cd.connectAttr("%s.rotateY" % cogControl, "%s.input1D[0]" % chestPlus)
    cd.connectAttr("%s.rotateY" % chestControl, "%s.input1D[1]" % chestPlus)

    cd.connectAttr("%s.output1D" % hipPlus, "%s.input1D[0]" % hipChestAvg)
    cd.connectAttr("%s.output1D" % chestPlus, "%s.input1D[1]" % hipChestAvg)

    cd.connectAttr("%s.output1D" % hipPlus, "%s.rotateY" % aimGroups[0])
    cd.connectAttr("%s.output1D" % chestPlus, "%s.rotateY" % aimGroups[-1])
    cd.connectAttr("%s.output1D" % hipChestAvg, "%s.rotateY" % aimGroups[int(math.floor(len(aimGroups)/2))])

    iterNum = 0
    avgNodes = []
    # Loops through aim groups
    for aims in aimGroups:
        if iterNum != int(math.floor(len(aimGroups)/2)) and iterNum != 0 and iterNum != len(aimGroups) - 1:
            plusNode = cd.createNode("plusMinusAverage", n="util_avg_%s" % aims.split("_")[-1])
            cd.setAttr("%s.operation" % plusNode, 3)
            cd.connectAttr("%s.output1D" % plusNode, "%s.rotateY" % aims)
            avgNodes.append(plusNode)
        iterNum += 1

    if len(avgNodes) > 1:
        cd.connectAttr("%s.output1D" % hipPlus, "%s.input1D[1]" % avgNodes[0])
        cd.connectAttr("%s.output1D" % chestPlus, "%s.input1D[0]" % avgNodes[-1])

    # CHANGE COLOURS
    ops_operations.overrideColour(cogControl, [1.0, 1.0, 0.0])
    ops_operations.overrideColour(hipControl, [1.0, 1.0, 0.0])
    ops_operations.overrideColour(chestControl, [1.0, 1.0, 0.0])
    ops_operations.overrideColour(boundChain, [0.0, 0.0, 1.0])
    ops_operations.overrideColour(driverChain, [1.0, 0.0, 0.0])
    ops_operations.overrideColour(jCtrlHip, [0.0, 1.0, 1.0])
    ops_operations.overrideColour(jCtrlChest, [0.0, 1.0, 1.0])
