# BUILT-INS IMPORT
import os
from ConfigParser import ConfigParser

from tMayaUIs_bin.conf import lib_layouts
from tMayaUIs_bin.manip import dt_colour

availableLayouts = []
for func in lib_layouts.lDict:
    availableLayouts.append(str(func))

defaultCFG = {
    "info": [["Author", "Tom Wood 2020"], ["version", "0.1a"], ["license", "MIT License 2020"]],
    "colours":[[],[]],
    "ui_exampleWin": [["layouts", "lt_basicButtons", "lt_pivotChanger"],
                      ["onStart", str(0)],
                      ["uiType", "win"],
                      ["colour", dt_colour.Colour(1.0).toHex(), dt_colour.Colour(0.0).toHex(),
                       dt_colour.Colour(0.5).toHex()]],
    "ui_exampleDock": [["layouts", "lt_basicButtons", "lt_pivotChanger"],
                       ["onStart", str(0)],
                       ["uiType", "dock"],
                       ["dockArea", "right"],
                       ["colour", dt_colour.Colour(1.0).toHex(), dt_colour.Colour(0.0).toHex(),
                        dt_colour.Colour(0.5).toHex()]]
}

modPath = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(modPath, "LICENSE"), "r") as lic:
    LICENSE = lic.read()


class Config:

    def __init__(self, *args):

        self.cfg_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")

        if os.path.isfile(self.cfg_file):

            cfgParse = ConfigParser()

            self.cfgData = cfgParse
            self.cfgData.read(self.cfg_file)

        else:

            self.resetPrefs()

        self.sections = []

        self.options = []

        for section in self.cfgData.sections():
            self.sections.append(section)
            for option, value in self.cfgData.items(section):
                self.options.append([section, option, value])

        self.startupUIs = []

    def resetPrefs(self, *args):

        cfgParse = ConfigParser()

        for section in defaultCFG.keys():

            for values in defaultCFG.get(section):

                try:
                    cfgParse.add_section(section)
                except:
                    pass

                cfgParse.set(section, values[0], ",".join(values[1:]))

                with open(self.cfg_file, "w") as cfg_write:
                    cfgParse.write(cfg_write)

                self.cfgData = cfgParse
                self.cfgData.read(self.cfg_file)

                self.updateVars()

    def savePrefs(self, *args):

        with open(self.cfg_file, "w") as cfg_write:
            self.cfgData.write(cfg_write)

        self.refresh()

    def refresh(self):
        cfgParse = ConfigParser()
        self.cfgData = cfgParse
        self.cfgData.read(self.cfg_file)
        self.updateVars()

    def readPref(self, element, value, *args):

        self.cfgData.get(element, value)

    def writePref(self, section, attr, value, *args):

        self.cfgData.set(section, attr, value)

    def newWin(self, winName, layouts, onStart, uiType, dockArea):

        try:
            self.cfgData.add_section(winName)
        except:
            pass

        self.cfgData.set(winName, "layouts", layouts)
        self.cfgData.set(winName, "onStart", str(onStart))
        self.cfgData.set(winName, "uiType", uiType)
        if uiType == "dock" and dockArea:
            self.cfgData.set(winName, "dockArea", dockArea)

    def updateVars(self):
        self.sections = []
        self.options = []
        for section in self.cfgData.sections():
            self.sections.append(section)
            for option, value in self.cfgData.items(section):
                self.options.append([section, option, value])
