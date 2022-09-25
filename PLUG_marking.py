# PLUG_marking.py

# ================================================================= #
#                                                                   #
#   __   __  _______  ______    ___   _  ___   __    _  _______     #
#   |  |_|  ||   _   ||    _ |  |   | | ||   | |  |  | ||       |   #
#   |       ||  |_|  ||   | ||  |   |_| ||   | |   |_| ||    ___|   #
#   |       ||       ||   |_||_ |      _||   | |       ||   | __    #
#   |       ||       ||    __  ||     |_ |   | |  _    ||   ||  |   #
#   | ||_|| ||   _   ||   |  | ||    _  ||   | | | |   ||   |_| |   #
#   |_|   |_||__| |__||___|  |_||___| |_||___| |_|  |__||_______|   #
#                                                                   #
# ================================================================= #

# ==============================================
# Imports
# ==============================================
# Python Built-ins
import csv
import os
import re
import shutil
import string
from ConfigParser import ConfigParser
from functools import partial

# API
import maya.OpenMaya as om
import maya.OpenMayaMPx as ommpx
from maya import OpenMayaUI as omui
# CMDS/PyMel/Mel
import maya.cmds as cd
from maya import mel
import pymel.core as pm
from pymel.core import uitypes as ut

# PYSIDE
try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance

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
# CFG Creation in Users Docs
# ===================================
preferencesDir = os.path.expanduser('~/Clean Maya Marking')
# Creates preferences dir if doesn't exist
if not os.path.exists(preferencesDir):
    os.mkdir(preferencesDir)
# Prefs File
preferencesFile = os.path.join(preferencesDir, "prefs.cfg")
# Example Class Directory
example_class_dir = os.path.normpath(os.path.join(preferencesDir, "EXAMPLE"))
# Defaults prefs var definitions
defaultCFG = {
    "info": [["Author", "Tom Wood 2020"], ["version", "0.1a"], ["license", "MIT License 2020"]],
    "Classes": [["D3Dxxx Example 01", os.path.normpath(os.path.join(example_class_dir, "Tri 3 2020"))]]
}
studentListHeaders = ["Student Number", "First Name", "Last Name", "email"]
contentDirs = ["Maya Project", "Nuke Scripts", "Video", "Images", "PDFs", "Other"]
# Create preference file if doesn't exist
if not os.path.isfile(preferencesFile):
    cfgParse = ConfigParser()
    for section in defaultCFG.keys():
        if not cfgParse.has_section(section):
            cfgParse.add_section(section)
        for values in defaultCFG.get(section):
            if isinstance(values, list):
                cfgParse.set(section, values[0], values[1])
    with open(preferencesFile, "w") as cfg_write:
        cfgParse.write(cfg_write)


# Creates Example Class
def class_example_create():
    # Stored Example
    exampleDir = os.path.join(preferencesDir, "EXAMPLE")
    examplePeriodDir = os.path.join(exampleDir, "Tri 3 2020")
    exampleClassDir = os.path.join(examplePeriodDir, "D3Dxxx Example 01")
    exampleStudentListFile = os.path.join(exampleClassDir, "student_list.csv")
    exampleAssessments = ["A1 - Plan", "A2 - Final"]
    exampleStudentList = [
        ["0000000T", "John", "3. Smith", "john_smith@email.com"],
        ["1000000T", "Toni", "1. Banana", "toni_banana@email.com"],
        ["2000000T", "Frances", "2. Burgham", "frances_burgham@email.com"]
    ]
    # CFG Creation in User Docs
    if not os.path.exists(exampleDir):
        os.mkdir(exampleDir)
    if not os.path.exists(examplePeriodDir):
        os.mkdir(examplePeriodDir)
    if not os.path.exists(exampleClassDir):
        os.mkdir(exampleClassDir)
    if not os.path.isfile(exampleStudentListFile):
        with open(exampleStudentListFile, "w") as studentList_write:
            write_studentListCsv = csv.writer(studentList_write)
            write_studentListCsv.writerow(studentListHeaders)
            write_studentListCsv.writerows(exampleStudentList)
    for assessment in exampleAssessments:
        assessmentDir = os.path.join(exampleClassDir, assessment)
        if not os.path.exists(assessmentDir):
            os.mkdir(assessmentDir)
        with open(exampleStudentListFile, "r") as studentList_read:
            read_studentListCsv = csv.reader(studentList_read)
            for row in read_studentListCsv:
                if row != studentListHeaders:
                    studentPath = os.path.join(assessmentDir, "%s_%s_%s" % (row[2], row[1], row[0]))
                    if not os.path.exists(studentPath):
                        os.mkdir(studentPath)
                    for content in contentDirs:
                        contentPath = os.path.join(studentPath, content)
                        if not os.path.exists(contentPath):
                            os.mkdir(contentPath)


# Creates Example Class if Example Directory doesn't exist in Prefs path
if not os.path.exists(example_class_dir):
    class_example_create()


# Reset preferences to defaults.
def reset_prefs(*args):
    reset_parse = ConfigParser()
    for section in defaultCFG.keys():
        reset_parse.add_section(section)
        for values in defaultCFG.get(section):
            reset_parse.set(section, values[0], values[1])
    with open(preferencesFile, "w") as cfg_reset:
        reset_parse.write(cfg_reset)


# ===================================
# STRINGS
# ===================================
# Converts string to camel case
def camel(string):
    words = string.split(' ')
    if len(words) == 1:
        return string[0].lower() + string[1:]
    words[0] = words[0].lower()
    for x in range(1, len(words), 1):
        first = words[x][0].upper()
        words[x] = first + words[x][1:]
    camelStr = ''
    for w in words:
        camelStr = camelStr + w
    return camelStr


# Removes punctuation and vowels for vShortname
def shortName(string):
    shortNameStr = camel(string)

    chars = ['a', 'e', 'i', 'o', 'u', '', '_']

    for s in shortNameStr:

        if s in chars:
            shortNameStr = shortNameStr.replace(s, '')

    return shortNameStr


# ===================================
# Window Creator Class
# ===================================
class Window:

    def __init__(self,
                 title="New Window",
                 height=None,
                 width=None,
                 bgc=None,
                 resizeToFitChildren=True,
                 sizeable=True,
                 toolbox=None,
                 layout=None,
                 dock=False,
                 dockArea=None,
                 menuBar=None
                 ):

        if 'MayaWindow|' + shortName(title) + 'Dock' in pm.lsUI(type='dockControl'):
            pm.deleteUI('MayaWindow|' + shortName(title) + 'Dock')
        try:
            pm.deleteUI(shortName(title) + 'Dock')
        except:
            pass
        try:
            pm.deleteUI(shortName(title))
        except:
            pass

        if shortName(title) in pm.lsUI(windows=True):
            pm.deleteUI(shortName(title))

        """Empty Variables"""

        self.scriptjobs = []

        # Extra Window Args
        windowArgs = {}

        # Layout returns
        output = []

        """Changes to window arguments based on inputs"""

        # Specified Height
        if height is not None:
            windowArgs['height'] = height

        # Specified Width
        if width is not None:
            windowArgs['width'] = width

        # If background colour (bgc) is passed in; setting argument to input
        if bgc is not None:
            windowArgs['bgc'] = bgc

        # Sizeability
        if sizeable is not None:
            windowArgs['sizeable'] = sizeable

        # Is Toolbox
        if toolbox is not None:
            windowArgs['toolbox'] = toolbox

        # Query if layout is input
        if layout is None:
            print("WINDOW NEEDS LAYOUT: layout=[func]")
            return

        if dock is True:
            self.uiType = "dock"
            self.dockArea = "left"
            if dockArea is not None:
                if dockArea in ["left", "right"]:
                    self.dockArea = dockArea
                    self.allowedArea = ["left", "right"]
                elif dockArea == "bottom":
                    self.dockArea = dockArea
                    self.allowedArea = dockArea

        else:
            self.uiType = "win"

        if menuBar is not None:
            windowArgs["menuBar"] = True

        """Window Start"""

        # Window definition
        self.window = pm.window(shortName(title),
                                t=title, docTag="cleanMarkingUI",
                                **windowArgs)

        if windowArgs.get("menuBar") is True:
            menuBar(self.window)

        if dockArea == "bottom":
            self.holderLayout = pm.rowLayout(shortName(title) + "Row01", nc=len(layout) + 1, parent=self.window)
            for lt in layout:
                output.append(lt(self.holderLayout, uiType=self.uiType))
                pm.setParent(self.holderLayout)
        else:
            # Main column layout
            self.holderLayout = pm.columnLayout(shortName(title) + "Column01", adj=True, parent=self.window)
            # For functions in list layout inputted
            for lt in layout:
                output.append(lt(self.holderLayout, uiType=self.uiType))
                pm.setParent('..')

        pm.setParent(self.holderLayout)

        """Window Layout End"""

        for sj in output:

            if isinstance(sj, list):

                for multiSJ in sj:

                    if isinstance(multiSJ, int):
                        self.scriptjobs.append(multiSJ)

            elif isinstance(sj, int):

                self.scriptjobs.append(sj)

        closeLabel = 'CLOSE'

        if self.scriptjobs:
            print('ScriptJobs in Win: %s' % self.scriptjobs)
            closeLabel = closeLabel + ' and KILL SCRIPT JOB '
            pm.window(self.window, edit=True, cc=self.killScriptJobs)

        if dock is True:

            self.window = pm.dockControl(shortName(title) + 'Dock',
                                         content=self.window,
                                         allowedArea=self.allowedArea,
                                         sizeable=True,
                                         docTag="tMayaUI",
                                         area=self.dockArea)
            if self.scriptjobs:
                pm.dockControl(self.window, edit=True, cc=self.killScriptJobs)

        else:
            self.button = pm.button(l=closeLabel, parent=self.holderLayout, c=self.deleteUI)

            pm.showWindow(self.window)

    def deleteUI(self, *args):

        if self.uiType == "win":

            pm.deleteUI(self.window)

        elif self.uiType == "dock":

            pm.deleteUI(self.window)

    def killScriptJobs(self):

        pm.scriptJob(kill=self.scriptjobs)


# ===================================
# DATA
# ===================================
class Data:

    def __init__(self, *args):
        self.preferences = ConfigParser()
        self.preferences.read(preferencesFile)
        self.classes = self.preferences.options("Classes")
        self.studentList = []
        self.assessments = []
        self.classPath = ""
        self.period = ""
        self.className = ""

    def update_prefs(self):
        self.preferences = ConfigParser()
        self.preferences.read(preferencesFile)
        self.classes = self.preferences.options("Classes")

    def class_scroll(self, scrollListIn, *args):
        self.update_prefs()
        scrollList = ut.TextScrollList(scrollListIn)
        scrollList.removeAll()
        for savedClass in self.classes:
            classPath = self.preferences.get("Classes", savedClass)
            scrollList.append("%s" % (savedClass.upper()))

    def write_pref(self, *args):
        with open(preferencesFile, "w") as cfg_update:
            self.preferences.write(cfg_update)

    def delete_class(self, scrollListIn, *args):
        scrollList = ut.TextScrollList(scrollListIn)
        selectedItem = scrollList.getSelectItem()[0]
        try:
            self.preferences.remove_option("Classes", selectedItem.split(" -")[0])
            self.write_pref()
            self.class_scroll(scrollListIn)
        except:
            raise RuntimeError("Could not find Class to remove from Preferences")

    def csv_student_list(self, scrollFieldIn, *args):
        scrollFieldString = ut.ScrollField(scrollFieldIn).getText()
        byRow = scrollFieldString.split("\n")
        for row in byRow:
            self.studentList.append(row.split(","))

    def new_class(self, className, classPath):
        self.preferences.set("Classes", className, os.path.normpath(classPath))
        self.write_pref()

    def create_class(self, classPath, className, semTri, semTriNum, year, student_scrollList, assessment_layout,
                     student_layout, *args):

        self.studentList = []
        scrollListText = student_scrollList().split("\n")
        for student in scrollListText:
            if student and student.split(","):
                self.studentList.append([student_part for student_part in student.split(",") if student_part != ""])

        self.assessments = []
        rowChildren = [child for child in pm.layout(assessment_layout, query=True, ca=True) if
                       child.find("rowLayout") == 0]
        for rows in rowChildren[2:]:
            children = pm.layout(rows, query=True, ca=True)
            assessmentName = ut.TextField(children[1]).getText()
            pdfPath = ut.TextField(children[2]).getText()
            self.assessments.append([assessmentName, pdfPath])

        self.classPath = classPath()
        self.semTri = semTri()
        self.semTriNum = semTriNum()
        self.year = year()
        self.className = className()

        self.period = "%s %s %s" % (self.year, self.semTri, self.semTriNum)

        challengeString = ""
        if student_scrollList() == "StudentNumber,FirstName,LastName,Email":
            challengeString += "Add Some Students"

        if challengeString != "":
            challenge = pm.confirmDialog(
                title="reset prefs",
                message=challengeString,
                button=['Continue'],
                defaultButton='Continue',
                cancelButton='Continue',
                dismissString='Continue'
            )
            if challenge == "Continue":
                ut.FrameLayout(pm.layout(student_layout, q=True, parent=True)).setCollapse(False)
                return

        period_path = os.path.join(self.classPath, self.period)
        if not os.path.exists(period_path):
            os.mkdir(period_path)
        class_path = os.path.join(period_path, self.className)
        if not os.path.exists(class_path):
            os.mkdir(class_path)
        self.update_prefs()
        self.new_class(self.className, os.path.normpath(period_path))
        self.write_pref()
        student_list_file = os.path.join(class_path, "student_list.csv")
        if not os.path.isfile(student_list_file):
            with open(student_list_file, "w") as write_student_list:
                csvWriter = csv.writer(write_student_list)
                csvWriter.writerow(studentListHeaders)
                csvWriter.writerows(self.studentList)
        elif os.path.isfile(student_list_file):
            challenge = pm.confirmDialog(
                title="OverWrite",
                message='OverWrite Student List?',
                button=['Yes (OverWrite)', 'No (Read)'],
                defaultButton='No (Read)',
                cancelButton='No (Read)',
                dismissString='No (Read)'
            )
            if challenge == 'Yes (OverWrite)':
                with open(student_list_file, "w") as write_student_list:
                    csvWriter = csv.writer(write_student_list)
                    csvWriter.writerow(studentListHeaders)
                    csvWriter.writerows(self.studentList)
            else:
                with open(student_list_file, "r") as read_student_list:
                    self.studentList = []
                    csvReader = csv.reader(read_student_list)
                    for row in csvReader:
                        if row != studentListHeaders:
                            self.studentList.append(row)
        for assessment in self.assessments:
            assessmentPath = os.path.join(class_path, assessment[0])
            if not os.path.exists(assessmentPath):
                os.mkdir(assessmentPath)
            assessment_pdf = assessment[1]
            if os.path.isfile(assessment_pdf):
                try:
                    shutil.copy(assessment_pdf, assessmentPath)
                except IOError:
                    print("%s Not Copied, probably due to permission error, Move Manually" % os.path.basename(
                        assessment_pdf))
            folderNum = 1
            for student in self.studentList:
                student_assessment_path = os.path.join(assessmentPath,
                                                       "%s. %s_%s_%s" % (folderNum, student[2], student[1], student[0]))
                if not os.path.exists(student_assessment_path):
                    os.mkdir(student_assessment_path)
                    folderNum += 1
                for file_folder in contentDirs:
                    file_folder_path = os.path.join(student_assessment_path, file_folder)
                    if not os.path.exists(file_folder_path):
                        os.mkdir(file_folder_path)

        pm.deleteUI(shortName("Create Class"))


# Global Row Vars
studentRowNumber = 0
assessmentRowNumber = 0

# ===================================
# GAME BOY COLOURS
# ===================================
# UI COLOURS
GRAY2 = 'rgb(40,40,40)'
GRAY1 = 'rgb(20,20,20)'
BLUEGREENDARK = 'rgb(27, 47, 47)'
BLUEGREENMED1 = 'rgb(52, 94, 94)'
BLUEGREENMED = 'rgb(77, 121, 121)'
BLUEGREENMED2 = 'rgb(170, 200, 200)'
BLUEGREENLIGHT1 = 'rgb(131, 215, 215)'
BLUEGREENLIGHT2 = 'rgb(180, 250, 250)'

GREENDARK = 'rgb(37, 69, 47)'
DARKRED = 'rgb(23, 6, 3)'
BROWNDARK = 'rgb(56, 55, 40)'
GRAYGREEN = 'rgb(84, 120, 103)'
GREEN = 'rgb(87, 126, 52)'
BROWN = 'rgb(121, 112, 97)'
YELLOWGREENLIGHT = 'rgb(175, 195, 51)'
BROWNLIGHT = 'rgb(177, 165, 102)'
WHITEBLUE = 'rgb(170, 191, 176)'
WHITEGREEN = 'rgb(216, 231, 143)'
WHITEYELLOW = 'rgb(227, 213, 153)'
WHITE = 'rgb(225, 240, 231)'

RED = 'rgb(255, 0, 0)'
RED1 = 'rgb(25, 10, 10)'
RED2 = 'rgb(50, 45, 45)'
RED3 = 'rgb(76, 0, 0)'
RED4 = 'rgb(102, 0, 0)'
RED5 = 'rgb(127, 0, 0)'
RED6 = 'rgb(153, 0, 0)'
RED7 = 'rgb(178, 0, 0)'
RED8 = 'rgb(204, 0, 0)'
RED9 = 'rgb(229, 0, 0)'

FAIL = 'rgb(200, 0, 0)'
PASS = 'rgb(150, 90, 90)'
CREDIT = 'rgb(100, 100, 100)'
DIST = 'rgb(80, 100, 160)'
HDIST = 'rgb(40, 80, 200)'



defaultText = {
    "color": BLUEGREENMED2,
    #"font-family": "tahoma, verdana"
}
frame1 = {
    "background-color": BROWNDARK
}
frame2 = {
    "background-color": DARKRED
}
frame3 = {
    "background-color": GREEN
}
frame4 = {
    "background-color": BROWN
}
redText = {
    "color": WHITEYELLOW,
    "font-family": "Arial, Helvetica, sans-serif",
    "font-size": "12px",
}
listText = {
    "color": BLUEGREENLIGHT1,
    "font-family": "courier-new",
    "font-weight": "bold",
    "font-size": "12px",
}
feedbackText = {
    "color": BLUEGREENLIGHT1,
    "font-family": "Arial, Helvetica, sans-serif",
    "font-size": "12px",
}
header = {
    "color": BROWN
}
csvList = {
    "color": BLUEGREENMED2,
    "font-family": "courier-new",

}
defaultType = {
    "color": BLUEGREENLIGHT1,
    "font-family": "Arial, Helvetica, sans-serif",
    "font-size": "12px",
    "background-color": RED2
}
style_main_col = {
    "background-color": GRAY2
}

style_title = {
    "color": BLUEGREENMED2,
    "font-family": "impact, Helvetica, sans-serif",
    "font-style": "bold",
    "font-size": "15px",
    "background-color": GRAY2
}
style_grades = {
    "font-style": "bold",
    "font-family": "impact",
    "font-size": "15px",
    "color": RED7,
    "align": "center"
}
style_marks = {
    "font-style": "bold",
    "font-family": "impact",
    "font-size": "15px",
    "color": BLUEGREENMED2,
    "align": "center"
}

buttonStyle = {
    "color": BLUEGREENMED,
    "font-family": "Arial, Helvetica, sans-serif",
    "font-style": "bold",
    "font-size": "10px",
    "background-color": GRAY2
}
defaultStyles = {
    "font-style": "normal",
    "font-variant": "allcaps",
    "font-weight": "normal",
    "font-size": "20px",
    "font-family": "Arial, Helvetica, sans-serif",
    "color": YELLOWGREENLIGHT,
    "text-transform": "uppercase",
    "background-color": GREEN,
    "padding": "10px"
}
GRADEF = {
    "background-color": FAIL,
    "font-style": "bold",
    "font-family": "impact",
    "font-size": "15px",
}
GRADEP = {
    "background-color": PASS,
    "font-style": "bold",
    "font-family": "impact",
    "font-size": "15px",
}
GRADEC = {
    "background-color": CREDIT,
    "font-style": "bold",
    "font-family": "impact",
    "font-size": "15px",
}
GRADED = {
    "background-color": DIST,
    "font-style": "bold",
    "font-family": "impact",
    "font-size": "15px",
}
GRADEHD = {
    "background-color": HDIST,
    "font-style": "bold",
    "font-family": "impact",
    "font-size": "15px",
}



def qtStyle(widget, **kwargs):
    styleSheet = ""

    if widget is not None:
        ptr = omui.MQtUtil.findControl(widget)

        widget = wrapInstance(long(ptr), QWidget)

    for attr, value in kwargs.items():
        styleSheet += "%s:%s;" % (attr, value)

        widget.setStyleSheet(styleSheet)


# ===================================
# GUI
# ===================================
class Gui:

    # Class Init
    def __init__(self):
        self.class_data = Data()

    # Class Create Layout
    def layout_create_class(self, parentIn, uiType="win", *args):

        assessmentRowNumber = 0

        def gui_resize(*args):

            if "AssessmentFrame" in cd.lsUI(type="frameLayout") and "StudentListFrame" in cd.lsUI(type="frameLayout"):
                aC = ut.FrameLayout("AssessmentFrame").getCollapse()
                sC = ut.FrameLayout("StudentListFrame").getCollapse()
                if aC is True and sC is True:
                    ut.Window(shortName("Create Class")).setHeight(150)
                elif aC is True and sC is not True:
                    ut.Window(shortName("Create Class")).setHeight(409)
                elif sC is True and aC is not True:
                    ut.Window(shortName("Create Class")).setHeight(267)

        def reformat_csv_content(scrollFieldIn, *args):
            """FILTERS CSV CONTENT"""
            inScrollField = ut.ScrollField(scrollFieldIn)

            # Gets Text from scrollField
            strippedString = inScrollField.getText()
            # Set of printable characters
            # List of not required words.
            removeWords = ["Student", "Lecturer +", "Lecturer", "Yes", "No", "Username", "Options", "Menu:", "+", "?",
                           ""]

            # Printable Characters
            printableChars = set(string.printable)

            # Text from scrollField
            mString = strippedString

            # Re Test
            searchObject = re.search(r"\d{8,}t", mString)

            # Removes everything before first student number
            mString = mString.split(searchObject.group())[1]

            # Rebuilds string after removing string before first student number
            mString = searchObject.group() + mString

            # Removes literal unknowns
            mString = mString.replace("?", "")

            # Filters out any character not in Printable Characters
            mString = filter(lambda x: x in printableChars, mString)

            # Removes specific words known not to be needed
            mString = filter(lambda x: x not in removeWords, mString.split("\n"))

            # Strips trailing and leading spaces
            mString = [stripped.strip() for stripped in mString]

            # Creates List of Lists, knowing length of data row - 4
            infoLength = 4
            csvList = []
            myIter = -1

            for x in range(len(mString)):
                if x % infoLength == 0:
                    csvList.append([])
                    myIter += 1
                csvList[myIter].append(mString[x])

            printableString = ""
            for items in mString:
                if items.find("@") != -1 and items != mString[-1]:
                    printableString += "%s\n" % items
                elif items == mString[-1]:
                    printableString += items
                else:
                    printableString += "%s," % items

            inScrollField.setText(printableString)

        def create_assessment_row(*args):

            def path_to_pdf(*args):
                pdf_path_dialog = pm.fileDialog2(
                    fileFilter="PDF Files (*.pdf)",
                    dialogStyle=2,
                    fileMode=4,
                    caption="Pdf Path",
                    okCaption="set"
                )
                if pdf_path_dialog and os.path.isfile(pdf_path_dialog[0]):
                    pdfPath.setText(pdf_path_dialog[0])

            global assessmentRowNumber
            if len(pm.layout(assessmentCol, query=True, ca=True)) == 3:
                assessmentRowNumber = 0
            assessmentRowNumber += 1

            row = pm.rowLayout(
                nc=4,
                parent=assessmentCol,
                cw4=[20, 70, 300, 80],
                adjustableColumn=3
            )
            pm.text(
                l="%s." % assessmentRowNumber
            )
            pm.textField(
                text="A%s" % assessmentRowNumber,
                parent=row,
                width=130
            )
            pdfPath = pm.textField(
                text="",
                parent=row,
                width=240
            )
            pm.button(
                l="Path to PDF",
                parent=row,
                c=path_to_pdf
            )
            return row

        def delete_assessment_row(*args):
            global assessmentRowNumber

            if len(pm.layout(assessmentCol, query=True, ca=True)) == 3:
                assessmentRowNumber = 0

            rowChildren = [child for child in pm.layout(assessmentCol, query=True, ca=True) if
                           child.find("rowLayout") == 0]
            if len(rowChildren) > 3:
                pm.deleteUI(rowChildren[-1])
                assessmentRowNumber -= 1
                ut.Window(shortName("Create Class")).setHeight((ut.Window(shortName("Create Class")).getHeight() - 60))

        def path_to_class(*args):
            pathToClass = pm.fileDialog2(caption="Path to Class", startingDirectory=preferencesDir,
                                         okCaption="set", dialogStyle=2, fileMode=3)
            if pathToClass and os.path.exists(pathToClass[0]):
                print(pathToClass[0])
                pathToClassField.setText(pathToClass[0])
            else:
                print("Cancelled")

        windowCol = pm.columnLayout(adj=True, parent=parentIn)

        # Student List Frame Start
        studentListFrame = pm.frameLayout(
            "StudentListFrame",
            l="Student List",
            parent=windowCol,
            cll=True,
            cl=True,
            cc=gui_resize,
            ec=gui_resize
        )
        studentListCol = pm.columnLayout(
            adj=True,
            parent=studentListFrame
        )
        pm.separator(
            style="none",
            height=10,
            parent=studentListCol
        )
        studentListHeaderRow = pm.rowLayout(
            nc=2,
            parent=studentListCol,
            cw2=[5, 70]
        )
        pm.separator(
            style="none",
            parent=studentListHeaderRow,
            width=5
        )
        pm.text(
            l="CSV BY ROW",
            parent=studentListHeaderRow
        )
        studentListScrollField = pm.scrollField(
            parent=studentListCol,
            text="StudentNumber,FirstName,LastName,Email",
            font="fixedWidthFont"
        )
        qtStyle(studentListScrollField, **csvList)
        csvOutButton = pm.button(
            l="Try to Convert to CSV",
            parent=studentListCol,
            c=partial(reformat_csv_content, studentListScrollField)
        )
        pm.setParent("..")  # Student List Frame END

        # Assessment Frame Start
        assessmentFrame = pm.frameLayout(
            "AssessmentFrame",
            l="Assessments",
            cll=True,
            cl=True,
            cc=gui_resize,
            ec=gui_resize,
            parent=windowCol
        )
        assessmentCol = pm.columnLayout(
            adj=True,
            parent=assessmentFrame
        )
        assessmentRowButtonRow = pm.rowLayout(
            nc=2,
            cw2=[80, 80],
            parent=assessmentCol
        )
        pm.button(
            l="New Row",
            c=create_assessment_row,
            width=80,
            parent=assessmentRowButtonRow
        )
        pm.button(
            l="Delete Row",
            c=delete_assessment_row,
            width=80,
            parent=assessmentRowButtonRow
        )
        pm.separator(
            style="none",
            height=10,
            parent=assessmentCol
        )
        assessmentHeaderRow = pm.rowLayout(
            nc=5,
            parent=assessmentCol
        )
        pm.separator(
            style="none",
            width=20,
            parent=assessmentHeaderRow
        )
        pm.text(
            l="Assessment:",
            parent=assessmentHeaderRow,
            width=70
        )
        pm.text(
            l="PDF?",
            parent=assessmentHeaderRow,
            width=300
        )
        pm.setParent("..")  # Student List Frame END

        sepcol = pm.columnLayout(adj=True, parent=assessmentFrame)
        pm.separator(style='none', height=8, parent=sepcol)

        # Create Class Start
        createCol = pm.columnLayout(
            adj=True,
            parent=windowCol
        )
        createClassRow = pm.rowLayout(
            nc=2,
            parent=createCol,
            adjustableColumn=1
        )
        pathToClassField = pm.textField(
            text=preferencesDir,
            parent=createClassRow,
            height=25
        )
        pathToClassButton = pm.button(
            l="Path to Class",
            parent=createClassRow,
            c=path_to_class,
            height=20,
            width=100
        )
        semTriRow = pm.rowLayout(
            nc=4,
            parent=createCol,
            adjustableColumn=2
        )
        pm.text(
            l="Period: ",
            parent=semTriRow,
            width=65,
            align="left"
        )
        semTriOptionMenu = pm.optionMenu(
            "SemTriOptionMenu",
            parent=semTriRow
        )
        pm.menuItem(
            l="Trimester",
            parent=semTriOptionMenu
        )
        pm.menuItem(
            l="Semester",
            parent=semTriOptionMenu
        )
        numberField = pm.intField(
            value=1,
            parent=semTriRow,
            width=30
        )
        yearField = pm.intField(
            value=2020,
            parent=semTriRow,
            width=80
        )
        classNameRow = pm.rowLayout(
            nc=2,
            parent=createCol,
            adjustableColumn=2
        )
        pm.text(
            l="Class Name: ",
            parent=classNameRow,
            width=65,
            align="left"
        )
        classNameField = pm.textField(
            text="e.g. D3D201A Character Animation 1",
            parent=classNameRow
        )

        createClassButton = pm.button(
            l="Create Class",
            parent=createCol,
            c=partial(
                self.class_data.create_class,
                pathToClassField.getText,
                classNameField.getText,
                semTriOptionMenu.getValue,
                numberField.getValue,
                yearField.getValue,
                studentListScrollField.getText,
                assessmentCol, studentListCol)
        )

        pm.setParent("..")
        create_assessment_row()
        gui_resize()

    # Main Window Layout
    def layout_main_win(self, parentIn, uiType="win"):
        def window_resize(*args):
            pm.window(shortName("Clean Marking GUI"), edit=True, height=20)

        def dbl_click_list(listIn, *args):
            pathFromFile = ConfigParser()
            pathFromFile.read(preferencesFile)
            selectedClassPath = pathFromFile.get("Classes", listIn.getSelectItem()[0])
            os.startfile(selectedClassPath)

        def gradeChanger(*args):
            mark = ut.IntField("StudentMark").getValue()
            gradeFieldIn = ut.TextField("StudentGrade")
            if mark < 50:
                gradeFieldIn.setText("F")
                qtStyle(gradeFieldIn, **GRADEF)
            elif 50 <= mark < 65:
                gradeFieldIn.setText("P")
                qtStyle(gradeFieldIn, **GRADEP)
            elif 65 <= mark < 75:
                gradeFieldIn.setText("C")
                qtStyle(gradeFieldIn, **GRADEC)
            elif 75 <= mark < 85:
                gradeFieldIn.setText("D")
                qtStyle(gradeFieldIn, **GRADED)
            elif mark >= 85:
                gradeFieldIn.setText("HD")
                qtStyle(gradeFieldIn, **GRADEHD)
            else:
                gradeFieldIn.setText("None")


        def layout_studentFeedback(feedback_col_in, classListIn, *args):

            def read_students(classPathIn, class_name_in):

                studentListFile = os.path.join(os.path.join(classPathIn, class_name_in), "student_list.csv")
                if os.path.isfile(studentListFile):
                    with open(studentListFile, "r") as student_list:
                        read_csv = csv.reader(student_list)
                        for row in read_csv:
                            pass
                else:
                    raise Exception("%s doesn't exist." % studentListFile)

            def createAOptions(rowIn, classPathIn, class_name_in):
                aDir = os.path.join(classPathIn, class_name_in)
                aOptions = os.listdir(aDir)[:-1]
                assessmentOptions = pm.optionMenu(
                    "AssessmentOptionsMenu",
                    parent=rowIn,
                    width=200,
                    height=30,
                    cc=partial(findFeedBack, classPathIn, class_name_in)
                )
                for optionIn in aOptions:
                    pm.menuItem(
                        l=optionIn,
                        parent=assessmentOptions
                    )
                createStudentOptions(rowIn, classPathIn, class_name_in)

            def createStudentOptions(rowIn, classPathIn, class_name_in, *args):
                if len(pm.layout(rowIn, q=True, ca=True)) == 2:
                    pm.deleteUI(pm.layout(rowIn, q=True, ca=True)[1])
                aDir = ut.OptionMenu("AssessmentOptionsMenu").getValue()
                aPath = os.listdir(os.path.join(os.path.join(classPathIn, class_name_in), aDir))
                studentOptions = pm.optionMenu(
                    "StudentOptionsMenu",
                    parent=rowIn,
                    width=200,
                    height=30,
                    cc=partial(findFeedBack, classPathIn, class_name_in)
                )
                for students in aPath:
                    if not os.path.isfile(students) and not students.lower().endswith(".pdf"):
                        pm.menuItem(l=", ".join(students.split("_")[:-1]), parent=studentOptions)

            def findFeedBack(classPathIn, class_name_in, *args):
                aDir = ut.OptionMenu("AssessmentOptionsMenu").getValue()
                aPath = os.path.join(os.path.join(classPathIn, class_name_in), aDir)
                studentDir = ""
                folderName = ut.OptionMenu("StudentOptionsMenu").getValue().split(" ")[0]
                nothingText = "Replace this and Add Feedback for:\n\t%s\n\t%s" % (
                    ut.OptionMenu("AssessmentOptionsMenu").getValue(), ut.OptionMenu("StudentOptionsMenu").getValue())

                for students in os.listdir(aPath):
                    if students.find(folderName) == 0:
                        studentDir = students
                        break
                if studentDir:
                    studentPath = os.path.join(aPath, studentDir)
                else:
                    raise Exception("Couldn't find student path.")
                feedbackFile = os.path.join(studentPath, "feedback.txt")
                if os.path.isfile(feedbackFile):
                    with open(feedbackFile, "r") as read_feedback:
                        lines = read_feedback.readlines()
                        if len(lines) > 1:
                            ut.ScrollField("FeedBackScrollField").setText("".join(lines[1:]))
                        else:
                            ut.ScrollField("FeedBackScrollField").setText("".join(nothingText))
                        ut.IntField("StudentMark").setValue(int(lines[0].split(" ")[0]))
                        ut.TextField("StudentGrade").setText(lines[0].split(" ")[1])
                else:
                    ut.ScrollField("FeedBackScrollField").setText(nothingText)
                    ut.IntField("StudentMark").setValue(50)
                    ut.TextField("StudentGrade").setText("P")
                gradeChanger()

            def save_feedback(classPathIn, class_name_in, *args):
                aDir = ut.OptionMenu("AssessmentOptionsMenu").getValue()
                aPath = os.path.join(os.path.join(classPathIn, class_name_in), aDir)
                studentDir = ""
                folderName = ut.OptionMenu("StudentOptionsMenu").getValue().split(" ")[0]
                for students in os.listdir(aPath):
                    if students.find(folderName) == 0:
                        studentDir = students
                        break
                if studentDir:
                    studentPath = os.path.join(aPath, studentDir)
                else:
                    raise Exception("Couldn't find student path.")
                feedbackFile = os.path.join(studentPath, "feedback.txt")
                markText = ut.IntField("StudentMark").getValue()
                gradeText = ut.TextField("StudentGrade").getText()
                feedbackText = ut.ScrollField("FeedBackScrollField").getText()
                saveString = str(markText) + " " + gradeText + "\n" + feedbackText
                with open(feedbackFile, "w") as write_feedback:
                    write_feedback.write(saveString)

            def set_maya_project(class_path_in, *args):
                aDir = ut.OptionMenu("AssessmentOptionsMenu").getValue()
                aPath = os.path.join(class_path_in, aDir)
                folderName = ut.OptionMenu("StudentOptionsMenu").getValue().split(" ")[0]
                for students in os.listdir(aPath):
                    if students.find(folderName) == 0:
                        studentDir = students
                        break
                student_dir = os.path.join(aPath, studentDir)
                mayaProjectFolder = os.path.join(student_dir, "Maya Project")
                if os.path.exists(mayaProjectFolder) and os.path.isfile(
                        os.path.join(mayaProjectFolder, "workspace.mel")):
                    pm.workspace(mayaProjectFolder, openWorkspace=True)
                else:
                    pm.confirmDialog(
                        title="MayaProject",
                        message='NO MAYA PROJECT',
                        button=['Ok'],
                        defaultButton='Ok',
                        cancelButton='Ok',
                    )

            def open_file_folder(class_path_in, *args):
                aDir = ut.OptionMenu("AssessmentOptionsMenu").getValue()
                aPath = os.path.join(class_path_in, aDir)
                folderName = ut.OptionMenu("StudentOptionsMenu").getValue().split(" ")[0]
                for students in os.listdir(aPath):
                    if students.find(folderName) == 0:
                        studentDir = students
                        break
                student_dir = os.path.join(aPath, studentDir)
                os.startfile(student_dir)

            classListScrollIn = ut.TextScrollList(classListIn)
            if not classListScrollIn.getSelectItem():
                raise Exception("SELECT A CLASS")
            if pm.layout("FeedBackFrame", q=True, exists=True):
                pm.deleteUI("FeedBackFrame")

            selectedClassName = classListScrollIn.getSelectItem()[0]
            pathFromFile = ConfigParser()
            pathFromFile.read(preferencesFile)
            selectedClassPath = pathFromFile.get("Classes", classListScrollIn.getSelectItem()[0])


            created_class_path = os.path.join(selectedClassPath, selectedClassName)

            read_students(selectedClassPath, selectedClassName)
            window_resize()

            feedBackFrame = pm.frameLayout(
                "FeedBackFrame",
                l=selectedClassName,
                cll=True,
                cl=False,
                parent=feedback_col_in
            )
            feedBackCol = pm.columnLayout(
                adj=True,
                parent=feedBackFrame
            )
            studentOptionsRow = pm.rowLayout(
                nc=2,
                parent=feedBackCol,
                height=40
            )
            optionRows = pm.rowLayout(
                nc=2,
                parent=studentOptionsRow
            )
            setButtonRow = pm.rowLayout(
                nc=2,
                parent=studentOptionsRow
            )
            pm.button(
                l="Open File Folder",
                parent=setButtonRow,
                c=partial(open_file_folder, created_class_path),
                height=30
            )
            pm.button(
                l="Set Maya Project",
                parent=setButtonRow,
                c=partial(set_maya_project, created_class_path),
                height=30
            )
            studentRow = pm.rowLayout(
                parent=feedBackCol,
                nc=2
            )
            studentMark = pm.intField(
                "StudentMark",
                parent=studentRow,
                value=50,
                width=30,
                height=30,
            )
            qtStyle(studentMark, **style_marks)
            studentGrade = pm.textField(
                "StudentGrade",
                parent=studentRow,
                text="P",
                width=30,
                height=30,
                editable=False
            )
            qtStyle(studentGrade, **GRADEP)
            feedback = pm.scrollField(
                "FeedBackScrollField",
                parent=feedBackCol,
                width=300,
                height=400,
                wordWrap=True,
                # font="fixedWidthFont",
            )
            qtStyle(feedback, **feedbackText)
            outputButton = pm.button(
                l="Save Out",
                parent=feedBackCol,
                c=partial(save_feedback, selectedClassPath, selectedClassName)
            )
            pm.setParent("..")  # Feedback Column End
            pm.setParent("..")  # Feedback Frame End

            createAOptions(optionRows, selectedClassPath, selectedClassName)
            findFeedBack(selectedClassPath, selectedClassName)
            studentMark.changeCommand(partial(gradeChanger, studentMark, studentGrade))
            studentMark.enterCommand(partial(gradeChanger, studentMark, studentGrade))
            studentMark.receiveFocusCommand(partial(gradeChanger, studentMark, studentGrade))
            ut.FrameLayout("FeedBackFrame").collapseCommand(window_resize)
            ut.FrameLayout("FeedBackFrame").expandCommand(window_resize)
            gradeChanger(studentMark, studentGrade)

        col = pm.columnLayout(
            adj=True,
            parent=parentIn
        )

        classFrame = pm.frameLayout(
            "ClassFrame",
            l="CLASS LIST - Dbl Click for Folder Open",
            cll=True,
            cl=False,
            parent=col
        )
        classFrameCol = pm.columnLayout(
            adj=True
        )
        classScrollList = pm.textScrollList(
            parent=classFrameCol
        )
        qtStyle(classScrollList, **listText)
        buttonForm = pm.formLayout(numberOfDivisions=100)

        classLoadButton = pm.button(
            l="LOAD",
            parent=buttonForm,
            width=150,
            c=partial(layout_studentFeedback, col, classScrollList)
        )
        createClassButton = pm.button(
            l="New Class",
            parent=buttonForm,
            width=80,
            height=20,
            c=self.gui_create_class
        )
        classRefreshButton = pm.button(
            l="Refresh List",
            parent=buttonForm,
            width=80,
            height=20,
            c=partial(self.class_data.class_scroll, classScrollList)
        )
        classDeleteButton = pm.button(
            l="Delete Class",
            parent=buttonForm,
            width=80,
            height=20,
            c=partial(self.class_data.delete_class, classScrollList)
        )

        pm.setParent("..")  # Frame End
        pm.setParent("..")  # Column End
        pm.setParent("..")  # Main Layout End

        # Control Edits
        classFrame.collapseCommand(window_resize)
        classFrame.expandCommand(window_resize)
        classScrollList.doubleClickCommand(partial(dbl_click_list, classScrollList))
        formAttach = [
            (classLoadButton, 'left', 5),
            (classLoadButton, 'top', 5),
            (classLoadButton, 'bottom', 5),
            (createClassButton, 'right', 175),
            (createClassButton, 'top', 5),
            (createClassButton, 'bottom', 5),
            (classRefreshButton, 'right', 90),
            (classRefreshButton, 'top', 5),
            (classRefreshButton, 'bottom', 5),
            (classDeleteButton, 'right', 5),
            (classDeleteButton, 'top', 5),
            (classDeleteButton, 'bottom', 5)
        ]
        formAttachPosition = [(classLoadButton, "right", 5, createClassButton)]
        pm.formLayout(buttonForm, edit=True, attachForm=formAttach, attachControl=formAttachPosition)
        self.class_data.class_scroll(classScrollList)

    # License Gui
    def licence_gui(self, *args):

        # License Window Layout
        def layout_license(parentIn, uiType="win"):
            cd.columnLayout(
                parent=parentIn
            )
            cd.rowLayout(
                nc=3
            )
            cd.separator(
                width=15,
                style="none"
            )
            cd.columnLayout()
            cd.separator(
                height=15,
                style="none"
            )
            cd.text(
                l=kLICENSE,
                align="left"
            )
            cd.separator(
                height=15,
                style="none"
            )
            cd.setParent("..")
            cd.separator(
                width=15,
                style="none"
            )
            cd.setParent("..")
            cd.setParent("..")

            # ss(parentIn, bgColour=qtCol(0.2, 0.2, 0.2))
            # ss(col, bgColour=qtCol(0.25, 0.2, 0.2))
            # ss(createFrame, bgColour=qtCol(0.35, 0.35, 0.35))
            # ss(savedFrame, bgColour=qtCol(0.3, 0.3, 0.3))
            # ss(createCol, bgColour=qtCol(0.3, 0.3, 0.3))
            # ss(createText, bgColour=qtCol(0.2, 0.2, 0.2))
            # ss(uiSep, bgColour=qtCol(0.2, 0.2, 0.2))

        licenseWin = Window(title="License Info", layout=[layout_license])
        qtStyle(licenseWin.window, **defaultText)
        qtStyle(licenseWin.button, **buttonStyle)

    # Challenge to reset prefs
    def reset_pref_challenge(self, *args):
        challenge = pm.confirmDialog(
            title="reset prefs",
            message='Are you sure?\nNo Files Will be deleted\nClass Prefs will be reset.',
            button=['Yes', 'No'],
            defaultButton='No',
            cancelButton='No',
            dismissString='No'
        )
        if challenge == "Yes":
            reset_prefs()
            mel.eval("cleanMarking;")

    # MenuBar
    def menuBar_gui(self, parentIn):
        helpMenu = cd.menu(
            label="help",
            helpMenu=True,
            parent=parentIn
        )
        # menuItem1 = cd.menuItem(label="How to Use", parent=helpMenu)
        cd.menuItem(
            label="Reset",
            parent=helpMenu,
            c=self.reset_pref_challenge
        )
        cd.menuItem(
            label="License",
            parent=helpMenu,
            c=self.licence_gui
        )

    def gui_create_class(self, *args):
        CREATE_CLASS_WIN = Window(title="Create Class", layout=[self.layout_create_class], toolbox=True, sizeable=True)
        qtStyle(CREATE_CLASS_WIN.window, **defaultText)
        qtStyle(CREATE_CLASS_WIN.button, **buttonStyle)

        ut.Window(shortName("Create Class")).setHeight(50)

    def gui_main_win(self):
        MAIN_WIN = Window(title="Clean Marking GUI", layout=[self.layout_main_win], toolbox=True, sizeable=True,
                          menuBar=self.menuBar_gui)
        qtStyle(MAIN_WIN.window, **defaultText)
        qtStyle(MAIN_WIN.button, **buttonStyle)
        ut.Window(shortName("Clean Marking GUI")).setHeight(50)
        ut.Window(shortName("Clean Marking GUI")).setWidth(616)


# ===================================
# PLUGIN
# ===================================
# Class that initializes command.
class Marking_GUI_Command(ommpx.MPxCommand):
    kPluginCmdName = "cleanMarking"

    # Initial method, initializes command structure
    def __init__(self):
        ommpx.MPxCommand.__init__(self)

    # Doit method is called once during command.
    def doIt(self, args):
        Gui().gui_main_win()

    # Command creator Method
    @classmethod
    def cmdCreator(cls):
        return ommpx.asMPxPtr(cls())


# ===================================
# PLUGIN INITIALISATION
# ===================================
# Initialize Plugin
def initializePlugin(mobject):
    mplugin = ommpx.MFnPlugin(mobject,
                              kAuthorName,
                              kPluginVersion,
                              kRequiredApiVersion)

    Gui().gui_main_win()

    try:
        mplugin.registerCommand(Marking_GUI_Command.kPluginCmdName, Marking_GUI_Command.cmdCreator)
    except:
        raise Exception('Failed to register: %s' % Marking_GUI_Command.kPluginCmdName)


# DeInitialize Plugin
def uninitializePlugin(mobject):
    mplugin = ommpx.MFnPlugin(mobject)

    for cleanWindows in cd.lsUI(windows=True):
        if cd.window(cleanWindows, q=True, docTag=True) == "cleanMarkingUI":
            cd.deleteUI(cleanWindows)

    try:
        mplugin.deregisterCommand(Marking_GUI_Command.kPluginCmdName)
    except:
        raise Exception('Failed to register: %s' % Marking_GUI_Command.kPluginCmdName)
