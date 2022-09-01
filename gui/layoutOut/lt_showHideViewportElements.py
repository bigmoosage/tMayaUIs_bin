# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
lt_showHideViewportElements Layout
"""

# IMPORTS
import maya.cmds as cd
import pymel.core as pm
from tMayaUIs_bin.operations import ops_operations
from tMayaUIs_bin.gui.layoutOut.dockCorrect import *
from functools import partial

# hideViewPortLayout method.
def lt_showHideViewportElements(parentIn, uiType="win"):
    buttonDict = {'Joints': ['joints', (0.237, 0.028, 0.068)],
                  'Curves': ['nurbsCurves', (0.4, 0.237, 0.068)],
                  'Polys': ['polymeshes', (0.068, 0.028, 0.237)],
                  'Cameras': ['cameras', (0.237, 0.237, 0.068)],
                  'ImgPlanes': ['imagePlane', (0.068, 0.237, 0.237)],
                  'Deformers': ['deformers', (0.237, 0.028, 0.237)],
                  'Locators': ['locators', (0.6, 0.4, 0.1)],
                  'IKs': ['ikHandles', (0.6, 0.1, 0.2)],
                  'nCloth': ['nCloths', (0.3, 0.2, 0.2)],
                  'NurbsSurf': ['nurbsSurfaces', (0.3, 0.2, 0.4)],
                  'Lights': ['lights', (0.4, 0.237, 0.2)]
                  }
    primaryButtons = ['Polys', 'Joints', 'Curves', 'Locators', 'Lights']
    secondaryButtons = ['Cameras', 'ImgPlanes', 'Deformers', 'IKs', 'nCloth', 'NurbsSurf']

    mainColumn = pm.columnLayout(adj=True, parent=parentIn)

    bigButtonGrid = cd.columnLayout(parent=mainColumn, adj=True)
    smallButtonGrid = cd.gridLayout(nc=3, cwh=(80, 30), parent=mainColumn)
    for pb in primaryButtons:
        for x, y in buttonDict.items():
            if x == pb:
                cd.button(l=x, bgc=y[1], height=30, c=partial(ops_operations.componentHideShow, y[0]),
                          parent=bigButtonGrid)
    for sb in secondaryButtons:
        for x, y in buttonDict.items():
            if x == sb:
                cd.button(l=x, bgc=y[1], c=partial(ops_operations.componentHideShow, y[0]), parent=smallButtonGrid)
    cd.gridLayout(nc=2, cwh=(120, 30), parent=mainColumn)
    cd.button(l='Polys Alone', bgc=(0, 0.2, 0.3), c=partial(ops_operations.componentHideShow, 'polysOnly'))
    cd.button(l='Curves Alone', bgc=(0, 0.1, 0.4), c=partial(ops_operations.componentHideShow, 'curvesOnly'))
    cd.button(l='All On', bgc=(0.8, 0.8, 0.8), c=partial(ops_operations.componentHideShow, 'allOn'))
    cd.button(l='All Off', bgc=(0.6, 0.6, 0.6), c=partial(ops_operations.componentHideShow, 'allOff'))
    cd.setParent(mainColumn)
    cd.setParent("..")

