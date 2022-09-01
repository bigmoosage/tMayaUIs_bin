# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
lt_connectAttributes Layout
"""

# IMPORTS
import maya.cmds as cd
import maya.mel as melE
import pymel.core as pm
from tMayaUIs_bin.operations import ops_select as select
from tMayaUIs_bin.gui.layoutOut.dockCorrect import *
from functools import partial

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
        for selected in cd.ls(sl=True):
            for attr in attrlist:
                qAttr = "%s%s" % (selected, attr)
                if cd.connectionInfo(qAttr, isDestination=True):
                    cd.disconnectAttr(cd.connectionInfo(qAttr, sourceFromDestination=True), qAttr)

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

