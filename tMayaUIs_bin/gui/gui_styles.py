from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui
import pymel.core as pm
from tMayaUIs_bin.manip import dt_colour as mc

# ----------------------------------- #
#   Specific Maya QT Pyside Imports   #
# ----------------------------------- #
# noinspection PyUnresolvedReferences
from PySide2.QtCore import *
# noinspection PyUnresolvedReferences
from PySide2.QtGui import *
# noinspection PyUnresolvedReferences
from PySide2.QtWidgets import *
# noinspection PyUnresolvedReferences
from shiboken2 import wrapInstance


class Style:

    def __init__(self, widget=None, bgColour=None, tColour=None, tStyle=None, tWeight=None):
        """
        :param widget:
        :param bgColour:
        :param tColour:
        :param tStyle:
        :param tWeight:
        """
        if widget is not None:

            ptr = omui.MQtUtil.findControl(widget)

            self.widget = wrapInstance(int(ptr), QWidget)

        self.styleKwargs = {}

        self.styleSheet = ""

        if bgColour is not None:
            self.styleKwargs["background-color"] = bgColour

        if tColour is not None:
            self.styleKwargs["color"] = tColour

        if tStyle is not None:
            self.styleKwargs["font-style"] = tStyle

        if tWeight is not None:
            self.styleKwargs["font-weight"] = tWeight

    @classmethod
    def SetStyle(cls, widget, bgColour=None, tColour=None, tStyle=None, tWeight=None):

        style = cls(widget=widget, bgColour=bgColour, tColour=tColour, tStyle=tStyle, tWeight=tWeight)

        for attr, value in style.styleKwargs.items():

            style.styleSheet += "%s:%s;" % (attr, value)

        style.widget.setStyleSheet(style.styleSheet)
