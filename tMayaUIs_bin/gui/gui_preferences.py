"""
GUI for preference updater
"""

# Built-ins
from functools import partial

# Maya imports
import maya.cmds as cd

# Config Manipulation
from tMayaUIs_bin.conf import cfg
from tMayaUIs_bin.conf import cfg_UpdateLayoutLib
from tMayaUIs_bin.conf import lib_layouts
# Layout imports
from tMayaUIs_bin.gui import gui_Window
from tMayaUIs_bin.gui import gui_styles
from tMayaUIs_bin.gui import gui_controlWalk

from tMayaUIs_bin.manip import dt_colour

# --------------- #
#   CONFIG INIT   #
# --------------- #
configUpdater = cfg.Config()

columnWidth = 300
buttonHeight = 25


# Prefence Update Window.
def preferenceGUI(parentIn, *args, **kwargs):
    def changeOrder(direction, *args):

        listLength = cd.textScrollList(orderTxtScroll, q=True, ni=True)

        if listLength > 0:

            selectedItem = cd.textScrollList(orderTxtScroll, query=True, si=True)

            selectedItemIndex = int(cd.textScrollList(orderTxtScroll, query=True, sii=True)[0])

            if direction == "up":

                if selectedItemIndex > 1:
                    cd.textScrollList(orderTxtScroll,
                                      edit=True,
                                      ri=selectedItem
                                      )
                    cd.textScrollList(orderTxtScroll,
                                      edit=True,
                                      appendPosition=[selectedItemIndex - 1, selectedItem[0]]
                                      )
                    cd.textScrollList(orderTxtScroll, edit=True, sii=selectedItemIndex - 1)

            elif direction == "down":

                if selectedItemIndex < listLength:
                    cd.textScrollList(orderTxtScroll,
                                      edit=True,
                                      ri=selectedItem
                                      )
                    cd.textScrollList(orderTxtScroll,
                                      edit=True,
                                      appendPosition=[selectedItemIndex + 1, selectedItem[0]]
                                      )
                    cd.textScrollList(orderTxtScroll, edit=True, sii=selectedItemIndex + 1)

            else:
                pass

    def listSwap(inList, *args):

        fromList = inList
        lists = [orderTxtScroll, layoutTxtScroll]
        try:
            toList = (str(lst) for lst in lists if lst != fromList).next()
        except:
            toList = next(str(lst) for lst in lists if lst != fromList)

        # Query selected item.
        selectedItem = cd.textScrollList(fromList, q=True, si=True)
        # Remove the selected item from the list
        cd.textScrollList(fromList, e=True, ri=selectedItem)
        # Append to other list
        cd.textScrollList(toList, edit=True, append=selectedItem)

    def resetLists(*args):
        cd.textScrollList(orderTxtScroll, edit=True, ra=True)
        cd.textScrollList(layoutTxtScroll, edit=True, ra=True)
        for layout in lib_layouts.lDict:
            cd.textScrollList(layoutTxtScroll, edit=True, append=layout)

    def refreshListFromFolder(*args):

        cfg_UpdateLayoutLib.UpdateLayouts().write_dictFromFolder()

        reload(lib_layouts)

        resetLists()

    def createWin(uiType, *args):

        if cd.textScrollList(orderTxtScroll, query=True, ai=True):

            inGui = []
            inGuiSTRING = []

            for layouts in cd.textScrollList(orderTxtScroll, query=True, ai=True):
                inGui.append(lib_layouts.lDict.get(layouts))

            if uiType == "dock":
                gui_Window.Window(title="Quick Dock", layout=inGui, dock=True)

            else:
                gui_Window.Window(title="Quick Win", layout=inGui)

        else:
            raise TypeError("ADD SOME LAYOUTS")

    def updateSaveUIsScroll(*args):

        configUpdater.refresh()

        cd.textScrollList(savedTextScroll, edit=True, ra=True)

        for savedLayout in configUpdater.sections:

            if configUpdater.cfgData.has_option(savedLayout, "uiType"):

                if configUpdater.cfgData.get(savedLayout, "uiType") == "win":
                    addedString = "(win)"
                    if configUpdater.cfgData.getboolean(savedLayout, "onStart"):
                        addedString = "(win - Startup)"
                    cd.textScrollList(savedTextScroll, edit=True, append="%s %s" % (savedLayout, addedString))

                elif configUpdater.cfgData.get(savedLayout, "uiType") == "dock":
                    addedString = "(dock)"
                    if configUpdater.cfgData.getboolean(savedLayout, "onStart"):
                        addedString = "(dock - Startup)"
                    cd.textScrollList(savedTextScroll, edit=True, append="%s %s" % (savedLayout, addedString))

    def dblClickList(*args):

        cWin = cd.textScrollList(savedTextScroll, query=True, si=True)[0].split(" (")[0]

        layoutsIn = [lib_layouts.lDict.get(lFunc) for lFunc in configUpdater.cfgData.get(cWin, "layouts").split(",")]

        if configUpdater.cfgData.get(cWin, "uiType") == "win":
            isDock = False

        elif configUpdater.cfgData.get(cWin, "uiType") == "dock":
            dockArea = configUpdater.cfgData.get(cWin, "dockArea")
            isDock = True

        else:
            isDock = False

        if layoutsIn and isDock is True:
            gui_Window.Window(title=cWin, layout=layoutsIn, dock=isDock, dockArea=dockArea)

        else:
            gui_Window.Window(title=cWin, layout=layoutsIn, dock=isDock)

    def deleteUI(*args):

        configUpdater.cfgData.remove_section(cd.textScrollList(savedTextScroll, q=True, si=True)[0].split(" (")[0])
        configUpdater.savePrefs()
        updateSaveUIsScroll()

    def saveUI(*args):

        def saveGUI(parentIn, uiType="win"):

            def buttonCommand(*args):

                name = cd.textField(nameTextField, query=True, text=True)

                onStartVal = int(cd.checkBox(args[0][0], query=True, value=True))

                winVal = cd.checkBox(args[0][1], q=True, v=True)
                dockVal = cd.checkBox(args[0][2], q=True, v=True)
                if winVal and not dockVal:
                    saveUIType = "win"
                elif dockVal and not winVal:
                    saveUIType = "dock"
                else:
                    saveUIType = "win"
                sideList = ["left", "right", "bottom"]
                sideVal = sideList[cd.optionMenu(args[0][3], q=True, select=True)-1]

                if isinstance(cd.textScrollList(orderTxtScroll, query=True, ai=True), list):

                    configUpdater.newWin(
                        name,
                        ",".join(cd.textScrollList(orderTxtScroll, query=True, ai=True)),
                        onStartVal,
                        saveUIType,
                        sideVal
                    )

                    configUpdater.savePrefs()
                    updateSaveUIsScroll()

                    cd.deleteUI(savePrefWin.window)

                else:
                    raise TypeError("NEEDS SOME LAYOUTS FROM ABOVE")

            def checkBoxSet(cBoxIn, cBoxOut, *args):

                cd.checkBox(cBoxIn, edit=True, value=not cd.checkBox(cBoxOut, q=True, value=True))
                cd.optionMenu(dockSideOption, edit=True, enable=cd.checkBox(isDockCheck, q=True, value=True))

            column = cd.columnLayout(adj=True, parent=parentIn, width=columnWidth)
            nameTextField = cd.textField(text="nameUI", parent=column)
            uiCheckRow = cd.rowLayout(parent=column, nc=4)
            onStart = cd.checkBox(l="On Start?", parent=uiCheckRow, v=0, width=columnWidth / 4)
            isWinCheck = cd.checkBox(l="win", parent=uiCheckRow, v=1, width=columnWidth / 5)
            isDockCheck = cd.checkBox(l="dock", parent=uiCheckRow, v=0, width=columnWidth / 5)
            dockSideOption = cd.optionMenu(label='', parent=uiCheckRow, width=columnWidth / 4, enable=False)
            cd.menuItem(label='left', parent=dockSideOption)
            cd.menuItem(label='right', parent=dockSideOption)
            cd.menuItem(label='bottom', parent=dockSideOption)
            cd.optionMenu(dockSideOption, edit=True)
            cd.setParent('..')

            controlsIn = [onStart , isWinCheck, isDockCheck, dockSideOption]
            uiSaveButton = cd.button(l="save", c=partial(buttonCommand, controlsIn), parent=column)

            cd.setParent('..')  # Column end

            # Add Commands
            cd.checkBox(isWinCheck, edit=True, cc=partial(checkBoxSet, isDockCheck, isWinCheck))
            cd.checkBox(isDockCheck, edit=True, cc=partial(checkBoxSet, isWinCheck, isDockCheck))

        savePrefWin = gui_Window.Window(title="Save UI Dialog", layout=[saveGUI], sizeable=True)

    def resetPrefs(*args):

        resetChallenge = cd.confirmDialog(
            title='Reset Prefs',
            message='Are you sure?',
            button=['Yes', 'No'],
            defaultButton='No',
            cancelButton='No',
            dismissString='No'
        )

        if resetChallenge == "Yes":
            configUpdater.resetPrefs()
            updateSaveUIsScroll()
    def copyCode(*args):
        newText = createWin(uiType=True, create=False)
        cd.textField("copyCodeTextField", edit=True, text=newText)

    # Main Column
    col = cd.columnLayout(adj=True, parent=parentIn, width=300)

    # Main Frame
    createFrame = cd.frameLayout(l="Create UI", cll=False, cl=False, parent=col)

    # Frame Column
    createCol = cd.columnLayout(adj=True, parent=createFrame, width=columnWidth)

    # Pane layout for ordering and build
    layoutPane = cd.paneLayout(parent=createCol, configuration="vertical2")

    # Txt scroll for layout list order
    orderTxtColumn = cd.columnLayout(adj=True, parent=layoutPane)
    cd.text(label="Layout Order", font="boldLabelFont", parent=orderTxtColumn)
    orderTxtScroll = cd.textScrollList(parent=orderTxtColumn, height=220)
    cd.button(l=">>>", parent=orderTxtColumn, height=buttonHeight, c=partial(listSwap, orderTxtScroll))

    # Txt scroll for available layouts
    layoutTxtColumn = cd.columnLayout(adj=True, parent=layoutPane)
    cd.text(label="Available Layouts", font="boldLabelFont", parent=layoutTxtColumn)
    layoutTxtScroll = cd.textScrollList(parent=layoutTxtColumn, height=220)
    cd.button(l="<<<", parent=layoutTxtColumn, height=buttonHeight, c=partial(listSwap, layoutTxtScroll))

    # Pane Buttons
    upButton = cd.button(l="up", parent=orderTxtColumn, height=buttonHeight, width=columnWidth / 2,
                         c=partial(changeOrder, "up"))
    downButton = cd.button(l="down", parent=orderTxtColumn, height=buttonHeight, width=columnWidth / 2,
                           c=partial(changeOrder, "down"))
    reset = cd.button(l="reset", parent=layoutTxtColumn, height=buttonHeight, width=columnWidth / 2, c=resetLists)
    refreshLayouts = cd.button(l="refresh", parent=layoutTxtColumn, height=buttonHeight, width=columnWidth / 2,
                               c=refreshListFromFolder)

    # Create ui controls
    createText = cd.text(l="Create:", align="left", height=buttonHeight, parent=orderTxtColumn)
    uiSep = cd.separator(style="none", height=buttonHeight, parent=layoutTxtColumn)
    createWinButton = cd.button(l="Quick Window", height=buttonHeight, parent=orderTxtColumn, width=columnWidth / 2,
                                c=partial(createWin, "win"))
    createDockButton = cd.button(l="Quick Dock", height=buttonHeight, parent=layoutTxtColumn, width=columnWidth / 2,
                                 c=partial(createWin, "dock"))
    saveUIButton = cd.button(l="Save Layout", parent=createCol, c=saveUI)
    # copyCodeText = cd.textField("copyCodeTextField", text="Window Code", parent=createCol)
    # copyCodeButton = cd.button(l="COPY Window Code - For Button", parent=createCol, c=copyCode)

    cd.setParent('..')  # Pane End
    cd.setParent('..')  # Frame Column End
    cd.setParent('..')  # Frame End

    cd.separator(style='none', parent=col, height=15)

    savedFrame = cd.frameLayout(l="Saved UIs - Double Click", parent=col, cll=False, cl=False)
    savedCol = cd.columnLayout(adj=True, parent=savedFrame)

    savedTextScroll = cd.textScrollList(parent=savedCol, dcc=dblClickList)

    deleteUIButton = cd.button(l="deleteUI", parent=savedCol, c=deleteUI)
    refreshUIsButton = cd.button(l="Refresh List", parent=savedCol, c=updateSaveUIsScroll)

    resetPrefsButton = cd.button(l="Reset Preferences", height=buttonHeight, parent=savedCol, c=resetPrefs)

    cd.setParent('..')  # Frame Column End

    cd.setParent('..')  # Frame End

    cd.setParent('..')  # Main Column End

    # Edits for Controls.
    for lt in lib_layouts.lDict:
        cd.textScrollList(layoutTxtScroll, edit=True, append=lt)
    updateSaveUIsScroll()

    # =======================
    #   UI STYLING
    # =======================

    cd.layout(parentIn, edit=True, width=400)

    # ss = gui_styles.Style.SetStyle
    # qtCol = dt_colour.Colour.toQTRGB
    # guiWalk = gui_controlWalk.controlWalkGen
    #
    # ss(parentIn, bgColour=qtCol(0.2, 0.2, 0.2))
    # ss(col, bgColour=qtCol(0.25, 0.2, 0.2))
    # ss(createFrame, bgColour=qtCol(0.35, 0.35, 0.35))
    # ss(savedFrame, bgColour=qtCol(0.3, 0.3, 0.3))
    # ss(createCol, bgColour=qtCol(0.3, 0.3, 0.3))
    # ss(createText, bgColour=qtCol(0.2, 0.2, 0.2))
    # ss(uiSep, bgColour=qtCol(0.2, 0.2, 0.2))
    #
    # for text in guiWalk(col):
    #     if text.find("text") == 0:
    #         ss(text, bgColour=qtCol(0.25, 0.25, 0.25), tStyle="italic", tWeight="bold",
    #            tColour=qtCol(0.25, 0.5, 0.25))
    #
    # for button in guiWalk(createFrame):
    #     if button.find("button") == 0:
    #         ss(button, bgColour=qtCol(0.25, 0.25, 0.25), tWeight="bold", tColour=qtCol(0.25, 1.0, 0.25))
    #
    # for button in guiWalk(savedFrame):
    #     if button.find("button") == 0:
    #         ss(button, bgColour=qtCol(0.25, 0.25, 0.25), tWeight="bold", tColour=qtCol(0.25, 1.0, 0.25))


# MenuBar
def tMenuBar(parentIn):
    helpMenu = cd.menu(label="help", helpMenu=True)
    menuItem1 = cd.menuItem(label="Info", parent=helpMenu)
    menuItem2 = cd.menuItem(label="License Info", parent=helpMenu)


def createWin(*args):
    gui_Window.Window(title="TMayaUi_Preferences", layout=[preferenceGUI], sizeable=False, menuBar=tMenuBar)


if __name__ == "__main__":
    createWin()