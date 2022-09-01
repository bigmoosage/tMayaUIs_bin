# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
dockCorrect Layout
"""

# IMPORTS
from tMayaUIs_bin.gui.layoutOut.dockCorrect import *
from functools import partial

#   GLOBAL METHODS   #
# ------------------ #
def dockCorrect(inName):
    corrected = inName.split("|")
    corrected[0] = "MayaWindow"
    return "|".join(corrected)

