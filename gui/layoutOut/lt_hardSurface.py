# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
lt_basicButtons Layout
"""

# IMPORTS
import maya.cmds as cd
from tMayaUIs_bin.gui import gui_styles as qts
from tMayaUIs_bin.gui.layoutOut.dockCorrect import *
from functools import partial
from tMayaUIs_bin.operations import ops_vertex


def lt_hardSurface(parentIn, uiType="win"):
    buttonWidth = 300
    buttonCol = cd.columnLayout(adj=True, parent=parentIn)
    cd.button(label="Circularise (rel)", c=partial(ops_vertex.VCT.circularise, "rel"), w=buttonWidth, parent=buttonCol)
    cd.button(label="Circularise (abs)", c=partial(ops_vertex.VCT.circularise, "abs"), w=buttonWidth, parent=buttonCol)
    cd.button(label="Spherise", c=ops_vertex.VCT.spherise, w=buttonWidth, parent=buttonCol)
    cd.button(label="Spherise around Loc", c=ops_vertex.VCT.spheriseAroundPoint, w=buttonWidth, parent=buttonCol)
    cd.button(label="Planarise", c=ops_vertex.VCT.planarise, w=buttonWidth, parent=buttonCol)
    cd.button(label="Linearise (Equal)", c=partial(ops_vertex.VCT.linearise, True), w=buttonWidth, parent=buttonCol)
    cd.button(label="Linearise (Maintain)", c=partial(ops_vertex.VCT.linearise, False), w=buttonWidth, parent=buttonCol)
    butRow = cd.rowLayout(nc=3, w=buttonWidth, parent=buttonCol)
    cd.button(label="Linearise (X)", c=partial(ops_vertex.VCT.equal, 0), w=buttonWidth/3, parent=butRow)
    cd.button(label="Linearise (Y)", c=partial(ops_vertex.VCT.equal, 1), w=buttonWidth/3, parent=butRow)
    cd.button(label="Linearise (Z)", c=partial(ops_vertex.VCT.equal, 2), w=buttonWidth/3, parent=butRow)
    cd.setParent(buttonCol)