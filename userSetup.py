import sys


from maya.utils import executeDeferred

import pymel.core as pm
import maya.cmds as cd
import maya.mel as melE

from tMayaUIs_bin import gui
from tMayaUIs_bin.gui import gui_Window
from tMayaUIs_bin.operations import ops_joints as oj