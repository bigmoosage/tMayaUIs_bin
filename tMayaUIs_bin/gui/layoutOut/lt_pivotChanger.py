# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
lt_pivotChanger Layout
"""

# IMPORTS
import pymel.core as pm
import maya.cmds as cd
from tMayaUIs_bin.gui.layoutOut.dockCorrect import *
from functools import partial

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

        for obj in cd.ls(sl=True):

            objectPos = cd.xform(obj, q=True, t=True)

            objPiv = cd.xform(obj, q=True, rp=True, ws=True)

            objBbox = cd.xform(obj, q=True, bb=True)

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
            #cd.xform(obj, piv=finalPiv)
            #print(rotatePiv)
            #print(scalePiv)
            cd.xform(obj, rp=rotatePiv)
            cd.xform(obj, sp=rotatePiv)


            # print(newPivot)

    columnWidth = 70
    buttonHeight = 30

    pivotCol = cd.columnLayout(adj=True, parent=parentIn)
    cd.text(l="Pivot Changer", al="center", font="boldLabelFont")
    row = cd.rowLayout(nc=3, adj=2, parent=pivotCol, cw3=[columnWidth, columnWidth, columnWidth])
    col1 = cd.columnLayout(adj=True, parent=row)
    cd.separator(style="none", height=buttonHeight / 2)
    cd.button(l="x-", parent=col1, c=partial(setPivot, "xN"), height=buttonHeight, width=columnWidth)
    cd.button(l="z-", parent=col1, c=partial(setPivot, "zN"), height=buttonHeight, width=columnWidth)
    cd.setParent("..")  # Col1 End
    col2 = cd.columnLayout(adj=True, parent=row)
    cd.button(l="y+", parent=col2, c=partial(setPivot, "yP"), height=buttonHeight, width=columnWidth)
    cd.button(l="centre", parent=col2, c=partial(setPivot, "centre"), height=buttonHeight, width=columnWidth)
    cd.button(l="y-", parent=col2, c=partial(setPivot, "yN"), height=buttonHeight, width=columnWidth)
    cd.setParent("..")  # Col2 End
    col3 = cd.columnLayout(adj=True, parent=row)
    cd.separator(style="none", height=buttonHeight / 2)
    cd.button(l="x+", parent=col3, c=partial(setPivot, "xP"), height=buttonHeight, width=columnWidth)
    cd.button(l="z+", parent=col3, c=partial(setPivot, "zP"), height=buttonHeight, width=columnWidth)
    cd.setParent("..")  # Col3 End
    cd.setParent("..")  # Row End
    cd.setParent("..")  # PIVOT COL END

