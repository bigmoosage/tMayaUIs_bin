# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
lt_constraints Layout
"""

# IMPORTS
import maya.cmds as cd
from tMayaUIs_bin.gui.layoutOut.dockCorrect import *
from functools import partial

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
    cd.setParent("..")
    cd.setParent("..")
    cd.setParent("..")
    cd.setParent("..")
    cd.setParent("..")

