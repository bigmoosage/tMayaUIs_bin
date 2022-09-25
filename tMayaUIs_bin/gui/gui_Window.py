"""
Window Creator Class.
"""

import pymel.core as pm
from tMayaUIs_bin.manip import dt_namingConvention as nc

class Window:

    def __init__(self,
                 title="New Window",
                 height=None,
                 width=None,
                 bgc=None,
                 rtf=None,
                 sizeable=None,
                 toolbox=None,
                 layout=None,
                 fitchildren=True,
                 dock=False,
                 dockArea=None,
                 menuBar=None
                 ):

        if 'MayaWindow|' + nc.shortName(title) + 'Dock' in pm.lsUI(type='dockControl'):
            pm.deleteUI('MayaWindow|' + nc.shortName(title) + 'Dock')
        try:
            pm.deleteUI(nc.shortName(title) + 'Dock')
        except:
            pass
        try:
            pm.deleteUI(nc.shortName(title))
        except:
            pass

        if nc.shortName(title) in pm.lsUI(windows=True):
            pm.deleteUI(nc.shortName(title))

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
            windowArgs['bgc'] = [bgc[0], bgc[1], bgc[2]]

        # Resize window to fit children
        if rtf is not None:
            windowArgs['rtf'] = rtf

        # Sizeability
        if sizeable is not None:
            windowArgs['sizeable'] = sizeable

        # Is Toolbox
        if toolbox is not None:
            windowArgs['toolbox'] = toolbox

        windowArgs['resizeToFitChildren'] = fitchildren

        # Query if layout is input
        if layout is None:
            raise AttributeError("WINDOW NEEDS LAYOUT: layout=[func]")

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
        self.window = pm.window(nc.shortName(title),
                                t=title, docTag="tMayaUI",
                                **windowArgs)

        if windowArgs.get("menuBar") is True:
            menuBar(self.window)

        if dockArea == "bottom":
            self.holderLayout = pm.rowLayout(nc.shortName(title) + "Row01", nc=len(layout)+1, parent=self.window)
            for lt in layout:
                output.append(lt(self.holderLayout, uiType=self.uiType))
                pm.setParent(self.holderLayout)
        else:
            # Main column layout
            self.holderLayout = pm.columnLayout(nc.shortName(title) + "Column01", adj=True, parent=self.window)
            # For functions in list layout inputted
            for lt in layout:
                output.append(lt(self.holderLayout, uiType=self.uiType))
                pm.setParent('..')
                pm.separator(h=10, parent=self.holderLayout)

        pm.setParent(self.holderLayout)

        """Window Layout End"""

        for sj in output:

            if isinstance(sj, list):

                for multiSJ in sj:

                    if isinstance(multiSJ, int):
                        self.scriptjobs.append(multiSJ)

            elif isinstance(sj, int):

                self.scriptjobs.append(sj)

        closeLabel = 'close'

        if self.scriptjobs:

            print('ScriptJobs in Win: %s' % self.scriptjobs)
            closeLabel = closeLabel + ' and KILL SCRIPT JOB '
            pm.window(self.window, edit=True, cc=self.killScriptJobs)

        if dock is True:

            self.window = pm.dockControl(nc.shortName(title) + 'Dock',
                                         content=self.window,
                                         allowedArea=self.allowedArea,
                                         sizeable=True,
                                         docTag="tMayaUI",
                                         area=self.dockArea)
            if self.scriptjobs:

                pm.dockControl(self.window, edit=True, cc=self.killScriptJobs)

        else:
            pm.button(l=closeLabel, parent=self.holderLayout, c=self.deleteUI)
            pm.showWindow(self.window)

    def deleteUI(self, *args):

        if self.uiType == "win":

            pm.deleteUI(self.window)

        elif self.uiType == "dock":

            pm.deleteUI(self.window)

    def killScriptJobs(self):

        pm.scriptJob(kill=self.scriptjobs)
