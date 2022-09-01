# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
lt_colourPalettes Layout
"""

# IMPORTS
import csv
import os
import pymel.core as pm
from tMayaUIs_bin.manip import dt_colour
from tMayaUIs_bin.gui.layoutOut.dockCorrect import *
from functools import partial

def lt_colourPalettes(parentIn, uiType="win"):
    def createColours(ui, v, createType="shaders"):
        paletteName = pm.columnLayout(ui, q=True, ann=True)
        for rowLs in pm.layout(ui, q=True, ca=True):
            scrollChildren = pm.layout(rowLs, q=True, ca=True)
            for rows in scrollChildren:
                for check in pm.layout(rows, q=True, ca=True):
                    if pm.checkBox(check, q=True, v=True):
                        pColour = pm.checkBox(check, q=True, bgc=True)
                        if createType == "shaders":
                            matt = "matt_pixel_%s_%s_surfaceShader01" % (
                                paletteName, dt_colour.Colour(pColour).toHex()[1:])
                            SG = "SG_pixel_%s_%s_surfaceShaderSG1" % (
                                paletteName, dt_colour.Colour(pColour).toHex()[1:])
                            if matt not in pm.ls(type="surfaceShader"):
                                shader = pm.shadingNode("surfaceShader", asShader=True,
                                                        name=matt)
                                shaderGrp = pm.sets(renderable=True, noSurfaceShader=True, empty=True,
                                                    name=SG)
                                pm.connectAttr("%s.outColor" % shader, "%s.surfaceShader" % shaderGrp, force=True)
                                pm.setAttr("%s.outColor" % shader, pColour[0], pColour[1], pColour[2])
                        elif createType == "colourUtils":
                            cUtil = "UTIL_pixel_%s_%s_colour01" % (paletteName, dt_colour.Colour(pColour).toHex()[1:])
                            if cUtil not in pm.ls(type="colorConstant"):
                                colourUtil = pm.shadingNode("colorConstant", asTexture=True, n=cUtil)
                                pm.setAttr("%s.outColor" % cUtil, pColour[0], pColour[1], pColour[2])

    def deleteColours(ui, v, createType="shaders"):
        paletteName = pm.columnLayout(ui, q=True, ann=True)
        for rowLs in pm.layout(ui, q=True, ca=True):
            scrollChildren = pm.layout(rowLs, q=True, ca=True)
            for rows in scrollChildren:
                for check in pm.layout(rows, q=True, ca=True):
                    pColour = pm.checkBox(check, q=True, bgc=True)
                    if createType == "shaders":
                        matt = "matt_pixel_%s_%s_surfaceShader01" % (
                            paletteName, dt_colour.Colour(pColour).toHex()[1:])
                        SG = "SG_pixel_%s_%s_surfaceShaderSG1" % (paletteName, dt_colour.Colour(pColour).toHex()[1:])
                        if matt in pm.ls(type="surfaceShader"):
                            pm.delete(matt)
                        if SG in pm.ls(type="shadingEngine"):
                            pm.delete(SG)
                    elif createType == "colourUtils":
                        cUtil = "UTIL_pixel_%s_%s_colour01" % (paletteName, dt_colour.Colour(pColour).toHex()[1:])
                        if cUtil in pm.ls(type="colorConstant"):
                            pm.delete(cUtil)

    # Path to palette file
    paletteFile = "R:\\12. Maya Data\\mayaUI-0.1a\\tMayaUIs_bin\\data\\palettes_LIST.csv"

    # Existence check
    if not os.path.exists(paletteFile):
        raise Exception("Cannot find pallete file.")

    # ---------------- #
    #   Layout Start   #
    # ---------------- #
    # Main column for layouts

    mainPaletteFrame = pm.frameLayout(l="Palettes", cll=True, cl=True, parent=parentIn)

    mainScroll = pm.scrollLayout(parent=mainPaletteFrame, childResizable=True, h=300)

    paletteColumnMain = pm.columnLayout(adj=True, parent=mainScroll, rs=0)

    palettes = []

    paletteFrames = []

    rowN = 0

    buttonWidth = 60

    paletteRowHeight = {}

    # Palette creation loop
    with open(paletteFile, "r") as paletteCSV:
        # CSV Reader
        readPalette = csv.reader(paletteCSV)
        # Loop for CSV rows
        for row in readPalette:
            # Header Ignore
            if rowN != 0 and row:
                # Creates Frame and Column layout if palette name
                # not seen before.
                if row[0] not in palettes:
                    palettes.append(row[0])

                    paletteRowHeight[row[0]] = 0

                    paletteFrame = pm.frameLayout(l=row[0], parent=paletteColumnMain, cll=True, cl=True)

                    paletteFrames.append(paletteFrame)

                    paletteColumn = pm.columnLayout(adj=True, parent=paletteFrame, bgc=[0.5, 0.5, 0.5], rs=0,
                                                    ann=row[0])

                    paletteScroll = pm.scrollLayout(parent=paletteColumn)

                    buttonCol = pm.columnLayout(adj=True, parent=paletteFrame, rs=0)

                    buttonRow = pm.rowLayout(nc=3, parent=buttonCol)

                    pm.text(l="Shaders: ", parent=buttonRow, width=buttonWidth)

                    pm.button(parent=buttonRow,
                              l="Create",
                              c=partial(createColours, paletteColumn, createType="shaders"), width=buttonWidth)

                    pm.button(parent=buttonRow,
                              l="Delete",
                              c=partial(deleteColours, paletteColumn, createType="shaders"), width=buttonWidth)

                    buttonRow = pm.rowLayout(nc=3, parent=buttonCol)

                    pm.text(l="Textures: ", parent=buttonRow, width=buttonWidth)

                    pm.button(parent=buttonRow,
                              l="Create",
                              c=partial(createColours, paletteColumn, createType="colourUtils"), width=buttonWidth)

                    pm.button(parent=buttonRow,
                              l="Delete",
                              c=partial(deleteColours, paletteColumn, createType="colourUtils"), width=buttonWidth)
                    pm.setParent('..')
                    pm.setParent('..')
                    pm.setParent('..')
                # Row layout to hold colours from palette row
                paletteRow = pm.rowLayout(nc=int(row[2]) + 1, parent=paletteScroll)
                paletteRowHeight[row[0]] += 1
                # Loops through colours
                for colours in row[3:]:
                    # Creates checkboxes to act as swatches
                    checkBox = pm.checkBox(l="", parent=paletteRow,
                                           bgc=dt_colour.Colour(colours).toRGB(),
                                           width=25,
                                           height=20,
                                           v=1)
                    pm.setParent('..')
                pm.scrollLayout(paletteScroll, e=True, h=paletteRowHeight.get(row[0]) * 23 + 18, width=10)
                pm.setParent('..')
            # Add rowN every loop
            rowN += 1
    pm.setParent("..")
    pm.setParent("..")
    pm.setParent("..")
    pm.setParent("..")
    pm.setParent("..")
    pm.setParent("..")

