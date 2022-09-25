"""
Collection of scripts for actions on objects.
Tom Wood 2020
"""

# Maya mods.

# noinspection PyUnresolvedReferences
import maya.cmds as cd
# noinspection PyUnresolvedReferences
import pymel.core as pm
# noinspection PyUnresolvedReferences
from pymel.core import nodetypes as nt

# My mods.
from tMayaUIs_bin.objects import obj_curves
from tMayaUIs_bin.operations import ops_select




def unlockAttrs():
    attrlist = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v']

    for s in ops_select.sel():
        for a in attrlist:
            pm.setAttr(s + a, k=True)
            pm.setAttr(s + a, lock=False)


# Viewport Object Hide or Show.
def componentHideShow(type, v):
    view = cd.getPanel(wf=True)
    if 'modelPanel' in view:
        pass
    else:
        view = 'modelPanel4'
    qType = {type: 1}
    if type == 'allOff':
        cd.modelEditor(view, e=True, allObjects=0)
    elif type == 'allOn':
        cd.modelEditor(view, e=True, allObjects=1)
    elif type == 'polysOnly':
        cd.modelEditor(view, e=True, allObjects=0)
        cd.modelEditor(view, e=True, polymeshes=1)
    elif type == 'curvesOnly':
        cd.modelEditor(view, e=True, allObjects=0)
        cd.modelEditor(view, e=True, nurbsCurves=1)
    else:
        state = cd.modelEditor(view, q=True, **qType)
        if state == 1:
            changeflag = {type: 0}
            cd.modelEditor(view, e=True, **changeflag)
        else:
            changeflag = {type: 1}
            cd.modelEditor(view, e=True, **changeflag)


# Matches two objects transforms T and R by a parent Constraint
def matcher(*args):
    selection = cd.ls(sl=True)
    cd.delete(cd.parentConstraint(selection[0], selection[1]))


# Creates rig Hierarchy in Groups.
def createRigNodes():
    groupN = ["RIG_charName01", "globalMove01", "joints01", "iks01",
              "controlObjects01", "toTransform01", "trnsToShow01", "trnsToHide01",
              "model01", "blendShapes01", "extraNodes01", "xtraToShow01", "xtraToHide01"]
    groups = []
    for g in groupN:
        grp = cd.group(em=True, w=True, n=g)
        keyableAttr = cd.listAttr(grp, r=True, k=True)
        if grp != "globalMove01":
            for k in keyableAttr:
                if k != "visibility":
                    cd.setAttr(grp + "." + k, lock=True, k=False, cb=False)

    cd.parent("trnsToShow01", "trnsToHide01", "toTransform01")
    cd.parent("joints01", "iks01", "controlObjects01", "toTransform01", "globalMove01")
    cd.parent("xtraToShow01", "xtraToHide01", "extraNodes01")
    cd.parent("globalMove01", "model01", "blendShapes01", "extraNodes01", "RIG_charName01")


# TurkeyFucker
# Changes Colour of wireframe or curve via drawing overrides.
def curveColourChanger(colourSlider):
    selection = pm.ls(sl=True)
    colour = pm.colorSliderGrp(colourSlider, query=True, rgbValue=True)
    for x in selection:
        if pm.objectType(x) != "joint":
            for shp in x.getShapes():
                cd.setAttr(shp + ".overrideEnabled", 1)
                cd.setAttr(shp + ".overrideRGBColors", 1)
                cd.setAttr(shp + ".overrideColorRGB", colour[0], colour[1], colour[2])
        else:
            cd.setAttr(x + ".overrideEnabled", 1)
            cd.setAttr(x + ".overrideRGBColors", 1)
            cd.setAttr(x + ".overrideColorRGB", colour[0], colour[1], colour[2])


def overrideColour(objects, rgb):
    if not isinstance(objects, list):
        objects = [objects]
    objects = [nt.Transform(obj) for obj in objects]
    R = rgb[0]
    G = rgb[1]
    B = rgb[2]
    for x in objects:
        if pm.objectType(x) != "joint":
            for shp in x.getShapes():
                cd.setAttr(shp + ".overrideEnabled", 1)
                cd.setAttr(shp + ".overrideRGBColors", 1)
                cd.setAttr(shp + ".overrideColorRGB", R, G, B)
        else:
            cd.setAttr(x + ".overrideEnabled", 1)
            cd.setAttr(x + ".overrideRGBColors", 1)
            cd.setAttr(x + ".overrideColorRGB", R, G, B)



# deleteRig method.
def deleteRig(rigsList):
    trans = pm.ls(typ="transform")
    selectInList = pm.textScrollList(rigsList, q=True, si=True)[0].split('|')[0]
    print(selectInList)
    for t in trans:
        if t == selectInList:
            pm.lockNode(t, lock=False)
            allRig = pm.listRelatives(t, ad=True)
            for l in allRig:
                pm.lockNode(l, lock=False)
            pm.delete(allRig)
            pm.delete(t)
    rigListRefresh(rigsList)


# grpcreate method.
def grpcreate(controls, name):
    tiers = {}

    for t in controls:

        if t[0].getValue() == 1:
            tiers[t[2]] = pm.group(n=t[1].getText(), em=True, w=True)

    man = obj_curves.man(name.getText())

    pm.parent(man, str(tiers.get('tier')))

    pm.reorder(man, relative=-4)

    for x, y in tiers.items():

        if x != 'tier':
            pm.parent(y, tiers.get(str(x)[:-1]))

        pm.lockNode(y, lock=True)

    pm.lockNode(man, lock=True)


# Creates line between two selected objects.
def line(*args):
    # Two Object Selection
    selection = cd.ls(sl=True, fl=True)

    # Raises exception to method if not exactly two objects selected
    if not len(selection) == 2:
        raise Exception('Method requires exactly two objects to be selected')

    # Position of First Obj
    objAPosition = cd.xform(selection[0], q=True, t=True)

    # Position of Second Obj
    objBPosition = cd.xform(selection[1], q=True, t=True)

    # Create Line (Curve with Degree 1) between objects
    curveBetween = cd.curve(n="crv_betweenReference01", d=1, p=[objAPosition, objBPosition])
    curveBetweenShape = cd.listRelatives(curveBetween, shapes=True)  # Finds shape node of curve
    renamedShape = cd.rename(curveBetweenShape, "crv_betweenReference01Shape")  # Renames shape node

    # Create clusters on curve points
    cd.select(curveBetween + ".cv[0]")  # Select first CV
    clusterA = cd.cluster(n="dfmr_clusterFollowA01")  # Create cluster on selected CV
    cd.select(curveBetween + ".cv[1]")  # Select second CV
    clusterB = cd.cluster(n="dfmr_clusterFollowB01")  # Create cluster on selected CV

    # Constrain clusters to respective objects
    cd.pointConstraint(selection[0], clusterA)
    cd.pointConstraint(selection[1], clusterB)

    # Change colour of curve between objects on shape node
    cd.setAttr(renamedShape + ".overrideEnabled", 1)  # Sets colour override to on
    cd.setAttr(renamedShape + ".overrideRGBColors", 1)  # Sets colour override to RGB
    cd.setAttr(renamedShape + ".overrideColorRGB", 1, 0.2, 0.01)  # Sets override colour

    # Group and hide for organisation
    clusterGrp = cd.group(clusterA, clusterB, n="crv_betweenClusters01")  # Group clusters
    cd.setAttr(clusterGrp + ".visibility", 0)  # Set cluster group to hidden
    cd.group(clusterGrp, curveBetween, n="grp_curveBetweenElements01")  # Group all elements of constructions.


# lockunlock method.
def lockunlock(rigsList, button):
    locking = {}
    buttonLabel = pm.button(button, q=True, l=True)
    if buttonLabel == 'Lock':
        locking = {'lock': True}
    elif buttonLabel == 'Unlock':
        locking = {'lock': False}
    rigName = pm.textScrollList(rigsList, q=True, si=True)[0].split('|')[0]
    rigContents = pm.listRelatives(rigName, ad=True, type='transform')
    pm.lockNode(rigName, **locking)
    for r in rigContents:
        pm.lockNode(r, **locking)
    rigListRefresh(rigsList)


# Parents shape nodes underneath Transform node of last selected object
def parentCurve(*args):
    selection = cd.ls(sl=True)
    objs = selection[0:-1]
    for ident in objs:
        cd.makeIdentity(ident, a=1, t=1, r=1, s=1)
    parent = selection[-1]
    cd.makeIdentity(parent, a=1, t=1, r=1, s=1)
    for o in objs:
        selShapes = cd.listRelatives(o, s=True)
        cd.parent(selShapes, parent, s=True, r=True)
        cd.delete(o)
        cd.select(cl=True)


# parentOrder method.
def parentOrder(op):
    s = pm.ls(sl=True, fl=True)
    for x in range(0, (len(s) - 1)):
        if op == "p":
            pm.parent(s[x], s[x + 1])
        elif op == "unp":
            pm.parent(s[x], w=True)


# repeatableRigNodes method.
def repeatableRigNodes(dict, check):
    dI = dict.values()
    cd.group(n=dI[0][1], em=True)
    for x in range(1, len(check), 1):
        if cd.checkBox(check[x], q=True, v=True):
            group = cd.group(n=dI[x][1], em=True)


# rigListRefresh method.
def rigListRefresh(rigsList):
    trans = pm.ls(typ="transform")
    pm.textScrollList(rigsList, edit=True, ra=True)
    lock = "LOCKED"
    for t in trans:
        if t.find('RIG_') == 0:
            splitter = t.split('|')
            if len(splitter) == 1:
                lockState = pm.lockNode(splitter, q=True)
                if lockState == [True]:
                    lock = "LOCKED"
                elif lockState == [False]:
                    lock = "UNLOCKED"
                listText = splitter[0] + '|' + lock
                pm.textScrollList(rigsList, edit=True, append=listText)


def offsetGrp(*args):
    obj = pm.ls(sl=True)[0]

    objOffset = pm.group(n='grp_' + '_'.join(obj.split('_')[1:]), em=True)

    pm.delete(pm.parentConstraint(obj, objOffset))

    pm.parent(obj, objOffset)
