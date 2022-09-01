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

