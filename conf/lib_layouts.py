# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
Layout Library for tMayaUIs Plug-in
"""

from tMayaUIs_bin.gui.layoutOut import lt_basicButtons
from tMayaUIs_bin.gui.layoutOut import lt_colourPalettes
from tMayaUIs_bin.gui.layoutOut import lt_connectAttributes
from tMayaUIs_bin.gui.layoutOut import lt_constraints
from tMayaUIs_bin.gui.layoutOut import lt_customCurveLibrary
from tMayaUIs_bin.gui.layoutOut import lt_fingerRenamer
from tMayaUIs_bin.gui.layoutOut import lt_hardSurface
from tMayaUIs_bin.gui.layoutOut import lt_lockUnlockChannelBoxAttributes
from tMayaUIs_bin.gui.layoutOut import lt_paintingWeights
from tMayaUIs_bin.gui.layoutOut import lt_pivotChanger
from tMayaUIs_bin.gui.layoutOut import lt_renameLayout
from tMayaUIs_bin.gui.layoutOut import lt_renameScriptWindow
from tMayaUIs_bin.gui.layoutOut import lt_riggingTools
from tMayaUIs_bin.gui.layoutOut import lt_showHideViewportElements
from tMayaUIs_bin.gui.layoutOut import lt_vertexManipulation
from tMayaUIs_bin.gui.layoutOut import lt_wireframeColourChanger

# Defines list of available layouts.
lDict = {
	"lt_basicButtons": lt_basicButtons.lt_basicButtons,
	"lt_colourPalettes": lt_colourPalettes.lt_colourPalettes,
	"lt_connectAttributes": lt_connectAttributes.lt_connectAttributes,
	"lt_constraints": lt_constraints.lt_constraints,
	"lt_customCurveLibrary": lt_customCurveLibrary.lt_customCurveLibrary,
	"lt_fingerRenamer": lt_fingerRenamer.lt_fingerRenamer,
	"lt_hardSurface": lt_hardSurface.lt_hardSurface,
	"lt_lockUnlockChannelBoxAttributes": lt_lockUnlockChannelBoxAttributes.lt_lockUnlockChannelBoxAttributes,
	"lt_paintingWeights": lt_paintingWeights.lt_paintingWeights,
	"lt_pivotChanger": lt_pivotChanger.lt_pivotChanger,
	"lt_renameLayout": lt_renameLayout.lt_renameLayout,
	"lt_renameScriptWindow": lt_renameScriptWindow.lt_renameScriptWindow,
	"lt_riggingTools": lt_riggingTools.lt_riggingTools,
	"lt_showHideViewportElements": lt_showHideViewportElements.lt_showHideViewportElements,
	"lt_vertexManipulation": lt_vertexManipulation.lt_vertexManipulation,
	"lt_wireframeColourChanger": lt_wireframeColourChanger.lt_wireframeColourChanger
}
