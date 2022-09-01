"""
Script to hold gui windows for objfunctions.
Tom Wood 2020
"""

import csv
import os
import random
# Built-ins import
from functools import partial

# Imports mayaCommands into Python
import maya.cmds as cd
import maya.mel as melE
import pymel.core as pm

from tMayaUIs_bin.gui import gui_styles as qts
# My imports
from tMayaUIs_bin.manip import dt_colour
from tMayaUIs_bin.manip import dt_rignames
from tMayaUIs_bin.manip import dt_string
from tMayaUIs_bin.maths import maths_vectors
from tMayaUIs_bin.operations import ops_operations
from tMayaUIs_bin.operations import ops_select as select

seed = random.seed(a=256)

dataFolder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
dataFolder = dataFolder.replace("\\", "/")


# ------------------ #
#   GLOBAL METHODS   #
# ------------------ #
def dockCorrect(inName):
    corrected = inName.split("|")
    corrected[0] = "MayaWindow"
    return "|".join(corrected)


def lt_basicButtons(parentIn, uiType="win"):
    buttonCol = cd.columnLayout(adj=True, parent=parentIn)
    qts.Style.SetStyle(widget=cd.button(l="Delete History", c="cd.delete(ch=True)", parent=buttonCol),
                       tColour="rgb(250,222,180)")
    qts.Style.SetStyle(widget=cd.button(l="Centre Pivot", c="cd.CenterPivot()", parent=buttonCol),
                       tColour="rgb(210,230,222)")
    qts.Style.SetStyle(
        widget=cd.button(l="Freeze xForms", c="cd.makeIdentity(a=True,t=True,r=True,s=True)", parent=buttonCol),
        tColour="rgb(200,222,230)")
    cd.setParent("..")


# channelBoxAttrs method.
def lt_lockUnlockChannelBoxAttributes(parentIn, uiType="win"):
    def checkSetValues():

        if uiType == "dock":
            correctedList = []
            for checks in checkBoxes:
                correction = dockCorrect(checks)
                correctedList.append(correction)
            checkboxes = correctedList
        else:
            checkboxes = checkBoxes

        s = select.sel()

        if len(s) == 1:

            try:

                for ch in checkboxes:
                    a = pm.checkBox(ch, q=True, l=True)

                    pm.checkBox(ch, edit=True, value=not pm.getAttr(select.sel()[0] + '.' + a, lock=True))

            except TypeError:

                pass

        elif len(s) > 1:

            try:

                for ch in checkboxes:
                    pm.checkBox(ch, e=True, v=True)

            except TypeError:

                pass

        else:

            pass

    def attrLockUnlock(a, v):

        s = select.sel()
        for s in s:
            pm.setAttr(s + '.' + a, k=v)
            pm.setAttr(s + '.' + a, lock=not v)

    def unlockAll(v):

        attrlist = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v']

        for s in select.sel():
            for a in attrlist:
                pm.setAttr(s + a, k=True)
                pm.setAttr(s + a, lock=False)

        checkSetValues()

    # Variable Defs
    attrs = {
        'Translation': ['tx', 'ty', 'tz'],
        'Rotation': ['rx', 'ry', 'rz'],
        'Scale': ['sx', 'sy', 'sz'],
        'Visibility': ['v']
    }

    checkBoxes = []

    rh = 20

    """
    UI START
    """

    column = pm.columnLayout(adj=True, parent=parentIn)

    pm.text(font='boldLabelFont', l='Lock/Hide CBox Attrs', parent=column)
    cd.separator(style="none", h=5, parent=column)
    for x, y in attrs.items():
        pm.rowLayout(h=rh, nc=4, cw4=[50, 40, 40, 40], parent=column, adj=1)
        pm.text(l=x + ': ', h=rh, width=50)
        if len(y) == 3:
            checkBoxes.append(
                pm.checkBox(l=y[0], ann=y[0], h=rh, width=40, cc=partial(attrLockUnlock, y[0])).setValue(1))
            checkBoxes.append(
                pm.checkBox(l=y[1], ann=y[0], h=rh, width=40, cc=partial(attrLockUnlock, y[1])).setValue(1))
            checkBoxes.append(
                pm.checkBox(l=y[2], ann=y[0], h=rh, width=40, cc=partial(attrLockUnlock, y[2])).setValue(1))
        elif len(y) == 1:
            checkBoxes.append(
                pm.checkBox(l=y[0], ann=y[0], h=rh, width=40, cc=partial(attrLockUnlock, y[0])).setValue(1))
            pm.text(l="", width=40)
            pm.text(l="", width=40)
        pm.setParent('..')

    pm.button(l='Unlock and Show All', parent=column, c=unlockAll)

    pm.setParent('..')
    pm.setParent('..')

    sjob = pm.scriptJob(e=['SelectionChanged', checkSetValues])

    return sjob


# connectAttributes method.
def lt_connectAttributes(parentIn, uiType="win"):
    def conn(obj1tf, firstattrtf, obj2tf, secondattrtf, v):

        if uiType == "dock":
            obj1tf = dockCorrect(obj1tf)
            firstattrtf = dockCorrect(firstattrtf)
            obj2tf = dockCorrect(obj2tf)
            secondattrtf = dockCorrect(secondattrtf)

        pm.connectAttr(
            pm.textField(obj1tf, q=True, text=True) + '.' + pm.textField(firstattrtf, q=True, text=True),
            pm.textField(obj2tf, q=True, text=True) + '.' + pm.textField(secondattrtf, q=True, text=True))

    def onselection(obj1tf, obj2tf, v):

        if uiType == "dock":
            obj1tf = dockCorrect(obj1tf)
            obj2tf = dockCorrect(obj2tf)

        if len(select.sel()) == 2:
            pm.textField(obj1tf, edit=True, text=select.sel()[0])
            pm.textField(obj2tf, edit=True, text=select.sel()[1])

    def breakAllConnections(v):

        attrlist = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v']
        for s in select.sel():
            for a in attrlist:
                melE.eval("CBdeleteConnection \"%s%s\";" % (s, a))

    def makeNode(mNodeType, v):

        pm.createNode(mNodeType, name='util_' + mNodeType + '01')

    tfw = 110
    column = pm.columnLayout(adj=True, parent=parentIn)
    pm.text(l="Connect Attrs", parent=column, font="boldLabelFont")
    cd.separator(style="none", h=5, parent=column)
    row1 = pm.rowLayout(adj=1, nc=2, parent=column)
    pm.setParent("..")
    row2 = pm.rowLayout(adj=1, nc=2, parent=column)
    pm.setParent("..")
    connButton = pm.button(l='Connect', parent=column)
    pm.button(l="Break", parent=column, c=breakAllConnections)
    pm.setParent("..")

    obj1 = pm.textField('obj1TFCnnWin', text='obj1', parent=row1, width=tfw)
    obj2 = pm.textField('obj2TFCnnWin', text='obj2', parent=row2, width=tfw)
    firstAttr = pm.textField('attr1TFCnnWin', text='attr1', parent=row1, width=tfw)
    secondAttr = pm.textField('attr2TFCnnWin', text='attr2', parent=row2, width=tfw)

    pm.button(connButton, edit=True, c=partial(conn, obj1, firstAttr, obj2, secondAttr))

    sJob = pm.scriptJob(e=['SelectionChanged', partial(onselection, obj1, obj2, 'v')])

    return sJob


# Assign variable named frameColour to function in Maya:
def lt_wireframeColourChanger(parentIn, uiType="win"):

    def wireframeChange(rgbSlider, *args):

        if uiType == "dock":

            rgbSlider = dockCorrect(rgbSlider)

        ops_operations.curveColourChanger(rgbSlider)

    frameColourCol = cd.columnLayout(adj=True, parent=parentIn, width=50)
    cd.text(l='Set wireFrame colour', parent=frameColourCol, font="boldLabelFont")
    cd.separator(style="none", h=5, parent=frameColourCol)
    curveColourRGB = cd.colorSliderGrp(l='RGB', rgb=(0, 0, 0), adj=1, columnAlign=(1, 'left'),
                                       parent=frameColourCol,
                                       ann='fcs')
    cd.button(l='Set Colour', c=partial(wireframeChange, curveColourRGB), parent=frameColourCol)
    cd.setParent('..')


# hideViewPortLayout method.
def lt_showHideViewportElements(parentIn, uiType="win"):
    buttonDict = {'Joints': ['joints', (0.237, 0.028, 0.068)],
                  'Curves': ['nurbsCurves', (0.4, 0.237, 0.068)],
                  'Polys': ['polymeshes', (0.068, 0.028, 0.237)],
                  'Cameras': ['cameras', (0.237, 0.237, 0.068)],
                  'ImgPlanes': ['imagePlane', (0.068, 0.237, 0.237)],
                  'Deformers': ['deformers', (0.237, 0.028, 0.237)],
                  'Locators': ['locators', (0.6, 0.4, 0.1)],
                  'IKs': ['ikHandles', (0.6, 0.1, 0.2)],
                  'nCloth': ['nCloths', (0.3, 0.2, 0.2)],
                  'NurbsSurf': ['nurbsSurfaces', (0.3, 0.2, 0.4)]
                  }
    primaryButtons = ['Polys', 'Joints', 'Curves', 'Locators']
    secondaryButtons = ['Cameras', 'ImgPlanes', 'Deformers', 'IKs', 'nCloth', 'NurbsSurf']

    mainColumn = pm.columnLayout(adj=True, parent=parentIn)

    bigButtonGrid = cd.columnLayout(parent=mainColumn, adj=True)
    smallButtonGrid = cd.gridLayout(nc=3, cwh=(80, 30), parent=mainColumn)
    for pb in primaryButtons:
        for x, y in buttonDict.items():
            if x == pb:
                cd.button(l=x, bgc=y[1], height=30, c=partial(ops_operations.componentHideShow, y[0]),
                          parent=bigButtonGrid)
    for sb in secondaryButtons:
        for x, y in buttonDict.items():
            if x == sb:
                cd.button(l=x, bgc=y[1], c=partial(ops_operations.componentHideShow, y[0]), parent=smallButtonGrid)
    cd.gridLayout(nc=2, cwh=(120, 30), parent=mainColumn)
    cd.button(l='Polys Alone', bgc=(0, 0.2, 0.3), c=partial(ops_operations.componentHideShow, 'polysOnly'))
    cd.button(l='Curves Alone', bgc=(0, 0.1, 0.4), c=partial(ops_operations.componentHideShow, 'curvesOnly'))
    cd.button(l='All On', bgc=(0.8, 0.8, 0.8), c=partial(ops_operations.componentHideShow, 'allOn'))
    cd.button(l='All Off', bgc=(0.6, 0.6, 0.6), c=partial(ops_operations.componentHideShow, 'allOff'))
    cd.setParent(mainColumn)
    cd.setParent("..")


# pivotChanger method.
def lt_pivotChanger(parentIn, uiType="win"):
    buttonDict = {
        "yP": ["", "2", ""],
        "yN": ["", "0", ""],
        "centre": ["1", "1", "1"],
        "xP": ["2", "", ""],
        "xN": ["0", "", ""],
        "zP": ["", "", "2"],
        "zN": ["", "", "0"]
    }

    def setPivot(*args):
        inAxis = args[0]

        for obj in pm.ls(sl=True):

            objectPos = pm.xform(obj, q=True, t=True)

            objPiv = pm.xform(obj, q=True, rp=True, ws=True)

            objBbox = pm.xform(obj, q=True, bb=True)

            newPivotMatrix = [
                [
                    objBbox[0],
                    (objBbox[0] + objBbox[3]) / 2,
                    objBbox[3]
                ],
                [
                    objBbox[1],
                    (objBbox[1] + objBbox[4]) / 2,
                    objBbox[4]
                ],
                [
                    objBbox[2],
                    (objBbox[2] + objBbox[5]) / 2,
                    objBbox[5]
                ]
            ]
            newPivot = []
            for x in range(len(newPivotMatrix)):
                if buttonDict.get(inAxis)[x]:
                    newPivot.append(newPivotMatrix[x][int(buttonDict.get(inAxis)[x])])
                else:
                    newPivot.append(objPiv[x])

            rotatePiv = [newPivot[0] - objectPos[0], newPivot[1] - objectPos[1], newPivot[2] - objectPos[2]]
            scalePiv = [newPivot[0], newPivot[1], newPivot[2]]

            print(rotatePiv)
            print(scalePiv)

            pm.xform(obj, rp=rotatePiv)
            pm.xform(obj, sp=scalePiv)

            # print(newPivot)

    columnWidth = 70
    buttonHeight = 30

    pivotCol = pm.columnLayout(adj=True, parent=parentIn)
    pm.text(l="Pivot Changer", al="center", font="boldLabelFont")
    row = pm.rowLayout(nc=3, adj=2, parent=pivotCol, cw3=[columnWidth, columnWidth, columnWidth])
    col1 = pm.columnLayout(adj=True, parent=row)
    pm.separator(style="none", height=buttonHeight / 2)
    pm.button(l="x-", parent=col1, c=partial(setPivot, "xN"), height=buttonHeight, width=columnWidth)
    pm.button(l="z-", parent=col1, c=partial(setPivot, "zN"), height=buttonHeight, width=columnWidth)
    pm.setParent("..")  # Col1 End
    col2 = pm.columnLayout(adj=True, parent=row)
    pm.button(l="y+", parent=col2, c=partial(setPivot, "yP"), height=buttonHeight, width=columnWidth)
    pm.button(l="centre", parent=col2, c=partial(setPivot, "centre"), height=buttonHeight, width=columnWidth)
    pm.button(l="y-", parent=col2, c=partial(setPivot, "yN"), height=buttonHeight, width=columnWidth)
    pm.setParent("..")  # Col2 End
    col3 = pm.columnLayout(adj=True, parent=row)
    pm.separator(style="none", height=buttonHeight / 2)
    pm.button(l="x+", parent=col3, c=partial(setPivot, "xP"), height=buttonHeight, width=columnWidth)
    pm.button(l="z+", parent=col3, c=partial(setPivot, "zP"), height=buttonHeight, width=columnWidth)
    pm.setParent("..")  # Col3 End
    pm.setParent("..")  # Row End
    pm.setParent("..")  # PIVOT COL END


# renameLayout method.
def lt_renameLayout(parentIn, uiType="win"):
    """Function Definitions for Field Control"""

    def rnmScriptJob():

        previewtext(True)

    def renameSingle(obj, txt):
        pm.rename(obj, txt)

    def printTest(obj, txt):
        print(obj)
        print(txt)

    # Changes text of preview.
    def previewtext(v):

        names = renameFunc(False)

        if len(names.n) == 1:
            previewString = names.n[0]

        else:
            previewString = names.n[0] + ' -> ' + names.n[-1]

        if names.oN != '':
            previewString = previewString + names.oN

        pm.text('previewTextRnmWin', edit=True, l=previewString)

        if pm.frameLayout('manualFrameRnmWin', q=True, cl=True) is False:
            manualNamingFrame(True)

    # Updates frame of manual naming
    def manualNamingFrame(v):

        if pm.frameLayout('manualFrameRnmWin', q=True, cl=True) == 0:

            if pm.layout('manualFrameColumnRnmWin', q=True, ca=True):

                for field in pm.layout('manualFrameColumnRnmWin', q=True, ca=True):

                    if pm.control(field, q=True, ann=True) == 'toDelete':
                        pm.deleteUI(field)

            radioButtonValue = pm.radioButtonGrp('manualFrameRadioRnmWin', q=True, select=True)

            selection = select.sel()

            allNames = renameFunc(False)

            if radioButtonValue == 1:

                names = select.sel()

                for n in names:
                    pm.nameField(object=n, width=250, ann='toDelete', parent='manualFrameColumnRnmWin')

            elif radioButtonValue == 2:

                names = allNames.n

                if selection:

                    for x in range(len(names)):
                        manRnmTxtField = pm.textField(width=250, text=names[x], ann='toDelete',
                                                      parent='manualFrameColumnRnmWin',
                                                      cc=partial(renameSingle, selection[x]),
                                                      ec=partial(renameSingle, selection[x]))

    # Queries and changes fieldStates.
    def fieldstate(v):

        partsListCheck = pm.checkBox('partsListCheckBoxRnmWin', q=True, v=True)

        if partsListCheck == 1:
            pm.checkBox('partCheckRnmWin', e=True, v=0)

        preCheck = pm.checkBox('prefixCheckRnmWin', q=True, v=True)

        sideCheck = pm.checkBox('sideCheckRnmWin', q=True, v=True)

        partCheck = pm.checkBox('partCheckRnmWin', q=True, v=True)

        pm.textFieldGrp('prefixTxtRnmWin', edit=True, enable=preCheck)

        pm.textFieldGrp('sideTxtRnmWin', edit=True, enable=sideCheck)

        pm.textFieldGrp('partTxtRnmWin', edit=True, enable=partCheck)

        pm.textField('partsListTextFieldRnmWin', edit=True, enable=partsListCheck)

        previewtext(v)

    # Populates parts list text field on menu change
    def partslistpopulate(v):

        partsList = ''

        for n in dt_rignames.names(v):
            partsList = partsList + ', ' + n

        partsList = partsList[2:]

        pm.textField('partsListTextFieldRnmWin', edit=True, text=partsList)

        previewtext(v)

    # Rename
    def renameobjs(v):

        renameFunc(True)

    def renameFunc(bool):

        rnmArgs = {}

        if pm.checkBox('prefixCheckRnmWin', query=True, value=True) == 1:
            rnmArgs['prefix'] = pm.textFieldGrp('prefixTxtRnmWin', query=True, text=True)

        if pm.checkBox('sideCheckRnmWin', query=True, value=True) == 1:
            rnmArgs['side'] = pm.textFieldGrp('sideTxtRnmWin', query=True, text=True)

        if pm.checkBox('partCheckRnmWin', query=True, value=True) == 1:
            rnmArgs['part'] = pm.textFieldGrp('partTxtRnmWin', query=True, text=True)

        if pm.checkBox('partsListCheckBoxRnmWin', query=True, value=True) == 1:
            rnmArgs['partslist'] = pm.textField('partsListTextFieldRnmWin', query=True, text=True).split(', ')

        rnmArgs['perobject'] = pm.checkBox('perObjectCheckRnmWin', query=True, value=True)

        rnmArgs['letter'] = pm.checkBox('letterCheckRnmWin', query=True, value=True)

        rnmArgs['endchain'] = pm.checkBox('endChainCheckRnmWin', query=True, value=True)

        rnmArgs['separator'] = pm.checkBox('separatorCheckRnmWin', query=True, value=True)

        rnmArgs['withconnections'] = pm.checkBox('withConnectionsCheckRnmWin', query=True, value=True)

        rnmArgs['specialpart'] = pm.checkBox('specialNameCheckRnmWin', query=True, value=True)

        rnm = dt_string.Rename(
            rename=bool,
            **rnmArgs
        )
        return rnm

    # Gui Variables
    separatorHeight = 10

    """
    Layout Start
    """

    # Main column layout
    column = pm.columnLayout(adj=True, width=200)

    # Text to hold preview of rename
    preview = pm.text('previewTextRnmWin',
                      font='boldLabelFont',
                      height=60,
                      l='Preview',
                      parent=column)

    # Column layout for position adjustment of textFieldGrps
    textColumn = pm.columnLayout(adj=True,
                                 co=['left', -100],
                                 parent=column)
    preRow = pm.rowLayout(nc=2)
    prefix = pm.textFieldGrp('prefixTxtRnmWin',
                             label='Prefix',
                             text='bn',
                             adj=0,
                             cc=previewtext,
                             parent=preRow)

    preCheck = pm.checkBox('prefixCheckRnmWin', label='',
                           value=1,
                           cc=fieldstate,
                           parent=preRow)
    pm.setParent('..')
    sideRow = pm.rowLayout(nc=2)
    side = pm.textFieldGrp('sideTxtRnmWin',
                           label='Side',
                           text='left',
                           adj=0,
                           cc=previewtext,
                           parent=sideRow)

    sideCheck = pm.checkBox('sideCheckRnmWin',
                            label='',
                            value=1,
                            cc=fieldstate,
                            parent=sideRow)
    pm.setParent('..')
    partRow = pm.rowLayout(nc=2)
    part = pm.textFieldGrp('partTxtRnmWin',
                           label='Part',
                           text='part',
                           adj=0,
                           cc=previewtext,
                           parent=partRow)

    partCheck = pm.checkBox('partCheckRnmWin',
                            label='',
                            value=1,
                            cc=fieldstate,
                            parent=partRow)
    pm.setParent('..')
    pm.setParent('..')

    checkColumn = pm.columnLayout(co=['left', 50],
                                  parent=column)

    row = pm.rowLayout(nc=3,
                       parent=checkColumn)

    stringSeparator = pm.checkBox('separatorCheckRnmWin',
                                  l='separator',
                                  v=1,
                                  cc=previewtext,
                                  parent=row)

    letter = pm.checkBox('letterCheckRnmWin',
                         l='letter',
                         v=0,
                         cc=previewtext,
                         parent=row)

    perObject = pm.checkBox('perObjectCheckRnmWin',
                            l='perObject',
                            v=0,
                            cc=previewtext,
                            parent=row)

    endChain = pm.checkBox('endChainCheckRnmWin',
                           l='endchain?',
                           v=0,
                           cc=previewtext,
                           parent=checkColumn)

    rowCheck = pm.rowLayout(nc=2, parent=checkColumn)

    withConnections = pm.checkBox('withConnectionsCheckRnmWin',
                                  l='With Connections',
                                  v=0,
                                  cc=previewtext,
                                  parent=rowCheck)

    specialCheck = pm.checkBox('specialNameCheckRnmWin',
                               l='Special Name',
                               v=0,
                               cc=previewtext,
                               parent=rowCheck)

    pm.separator(style='none',
                 h=5,
                 parent=column)

    row2 = pm.rowLayout(nc=2,
                        # ad2=1,
                        # cat=[2, 'left', 0],
                        # bgc=[0.6, 0.42, 0.18],
                        parent=column)

    menuColumn = pm.columnLayout(adj=False,
                                 co=['left', 60],
                                 # bgc=[0.6, 0.42, 0.18],
                                 parent=row2)

    partsListCheck = pm.checkBox('partsListCheckBoxRnmWin',
                                 v=0,
                                 l='',
                                 cc=fieldstate,
                                 parent=row2)

    options = pm.optionMenu(parent=menuColumn,
                            width=100,
                            cc=partslistpopulate)

    pm.menuItem(l='arm',
                parent=options)
    pm.menuItem(l='arm2',
                parent=options)
    pm.menuItem(l='leg',
                parent=options)
    pm.menuItem(l='leg2',
                parent=options)
    pm.menuItem(l='foot',
                parent=options)
    pm.menuItem(l='foot',
                parent=options)

    partsList = pm.textField('partsListTextFieldRnmWin',
                             text='Comma Separated Parts',
                             width=100,
                             height=30,
                             enable=False,
                             # bgc=[0.7, 0.7, 0.7],
                             parent=column,
                             cc=previewtext)

    pm.button(l='rename',
              bgc=[0.1, 0.25, 0.2],
              c=renameobjs,
              parent=column)

    manualFrame = pm.frameLayout('manualFrameRnmWin', l='Manual Naming', parent=column, cll=True, cl=True,
                                 ec=partial(manualNamingFrame, True))

    manualFrameColumn = pm.columnLayout('manualFrameColumnRnmWin', adj=False, co=['left', 20])

    manualNameCheck = pm.radioButtonGrp('manualFrameRadioRnmWin', select=1, nrb=2,
                                        labelArray2=['Original', 'Generated'], cc1=previewtext,
                                        parent=manualFrameColumn)

    pm.separator(h=separatorHeight,
                 parent=column)

    pm.text(font='boldLabelFont', l='GLOBAL NAMING', parent=column)

    pm.separator(h=separatorHeight, style='none',
                 parent=column)

    pm.button(l='All Iks, Effectors and Constraints in Selection', parent=column)

    pm.button(l='All Utility Nodes in selection', parent=column)

    pm.separator(h=separatorHeight, style='none',
                 parent=column)

    pm.setParent('..')

    # Change preview text on open
    previewtext(None)
    partslistpopulate('arm')
    sJob = pm.scriptJob(e=['SelectionChanged', rnmScriptJob])

    return sJob


# renameScriptWindow method.
def lt_renameScriptWindow(parentIn, uiType="win"):
    def renameScriptJob(inLayout):

        if uiType == "dock":
            inLayout = dockCorrect(inLayout)

        if cd.layout(inLayout, q=True, ca=True):
            for nFields in cd.layout(inLayout, q=True, ca=True):
                cd.deleteUI(nFields)

        for selection in cd.ls(sl=True):
            cd.nameField(o=selection, parent=renameFrame)

    # Rename Frame Layout Start
    renameFrame = cd.frameLayout(l='Rename - Expand to Populate',
                                 parent=parentIn,
                                 cl=True,
                                 cll=True,
                                 )
    cd.setParent('..')

    outScriptJob = cd.scriptJob(e=["SelectionChanged", partial(renameScriptJob, renameFrame)])

    # Rename Frame Layout End
    return outScriptJob


# rigsinscene method.
def rigsinscene(parentIn, uiType="win"):
    def riglistrefresh(v):
        trans = pm.ls(typ="transform")
        pm.textScrollList('rigListPaneRigslist', edit=True, ra=True)
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
                    pm.textScrollList('rigListPaneRigslist', edit=True, append=listText)

    def deleteRig(v):
        trans = pm.ls(typ="transform")
        selectInList = pm.textScrollList('rigListPaneRigslist', q=True, si=True)[0].split('|')[0]
        for t in trans:
            if t == selectInList:
                pm.lockNode(t, lock=False)
                rigNodes = pm.listRelatives(t, ad=True)
                for node in rigNodes:
                    pm.lockNode(node, lock=False)
                pm.delete(rigNodes)
                pm.delete(t)
        riglistrefresh(True)

    def lock(v):

        rigName = pm.textScrollList('rigListPaneRigslist', q=True, si=True)[0].split('|')[0]
        rigContents = pm.listRelatives(rigName, ad=True, type='transform')
        pm.lockNode(rigName, lock=True)
        for r in rigContents:
            pm.lockNode(r, lock=True)
        riglistrefresh(True)

    def unlock(v):

        rigName = pm.textScrollList('rigListPaneRigslist', q=True, si=True)[0].split('|')[0]
        rigContents = pm.listRelatives(rigName, ad=True, type='transform')
        pm.lockNode(rigName, lock=False)
        for r in rigContents:
            pm.lockNode(r, lock=False)
        riglistrefresh(True)

    pm.paneLayout()

    rigList = pm.textScrollList('rigListPaneRigslist', numberOfRows=8, allowMultiSelection=True)

    pm.setParent('..')

    pm.rowLayout(nc=2)

    lockButton = pm.button(l='Lock', width=129, h=35, c=lock,
                           bgc=[0.2, 0.1, 0.3])

    unlockButton = pm.button(l='Unlock', width=129, h=35, c=unlock,
                             bgc=[0.3, 0.1, 0.2])
    pm.setParent('..')

    pm.button(l='Refresh', c=riglistrefresh, h=30, bgc=[0.2, 0.3, 0.2])

    pm.button(l='Delete Rig', c=deleteRig, bgc=[0, 0, 0])

    return


# rigCurveTypes method.
def lt_customCurveLibrary(parentIn, uiType="win"):
    curves = [
        'joint',
        'box',
        'arrow',
        'diamond',
        'tetrahedron',
        'lineCircle',
        'loccrv',
        'offArrow',
        'cardinalArrow',
        'cardinalArrow02',
        'cardinalArrow03',
        'halfCircleArrow',
        'circleArrow',
        'twoEndArrow',
        'threeDCircleArrow',
        'target',
        'oneAxisFinger',
        'droplet',
        'man',
        'house',
        'puzzle',
        'road',
        'rocket',
        'mountain',
        'tree',
    ]

    cd.frameLayout(l='Custom Curves', cll=True, cl=True, parent=parentIn)
    cd.gridLayout(nc=2, cwh=[120, 30])
    m = 'curves'
    for c in curves:
        name = "crv_%s01" % c
        cd.button(l=c, c=m + '.' + c + '(\'' + name + '\')')
    cd.setParent('..')
    cd.setParent('..')


def lt_vertexManipulation(parentIn, uiType="win"):
    # ---------------------------------- #
    #   VERT OPERATIONS FROM vctop.VRT   #
    # ---------------------------------- #
    myVrts = maths_vectors.VRT()  # Stores Verts on gui open.

    def randColour():
        return [random.uniform(0.1, 0.5), random.uniform(0.1, 0.5), random.uniform(0.1, 0.5)]

    def resetv(v):
        myVrts.reset()

    def updateVrts(v):
        return myVrts.updateVertexList()

    def moveByField(x, y, z, v):
        myVrts.move(round(x(), 2), round(y(), 2), round(z(), 2))

    # --------------- #
    #   WINDOW VARS   #
    # --------------- #
    columnWidth = 200
    colHalfW = columnWidth / 2
    colThirdW = columnWidth / 3
    bgColour = [0.1, 0.2, 0.3]

    # ---------------- #
    #   Layout START   #
    # ---------------- #
    col = pm.columnLayout(adj=True)
    statusText = pm.text(l="No Verts Yet", parent=col)
    row = pm.rowLayout(nc=3)
    xField = pm.floatField(v=0.0, width=colThirdW, parent=row)
    yField = pm.floatField(v=0.0, width=colThirdW, parent=row)
    zField = pm.floatField(v=0.0, width=colThirdW, parent=row)

    # ------------------ #
    #   Bottom Buttons   #
    # ------------------ #
    buttonRow = pm.rowLayout(nc=2, parent=col, bgc=bgColour)
    resetButton = pm.button(l="reset", c=resetv, width=colHalfW, parent=buttonRow)
    refreshVrtButton = pm.button(l="RefreshVrts", width=colHalfW, c=updateVrts, parent=buttonRow)

    # Final Set Parent
    pm.setParent(col)
    # -------------- #
    #   Layout END   #
    # -------------- #

    # ----------------------- #
    #   SETS FIELD COMMANDS   #
    # ----------------------- #
    pm.floatField(xField, edit=True, dc=partial(moveByField, xField.getValue, yField.getValue, zField.getValue))
    pm.floatField(xField, edit=True, cc=partial(moveByField, xField.getValue, yField.getValue, zField.getValue))
    pm.floatField(yField, edit=True, dc=partial(moveByField, xField.getValue, yField.getValue, zField.getValue))
    pm.floatField(yField, edit=True, cc=partial(moveByField, xField.getValue, yField.getValue, zField.getValue))
    pm.floatField(zField, edit=True, dc=partial(moveByField, xField.getValue, yField.getValue, zField.getValue))
    pm.floatField(zField, edit=True, cc=partial(moveByField, xField.getValue, yField.getValue, zField.getValue))


def lt_colourPalettes(parentIn, uiType="win"):
    def createColours(ui, v, createType="shaders"):
        paletteName = pm.columnLayout(ui, q=True, ann=True)
        for rowLs in pm.layout(ui, q=True, ca=True):
            scrollChildren = pm.layout(rowLs, q=True, ca=True)
            for rows in scrollChildren:
                for check in pm.layout(rows, q=True, ca=True):
                    if pm.checkBox(check, q=True, v=True):
                        pColour = pm.checkBox(check, q=True, bgc=True)
                        if createType == "shaders":
                            matt = "matt_pixel_%s_%s_surfaceShader01" % (
                                paletteName, dt_colour.Colour(pColour).toHex()[1:])
                            SG = "SG_pixel_%s_%s_surfaceShaderSG1" % (
                                paletteName, dt_colour.Colour(pColour).toHex()[1:])
                            if matt not in pm.ls(type="surfaceShader"):
                                shader = pm.shadingNode("surfaceShader", asShader=True,
                                                        name=matt)
                                shaderGrp = pm.sets(renderable=True, noSurfaceShader=True, empty=True,
                                                    name=SG)
                                pm.connectAttr("%s.outColor" % shader, "%s.surfaceShader" % shaderGrp, force=True)
                                pm.setAttr("%s.outColor" % shader, pColour[0], pColour[1], pColour[2])
                        elif createType == "colourUtils":
                            cUtil = "UTIL_pixel_%s_%s_colour01" % (paletteName, dt_colour.Colour(pColour).toHex()[1:])
                            if cUtil not in pm.ls(type="colorConstant"):
                                colourUtil = pm.shadingNode("colorConstant", asTexture=True, n=cUtil)
                                pm.setAttr("%s.outColor" % cUtil, pColour[0], pColour[1], pColour[2])

    def deleteColours(ui, v, createType="shaders"):
        paletteName = pm.columnLayout(ui, q=True, ann=True)
        for rowLs in pm.layout(ui, q=True, ca=True):
            scrollChildren = pm.layout(rowLs, q=True, ca=True)
            for rows in scrollChildren:
                for check in pm.layout(rows, q=True, ca=True):
                    pColour = pm.checkBox(check, q=True, bgc=True)
                    if createType == "shaders":
                        matt = "matt_pixel_%s_%s_surfaceShader01" % (
                            paletteName, dt_colour.Colour(pColour).toHex()[1:])
                        SG = "SG_pixel_%s_%s_surfaceShaderSG1" % (paletteName, dt_colour.Colour(pColour).toHex()[1:])
                        if matt in pm.ls(type="surfaceShader"):
                            pm.delete(matt)
                        if SG in pm.ls(type="shadingEngine"):
                            pm.delete(SG)
                    elif createType == "colourUtils":
                        cUtil = "UTIL_pixel_%s_%s_colour01" % (paletteName, dt_colour.Colour(pColour).toHex()[1:])
                        if cUtil in pm.ls(type="colorConstant"):
                            pm.delete(cUtil)

    # Path to palette file
    paletteFile = "R:\\12. Maya Data\\mayaUI-0.1a\\tMayaUIs_bin\\data\\palettes_LIST.csv"

    # Existence check
    if not os.path.exists(paletteFile):
        raise Exception("Cannot find pallete file.")

    # ---------------- #
    #   Layout Start   #
    # ---------------- #
    # Main column for layouts

    mainPaletteFrame = pm.frameLayout(l="Palettes", cll=True, cl=True, parent=parentIn)

    mainScroll = pm.scrollLayout(parent=mainPaletteFrame, childResizable=True, h=300)

    paletteColumnMain = pm.columnLayout(adj=True, parent=mainScroll, rs=0)

    palettes = []

    paletteFrames = []

    rowN = 0

    buttonWidth = 60

    paletteRowHeight = {}

    # Palette creation loop
    with open(paletteFile, "r") as paletteCSV:
        # CSV Reader
        readPalette = csv.reader(paletteCSV)
        # Loop for CSV rows
        for row in readPalette:
            # Header Ignore
            if rowN != 0 and row:
                # Creates Frame and Column layout if palette name
                # not seen before.
                if row[0] not in palettes:
                    palettes.append(row[0])

                    paletteRowHeight[row[0]] = 0

                    paletteFrame = pm.frameLayout(l=row[0], parent=paletteColumnMain, cll=True, cl=True)

                    paletteFrames.append(paletteFrame)

                    paletteColumn = pm.columnLayout(adj=True, parent=paletteFrame, bgc=[0.5, 0.5, 0.5], rs=0,
                                                    ann=row[0])

                    paletteScroll = pm.scrollLayout(parent=paletteColumn)

                    buttonCol = pm.columnLayout(adj=True, parent=paletteFrame, rs=0)

                    buttonRow = pm.rowLayout(nc=3, parent=buttonCol)

                    pm.text(l="Shaders: ", parent=buttonRow, width=buttonWidth)

                    pm.button(parent=buttonRow,
                              l="Create",
                              c=partial(createColours, paletteColumn, createType="shaders"), width=buttonWidth)

                    pm.button(parent=buttonRow,
                              l="Delete",
                              c=partial(deleteColours, paletteColumn, createType="shaders"), width=buttonWidth)

                    buttonRow = pm.rowLayout(nc=3, parent=buttonCol)

                    pm.text(l="Textures: ", parent=buttonRow, width=buttonWidth)

                    pm.button(parent=buttonRow,
                              l="Create",
                              c=partial(createColours, paletteColumn, createType="colourUtils"), width=buttonWidth)

                    pm.button(parent=buttonRow,
                              l="Delete",
                              c=partial(deleteColours, paletteColumn, createType="colourUtils"), width=buttonWidth)
                    pm.setParent('..')
                    pm.setParent('..')
                    pm.setParent('..')
                # Row layout to hold colours from palette row
                paletteRow = pm.rowLayout(nc=int(row[2]) + 1, parent=paletteScroll)
                paletteRowHeight[row[0]] += 1
                # Loops through colours
                for colours in row[3:]:
                    # Creates checkboxes to act as swatches
                    checkBox = pm.checkBox(l="", parent=paletteRow,
                                           bgc=dt_colour.Colour(colours).toRGB(),
                                           width=25,
                                           height=20,
                                           v=1)
                    pm.setParent('..')
                pm.scrollLayout(paletteScroll, e=True, h=paletteRowHeight.get(row[0]) * 23 + 18, width=10)
                pm.setParent('..')
            # Add rowN every loop
            rowN += 1
    pm.setParent("..")
    pm.setParent("..")
    pm.setParent("..")
    pm.setParent("..")
    pm.setParent("..")
    pm.setParent("..")


def lt_riggingTools(parentIn, uiType="win"):
    column = pm.columnLayout(adj=True)
    pm.button(l="Line-Between", c=ops_operations.line, parent=column)
    pm.button(l="Parent-Curve", c=ops_operations.parentCurve, parent=column)
    pm.button(l="Offset Grp", c=ops_operations.offsetGrp, parent=column)
    pm.setParent("..")


def lt_constraints(parentIn, uiType="win"):
    axes = ["x", "y", "z"]

    aConstraints = {
        "parent": [cd.parentConstraint, ["skipTranslate", 0, "skipRotate", 1]],
        "orient": [cd.orientConstraint, ["skip", 1]],
        "point": [cd.pointConstraint, ["skip", 0]],
        "scale": [cd.scaleConstraint, ["skip", 2]]
    }

    def createConstraint(linkType, offsetCheck, skipChecks, v):

        if uiType == "dock":
            offsetCheck = dockCorrect(offsetCheck)
            correctedSkipChecks = []
            for checks in skipChecks:
                correctedSkipChecks.append(dockCorrect(checks))
            skipChecks = correctedSkipChecks

        skipMatrix = []
        listIter = -1
        checkIter = 0
        for x in range(9):
            checkBool = cd.checkBox(skipChecks[x], q=True, v=True)
            if x % 3 == 0:
                skipMatrix.append([])
                listIter += 1
            if checkBool is not True:
                skipMatrix[listIter].append(axes[checkIter])
            checkIter += 1
            if checkIter % 3 == 0:
                checkIter = 0

        constraintArgs = {
            "name": "link_%sConstraint01" % linkType,
            "weight": 1.0,
            "maintainOffset": cd.checkBox(offsetCheck, q=True, v=True),
        }

        for x in range(0, len(aConstraints.get(linkType)[1]), 2):
            if skipMatrix[aConstraints.get(linkType)[1][x + 1]]:
                constraintArgs[aConstraints.get(linkType)[1][x]] = skipMatrix[aConstraints.get(linkType)[1][x + 1]]

        try:
            aConstraints.get(linkType)[0](**constraintArgs)

        except TypeError:

            raise TypeError("SELECT SOMETHING")

    def checksUpdate(inRow, value):

        if uiType == "dock":
            inRow = dockCorrect(inRow)

        for checks in cd.layout(inRow, q=True, ca=True)[1:]:
            cd.checkBox(checks, edit=True, value=value)

    skipChecksC = []
    pWidth = 200

    column = cd.columnLayout(adj=True, parent=parentIn, width=pWidth)

    cd.text(l="Constraint Axes", align="center", font="boldLabelFont")
    cd.separator(style="none", h=5, parent=column)

    skipTRow = cd.rowLayout(nc=5, adj=True, parent=column)
    cd.text(l="Translate")
    for axis in axes:
        skipChecksC.append(cd.checkBox(l=axis, v=1, width=pWidth / 6, parent=skipTRow))
    allCheck = cd.checkBox(l="all", v=1, width=pWidth / 6, parent=skipTRow, cc=partial(checksUpdate, skipTRow))
    cd.setParent("..")

    skipRRow = cd.rowLayout(nc=5, adj=True, parent=column)
    cd.text(l="Rotate")
    for axis in axes:
        skipChecksC.append(cd.checkBox(l=axis, v=1, width=pWidth / 6, parent=skipRRow))
    allCheck = cd.checkBox(l="all", v=1, width=pWidth / 6, parent=skipRRow, cc=partial(checksUpdate, skipRRow))
    cd.setParent("..")

    skipSRow = cd.rowLayout(nc=5, adj=True, parent=column)
    cd.text(l="Scale")
    for axis in axes:
        skipChecksC.append(cd.checkBox(l=axis, v=1, width=pWidth / 6, parent=skipSRow))
    allCheck = cd.checkBox(l="all", v=1, width=pWidth / 6, parent=skipSRow, cc=partial(checksUpdate, skipSRow))
    cd.setParent("..")

    for constraintType in ["parent", "orient", "point", "scale"]:
        for link in aConstraints:
            if link == constraintType:
                linkRow = cd.rowLayout(nc=2, adj=1, parent=column)
                linkButton = cd.button(l=link, width=pWidth / 2, height=30, parent=linkRow)
                linkOffsetCheck = cd.checkBox(l="Offset", v=0, parent=linkRow)
                cd.button(linkButton, edit=True, c=partial(createConstraint, link, linkOffsetCheck, skipChecksC))
    cd.setParent("..")
    cd.setParent("..")


def lt_fingerRenamer(parentIn, uiType="win"):
    sideD = {
        1: "_l_",
        2: "_r_",
        3: ""
    }

    def renameFingers(*args):
        finger = cd.textField(fingerField, q=True, tx=True)
        side = sideD.get(cd.radioButtonGrp(sideButtonGrp, q=True, select=True))
        cd.select(hi=True)
        s = cd.ls(sl=True, fl=True)
        d = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for x in range(0, len(s)):
            if s[x] != s[-1]:
                cd.rename(s[x], "bn" + side + finger + d[x] + "01")
            else:
                cd.rename(s[x], "be" + side + finger + d[x] + "01")

    col = cd.columnLayout(adj=True, parent=parentIn)

    fingerField = cd.textField(tx="Finger Name", parent=col)
    sideButtonGrp = cd.radioButtonGrp(nrb=3, la2=["left", "right"], l='', select=1, parent=col)
    cd.button(l='rename', parent=col, c=renameFingers)
    cd.setParent("..")
