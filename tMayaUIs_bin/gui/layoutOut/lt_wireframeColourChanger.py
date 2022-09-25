# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
lt_wireframeColourChanger Layout
"""

# IMPORTS
import maya.cmds as cd
from tMayaUIs_bin.operations import ops_operations
from tMayaUIs_bin.gui.layoutOut.dockCorrect import *
from functools import partial

# Assign variable named frameColour to function in Maya:
def lt_wireframeColourChanger(parentIn, uiType="win"):

    def wireframeChange(rgbSlider, *args):

        if uiType == "dock":

            rgbSlider = dockCorrect(rgbSlider)

        ops_operations.curveColourChanger(rgbSlider)

    frameColourCol = cd.columnLayout(adj=True, parent=parentIn, width=50)
    cd.text(l='Set wireFrame colour', parent=frameColourCol, font="boldLabelFont")
    cd.separator(style="none", h=5, parent=frameColourCol)
    curveColourRGB = cd.colorSliderGrp(l='RGB', rgb=(0, 0, 0), adj=1, columnAlign=(1, 'left'),
                                       parent=frameColourCol,
                                       ann='fcs')
    cd.button(l='Set Colour', c=partial(wireframeChange, curveColourRGB), parent=frameColourCol)
    cd.setParent('..')

