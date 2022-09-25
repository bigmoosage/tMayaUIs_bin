# tMayaUIs_PLUG.py

#################################################################################################
# _______  _     _    __   __  _______  __   __  _______    _______  ___      __   __  _______  #
#|       || | _ | |  |  |_|  ||   _   ||  | |  ||   _   |  |       ||   |    |  | |  ||       | #
#|_     _|| || || |  |       ||  |_|  ||  |_|  ||  |_|  |  |    _  ||   |    |  | |  ||    ___| #
#  |   |  |       |  |       ||       ||       ||       |  |   |_| ||   |    |  |_|  ||   | __  #
#  |   |  |       |  |       ||       ||_     _||       |  |    ___||   |___ |       ||   ||  | #
#  |   |  |   _   |  | ||_|| ||   _   |  |   |  |   _   |  |   |    |       ||       ||   |_| | #
#  |___|  |__| |__|  |_|   |_||__| |__|  |___|  |__| |__|  |___|    |_______||_______||_______| #
#################################################################################################

# Mostly based on example from Api Reference

# ==============================================
# Imports
# ==============================================
# Built-ins
import sys
import os

# import os
# sys.path.append("R:\\12. Maya Data\\mayaUI-0.1a")

# API
# import maya.OpenMaya as om
import maya.OpenMayaMPx as ommpx
# from maya import mel
import warnings

# CMDS
import maya.cmds as cd
# GUI IMPORTS
# import tMayaUIs_bin
from tMayaUIs_bin.gui import gui_Window
from tMayaUIs_bin.gui import gui_layouts
from tMayaUIs_bin.gui import gui_wrap
from tMayaUIs_bin.gui import gui_preferences

exec("from tMayaUIs_bin import gui")
exec("from tMayaUIs_bin.gui import gui_Window")

# ==============================================
# Author Info
# ==============================================
kAuthorName = 'Tom Wood'
kPluginVersion = '0.1a'
kRequiredApiVersion = 'Any'
kLICENSE = '''Copyright (c) 2020 Tom Wood

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''


# ===================================
# Plug-in Definition
# ===================================
# Class that initializes command.
class C_tMayaUIs_bin_CMD(ommpx.MPxCommand):
    kPluginCmdName = "tMayaUIs"

    # Initial method, initializes command structure
    def __init__(self):
        ommpx.MPxCommand.__init__(self)

    # Doit method is called once during command.
    def doIt(self, args):
        gui_preferences.createWin()

        # print("Window should have come up.")
        self.redoIt()

    # Redoit method is called multiple times, where it actually does the important stuff
    # in the command.
    def redoIt(self):
        pass

    # Called if command is undone.
    def undoIt(self):
        pass

    # If undoable returns True, each instance of the command is added to the undo Queue.
    def isUndoable(self):
        return True

    # Command creator Method
    @classmethod
    def cmdCreator(cls):
        return ommpx.asMPxPtr(cls())


# ===================================
#   ON START UI
# ===================================
class ToolShelf:

    def __init__(self):

        self.uiMenu = None

        self.onStartWins = None

        self.scriptjobs = None

    def create(self):

        self.uiMenu = gui_wrap.tMayaUIs_Menu()

        self.onStartWins = gui_wrap.onStartCreate()

        return self.onStartWins

    def delete(self):

        for scriptjob in self.onStartWins:
            try:
                cd.scriptJob(kill=scriptjob)
            except:
                pass

        if cd.menu("tMayaUIs_Menu", q=True, exists=True):
            cd.deleteUI("tMayaUIs_Menu")


# ===================================
# PLUGIN
# ===================================

shelfVar = ToolShelf()  # Initialises Start UI Class


# Initialize Plugin
def initializePlugin(mobject):
    mplugin = ommpx.MFnPlugin(mobject,
                              kAuthorName,
                              kPluginVersion,
                              kRequiredApiVersion)
    try:
        mplugin.registerCommand(C_tMayaUIs_bin_CMD.kPluginCmdName, C_tMayaUIs_bin_CMD.cmdCreator)

        global shelfVar

        shelfVar.create()

    except:

        raise Exception('Failed to register: %s' % C_tMayaUIs_bin_CMD.kPluginCmdName)


# DeInitialize Plugin
def uninitializePlugin(mobject):
    mplugin = ommpx.MFnPlugin(mobject)

    try:
        mplugin.deregisterCommand(C_tMayaUIs_bin_CMD.kPluginCmdName)

        global shelfVar

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            shelfVar.delete()

        for win in cd.lsUI(type="window"):
            try:
                if cd.window(win, q=True, docTag=True) == "tMayaUI":
                    cd.deleteUI(win)
            except RuntimeError:
                pass

        for dock in cd.lsUI(type="dockControl"):
            try:
                if cd.dockControl(dock, q=True, docTag=True) == "tMayaUI":
                    cd.deleteUI(dock)
            except RuntimeError:
                pass





    except:

        raise Exception('Failed to register: %s' % C_tMayaUIs_bin_CMD.kPluginCmdName)
