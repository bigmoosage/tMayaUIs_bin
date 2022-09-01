# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
lt_riggingTools Layout
"""

# IMPORTS
import pymel.core as pm
from tMayaUIs_bin.operations import ops_operations
from tMayaUIs_bin.gui.layoutOut.dockCorrect import *
from functools import partial

def lt_riggingTools(parentIn, uiType="win"):
    column = pm.columnLayout(adj=True)
    pm.button(l="Line-Between", c=ops_operations.line, parent=column)
    pm.button(l="Parent-Curve", c=ops_operations.parentCurve, parent=column)
    pm.button(l="Offset Grp", c=ops_operations.offsetGrp, parent=column)
    pm.button(l="Match Positions", c=ops_operations.matcher, parent=column)
    pm.setParent("..")

