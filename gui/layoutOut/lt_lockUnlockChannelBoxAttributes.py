# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
lt_lockUnlockChannelBoxAttributes Layout
"""

# IMPORTS
import maya.cmds as cd
import pymel.core as pm
from tMayaUIs_bin.operations import ops_select as select
from tMayaUIs_bin.gui.layoutOut.dockCorrect import *
from functools import partial

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

