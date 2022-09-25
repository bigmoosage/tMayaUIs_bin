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
def lt_paintingWeights(parentIn, uiType="win"):
    cd.columnLayout(parent=parentIn)
    cd.setParent('..', adj=True)
