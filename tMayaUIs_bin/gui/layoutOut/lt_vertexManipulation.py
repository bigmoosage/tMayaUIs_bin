# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
lt_vertexManipulation Layout
"""

# IMPORTS
import random
import pymel.core as pm
from pymel.core import nodetypes as nt
from pymel.core import uitypes as ut
from tMayaUIs_bin.maths import maths_vectors
from tMayaUIs_bin.gui.layoutOut.dockCorrect import *
from functools import partial
from tMayaUIs_bin.operations import ops_vertex


def lt_vertexManipulation(parentIn, uiType="win"):
    # ---------------------------------- #
    #   VERT OPERATIONS FROM vctop.VRT   #
    # ---------------------------------- #
    def updateVertList(*args):
        pass

    def updateText(*args):
        ut.Text("vertStatusText").setLabel("OK")

    def randColour():
        return [random.uniform(0.1, 0.5), random.uniform(0.1, 0.5), random.uniform(0.1, 0.5)]

    def resetv(v):
        ops_vertex.reset()

    def updateVrts(v):
        ut.Text("vertStatusText").setLabel("OK")
        return ops_vertex.updateVertexList()

    def moveByField(x, y, z, *args):
        ops_vertex.move(round(x(), 2), round(y(), 2), round(z(), 2))

    # --------------- #
    #   WINDOW VARS   #
    # --------------- #
    columnWidth = 200
    colHalfW = columnWidth / 2
    colThirdW = columnWidth / 3
    bgColour = [0.1, 0.2, 0.3]

    # ---------------- #
    #   Layout START   #
    # ---------------- #
    col = pm.columnLayout(adj=True)
    statusText = pm.text("vertStatusText", l="No Verts Yet", parent=col)
    row = pm.rowLayout(nc=3)
    xField = pm.floatField(v=0.0, width=colThirdW, parent=row)
    yField = pm.floatField(v=0.0, width=colThirdW, parent=row)
    zField = pm.floatField(v=0.0, width=colThirdW, parent=row)

    # ------------------ #
    #   Bottom Buttons   #
    # ------------------ #
    circleButtonRow = pm.rowLayout(nc=2, parent=col, bgc=bgColour)
    circulariseButton = pm.button(l="Circularise", c=ops_vertex.VCT().circularise)
    spheriseButton = pm.button(l="Spherise", c=ops_vertex.VCT().spherise)
    buttonRow = pm.rowLayout(nc=2, parent=col, bgc=bgColour)
    resetButton = pm.button(l="reset", c=resetv, width=colHalfW, parent=buttonRow)
    refreshVrtButton = pm.button(l="RefreshVrts", width=colHalfW, c=updateVrts, parent=buttonRow)

    # Final Set Parent
    pm.setParent(col)
    # -------------- #
    #   Layout END   #
    # -------------- #

    # ----------------------- #
    #   SETS FIELD COMMANDS   #
    # ----------------------- #
    pm.floatField(xField, edit=True, dc=partial(moveByField, xField.getValue, yField.getValue, zField.getValue))
    pm.floatField(xField, edit=True, cc=partial(moveByField, xField.getValue, yField.getValue, zField.getValue))
    pm.floatField(yField, edit=True, dc=partial(moveByField, xField.getValue, yField.getValue, zField.getValue))
    pm.floatField(yField, edit=True, cc=partial(moveByField, xField.getValue, yField.getValue, zField.getValue))
    pm.floatField(zField, edit=True, dc=partial(moveByField, xField.getValue, yField.getValue, zField.getValue))
    pm.floatField(zField, edit=True, cc=partial(moveByField, xField.getValue, yField.getValue, zField.getValue))

