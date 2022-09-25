# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
lt_fingerRenamer Layout
"""

# IMPORTS
import maya.cmds as cd
from tMayaUIs_bin.gui.layoutOut.dockCorrect import *
from functools import partial

def lt_fingerRenamer(parentIn, uiType="win"):
    sideD = {
        1: "_l_",
        2: "_r_",
        3: "_c_"
    }

    def renameFingers(*args):
        finger = cd.textField(fingerField, q=True, tx=True)
        side = sideD.get(cd.radioButtonGrp(sideButtonGrp, q=True, select=True))
        cd.select(hi=True)
        s = cd.ls(sl=True, fl=True)
        d = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for x in range(len(s)):
            if s[x] != s[-1]:
                cd.rename(s[x], "bn" + side + finger + d[x] + "01")
            else:
                cd.rename(s[x], "be" + side + finger + d[x] + "01")

    col = cd.columnLayout(adj=True, parent=parentIn)

    fingerField = cd.textField(tx="Finger Name", parent=col)
    sideButtonGrp = cd.radioButtonGrp(nrb=3, la3=["left", "right", "mid"], l='', select=1, parent=col)
    cd.button(l='rename', parent=col, c=renameFingers)
    cd.setParent("..")
