import os

from tMayaUIs_bin import Edit


class UpdateLayouts:

    def __init__(self):

        self.layoutFile = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gui\\gui_layouts.py")
        self.outputPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gui\\layoutOut")
        self.dictPath = os.path.join(os.path.dirname(__file__), "lib_layouts.py")
        self.analyseMethod = Edit.Editor(abspath=self.layoutFile)
        self.functionsIn = self.analyseMethod.Functions
        self.imports = self.analyseMethod.Imports
        self.layoutFiles = [lt for lt in os.listdir(self.outputPath) if lt.find("lt_") == 0 and not lt.endswith(".pyc")]

    def write_layouts(self):

        with open(self.layoutFile, "r") as readLayouts:
            lines = readLayouts.readlines()
            for funcName in self.functionsIn.keys():
                writeFile = lines[self.functionsIn.get(funcName)[0]: self.functionsIn.get(funcName)[1]]
                with open(os.path.join(self.outputPath, (funcName + ".py")), "w+") as writeOut:
                    writeOut.write("# !/usr/bin/env python\n")
                    writeOut.write("# -*-coding:utf-8-*-\n\n")
                    writeOut.write("\"\"\"\n%s Layout\n\"\"\"\n\n" % funcName)
                    writeOut.write("# IMPORTS\n")
                    for imports in self.imports.split("\n"):
                        for content in writeFile:
                            if content.find(imports.split(" ")[-1] + ".") != -1:
                                if imports not in ["\n", ""]:
                                    writeOut.write(imports.strip() + "\n")
                                    break
                    writeOut.write("from tMayaUIs_bin.gui.layoutOut.dockCorrect import *\n")
                    writeOut.write("from functools import partial\n")
                    writeOut.write("\n")
                    for rows in writeFile:
                        writeOut.writelines(rows)

    def write_dictFromFile(self):

        with open(self.dictPath, "w+") as writeLayoutLibrary:

            writeLayoutLibrary.write("# !/usr/bin/env python\n")

            writeLayoutLibrary.write("# -*-coding:utf-8-*-\n\n")

            writeLayoutLibrary.write("\"\"\"\nLayout Library for tMayaUIs Plug-in\n\"\"\"\n\n")

            for funcs in self.functionsIn.keys():

                if funcs.find("lt_") == 0:
                    writeLayoutLibrary.write("from tMayaUIs_bin.gui.layoutOut import %s\n" % funcs)

            writeLayoutLibrary.write("\n")

            writeLayoutLibrary.write("# Defines list of available layouts.\n")

            writeLayoutLibrary.write("lDict = {\n")

            for funcs in self.functionsIn.keys():
                if funcs.find("lt_") == 0:
                    if funcs != self.functionsIn.keys()[-1]:
                        writeLayoutLibrary.write("\t\"%s\": %s.%s,\n" % (funcs, funcs, funcs))
                    elif funcs == self.functionsIn.keys()[-1]:
                        writeLayoutLibrary.write("\t\"%s\": %s.%s\n}\n" % (funcs, funcs, funcs))

    def write_dictFromFolder(self):

        with open(self.dictPath, "w+") as writeLayoutLibrary:

            writeLayoutLibrary.write("# !/usr/bin/env python\n")

            writeLayoutLibrary.write("# -*-coding:utf-8-*-\n\n")

            writeLayoutLibrary.write("\"\"\"\nLayout Library for tMayaUIs Plug-in\n\"\"\"\n\n")

            for funcs in self.layoutFiles:

                if funcs.find("lt_") == 0:
                    writeLayoutLibrary.write("from tMayaUIs_bin.gui.layoutOut import %s\n" % funcs.split(".py")[0])

            writeLayoutLibrary.write("\n")

            writeLayoutLibrary.write("# Defines list of available layouts.\n")

            writeLayoutLibrary.write("lDict = {\n")

            for funcs in self.layoutFiles:
                if funcs.find("lt_") == 0:
                    if funcs != self.layoutFiles[-1]:
                        writeLayoutLibrary.write("\t\"%s\": %s.%s,\n" % (
                        funcs.split(".py")[0], funcs.split(".py")[0], funcs.split(".py")[0]))
                    elif funcs == self.layoutFiles[-1]:
                        writeLayoutLibrary.write("\t\"%s\": %s.%s\n}\n" % (
                        funcs.split(".py")[0], funcs.split(".py")[0], funcs.split(".py")[0]))
