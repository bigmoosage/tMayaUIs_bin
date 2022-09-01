"""
Wraps gui creation for plug-in initialisation
"""

import os

import maya.cmds as cd

from tMayaUIs_bin.gui import gui_Window
from tMayaUIs_bin.gui import gui_layouts
from tMayaUIs_bin.gui import gui_preferences
from tMayaUIs_bin.conf import cfg
from tMayaUIs_bin.conf import lib_layouts

modPath = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(modPath, "LICENSE"), "r") as lic:
    LICENSE = lic.read()



def onStartCreate():

    scriptJobs = []

    cfgRead = cfg.Config().cfgData

    for uis in cfgRead.sections():

        isDock = {"dock": True, "win": False}

        if cfgRead.has_option(uis, "onStart") and cfgRead.getboolean(uis, "onStart"):

            isDock = isDock.get(cfgRead.get(uis, "uiType"))

            layoutsIn = [lib_layouts.lDict.get(lFunc) for lFunc in cfgRead.get(uis, "layouts").split(",")]

            if isDock:
                dockArea = cfgRead.get(uis, "dockArea")
                onStartUI = gui_Window.Window(title=uis, layout=layoutsIn, dock=isDock, dockArea=dockArea)

            else:
                onStartUI = gui_Window.Window(title=uis, layout=layoutsIn, dock=isDock)

            if onStartUI.scriptjobs:

                scriptJobs += onStartUI.scriptjobs

    return scriptJobs


def tMayaUIs_Menu():

    if cd.menu("tMayaUIs_Menu", q=True, exists=True):
        cd.deleteUI("tMayaUIs_Menu")

    helpMenu = cd.menu("tMayaUIs_Menu", parent="MayaWindow")
    helpMenuItem1 = cd.menuItem(l="UI Creator", parent=helpMenu, c=gui_preferences.createWin)
    helpMenuItem2 = cd.menuItem(l="help", parent=helpMenu, c=helpWindow)
    helpMenuItem3 = cd.menuItem(l="LICENSE", parent=helpMenu, c=licenceWindow)

    return helpMenu


def helpWindow(*args):
    def helpGUI(parentIn, uiType="win"):
        cd.columnLayout()
        cd.setParent('..')

    gui_Window.Window(title="LICENSE", layout=[helpGUI])

def licenceWindow(*args):

    def licenseGUI(parentIn, uiType="win"):

        cd.columnLayout(parent=parentIn)
        cd.rowLayout(nc=3)
        cd.separator(width=15, style="none")
        cd.columnLayout()
        cd.separator(height=15, style="none")
        cd.text(l=LICENSE, align="left")
        cd.separator(height=15, style="none")
        cd.setParent("..")
        cd.separator(width=15, style="none")
        cd.setParent("..")
        cd.setParent("..")

    gui_Window.Window(title="LICENSE", layout=[licenseGUI])
