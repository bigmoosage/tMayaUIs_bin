# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
renameScriptWindow Layout
"""

# IMPORTS
import maya.cmds as cd
from tMayaUIs_bin.gui.layoutOut.dockCorrect import *
from functools import partial

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

