# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
renameLayout Layout
"""

# IMPORTS
import pymel.core as pm
from tMayaUIs_bin.manip import dt_rignames
from tMayaUIs_bin.manip import dt_string
from tMayaUIs_bin.operations import ops_select as select
from tMayaUIs_bin.gui.layoutOut.dockCorrect import *
from functools import partial

# renameLayout method.
def lt_renameLayout(parentIn, uiType="win"):
    """Function Definitions for Field Control"""

    def rnmScriptJob():

        previewtext(True)

    def renameSingle(obj, txt):
        pm.rename(obj, txt)

    def printTest(obj, txt):
        print(obj)
        print(txt)

    # Changes text of preview.
    def previewtext(v):

        names = renameFunc(False)

        if len(names.n) == 1:
            previewString = names.n[0]

        else:
            previewString = names.n[0] + ' -> ' + names.n[-1]

        if names.oN != '':
            previewString = previewString + names.oN

        pm.text('previewTextRnmWin', edit=True, l=previewString)

        if pm.frameLayout('manualFrameRnmWin', q=True, cl=True) is False:
            manualNamingFrame(True)

    # Updates frame of manual naming
    def manualNamingFrame(v):

        if pm.frameLayout('manualFrameRnmWin', q=True, cl=True) == 0:

            if pm.layout('manualFrameColumnRnmWin', q=True, ca=True):

                for field in pm.layout('manualFrameColumnRnmWin', q=True, ca=True):

                    if pm.control(field, q=True, ann=True) == 'toDelete':
                        pm.deleteUI(field)

            radioButtonValue = pm.radioButtonGrp('manualFrameRadioRnmWin', q=True, select=True)

            selection = select.sel()

            allNames = renameFunc(False)

            if radioButtonValue == 1:

                names = select.sel()

                for n in names:
                    pm.nameField(object=n, width=250, ann='toDelete', parent='manualFrameColumnRnmWin')

            elif radioButtonValue == 2:

                names = allNames.n

                if selection:

                    for x in range(len(names)):
                        manRnmTxtField = pm.textField(width=250, text=names[x], ann='toDelete',
                                                      parent='manualFrameColumnRnmWin',
                                                      cc=partial(renameSingle, selection[x]),
                                                      ec=partial(renameSingle, selection[x]))

    # Queries and changes fieldStates.
    def fieldstate(v):

        partsListCheck = pm.checkBox('partsListCheckBoxRnmWin', q=True, v=True)

        if partsListCheck == 1:
            pm.checkBox('partCheckRnmWin', e=True, v=0)

        preCheck = pm.checkBox('prefixCheckRnmWin', q=True, v=True)

        sideCheck = pm.checkBox('sideCheckRnmWin', q=True, v=True)

        partCheck = pm.checkBox('partCheckRnmWin', q=True, v=True)

        pm.textFieldGrp('prefixTxtRnmWin', edit=True, enable=preCheck)

        pm.textFieldGrp('sideTxtRnmWin', edit=True, enable=sideCheck)

        pm.textFieldGrp('partTxtRnmWin', edit=True, enable=partCheck)

        pm.textField('partsListTextFieldRnmWin', edit=True, enable=partsListCheck)

        previewtext(v)

    # Populates parts list text field on menu change
    def partslistpopulate(v):

        partsList = ''

        for n in dt_rignames.names(v):
            partsList = partsList + ', ' + n

        partsList = partsList[2:]

        pm.textField('partsListTextFieldRnmWin', edit=True, text=partsList)

        previewtext(v)

    # Rename
    def renameobjs(v):

        renameFunc(True)

    def renameFunc(bool):

        rnmArgs = {}

        if pm.checkBox('prefixCheckRnmWin', query=True, value=True) == 1:
            rnmArgs['prefix'] = pm.textFieldGrp('prefixTxtRnmWin', query=True, text=True)

        if pm.checkBox('sideCheckRnmWin', query=True, value=True) == 1:
            rnmArgs['side'] = pm.textFieldGrp('sideTxtRnmWin', query=True, text=True)

        if pm.checkBox('partCheckRnmWin', query=True, value=True) == 1:
            rnmArgs['part'] = pm.textFieldGrp('partTxtRnmWin', query=True, text=True)

        if pm.checkBox('partsListCheckBoxRnmWin', query=True, value=True) == 1:
            rnmArgs['partslist'] = pm.textField('partsListTextFieldRnmWin', query=True, text=True).split(', ')

        rnmArgs['perobject'] = pm.checkBox('perObjectCheckRnmWin', query=True, value=True)

        rnmArgs['letter'] = pm.checkBox('letterCheckRnmWin', query=True, value=True)

        rnmArgs['endchain'] = pm.checkBox('endChainCheckRnmWin', query=True, value=True)

        rnmArgs['separator'] = pm.checkBox('separatorCheckRnmWin', query=True, value=True)

        rnmArgs['withconnections'] = pm.checkBox('withConnectionsCheckRnmWin', query=True, value=True)

        rnmArgs['specialpart'] = pm.checkBox('specialNameCheckRnmWin', query=True, value=True)

        rnm = dt_string.Rename(
            rename=bool,
            **rnmArgs
        )
        return rnm

    # Gui Variables
    separatorHeight = 10

    """
    Layout Start
    """

    # Main column layout
    column = pm.columnLayout(adj=True, width=200)

    # Text to hold preview of rename
    preview = pm.text('previewTextRnmWin',
                      font='boldLabelFont',
                      height=60,
                      l='Preview',
                      parent=column)

    # Column layout for position adjustment of textFieldGrps
    textColumn = pm.columnLayout(adj=True,
                                 co=['left', -100],
                                 parent=column)
    preRow = pm.rowLayout(nc=2)
    prefix = pm.textFieldGrp('prefixTxtRnmWin',
                             label='Prefix',
                             text='bn',
                             adj=0,
                             cc=previewtext,
                             parent=preRow)

    preCheck = pm.checkBox('prefixCheckRnmWin', label='',
                           value=1,
                           cc=fieldstate,
                           parent=preRow)
    pm.setParent('..')
    sideRow = pm.rowLayout(nc=2)
    side = pm.textFieldGrp('sideTxtRnmWin',
                           label='Side',
                           text='left',
                           adj=0,
                           cc=previewtext,
                           parent=sideRow)

    sideCheck = pm.checkBox('sideCheckRnmWin',
                            label='',
                            value=1,
                            cc=fieldstate,
                            parent=sideRow)
    pm.setParent('..')
    partRow = pm.rowLayout(nc=2)
    part = pm.textFieldGrp('partTxtRnmWin',
                           label='Part',
                           text='part',
                           adj=0,
                           cc=previewtext,
                           parent=partRow)

    partCheck = pm.checkBox('partCheckRnmWin',
                            label='',
                            value=1,
                            cc=fieldstate,
                            parent=partRow)
    pm.setParent('..')
    pm.setParent('..')

    checkColumn = pm.columnLayout(co=['left', 50],
                                  parent=column)

    row = pm.rowLayout(nc=3,
                       parent=checkColumn)

    stringSeparator = pm.checkBox('separatorCheckRnmWin',
                                  l='separator',
                                  v=1,
                                  cc=previewtext,
                                  parent=row)

    letter = pm.checkBox('letterCheckRnmWin',
                         l='letter',
                         v=0,
                         cc=previewtext,
                         parent=row)

    perObject = pm.checkBox('perObjectCheckRnmWin',
                            l='perObject',
                            v=0,
                            cc=previewtext,
                            parent=row)

    endChain = pm.checkBox('endChainCheckRnmWin',
                           l='endchain?',
                           v=0,
                           cc=previewtext,
                           parent=checkColumn)

    rowCheck = pm.rowLayout(nc=2, parent=checkColumn)

    withConnections = pm.checkBox('withConnectionsCheckRnmWin',
                                  l='With Connections',
                                  v=0,
                                  cc=previewtext,
                                  parent=rowCheck)

    specialCheck = pm.checkBox('specialNameCheckRnmWin',
                               l='Special Name',
                               v=0,
                               cc=previewtext,
                               parent=rowCheck)

    pm.separator(style='none',
                 h=5,
                 parent=column)

    row2 = pm.rowLayout(nc=2,
                        # ad2=1,
                        # cat=[2, 'left', 0],
                        # bgc=[0.6, 0.42, 0.18],
                        parent=column)

    menuColumn = pm.columnLayout(adj=False,
                                 co=['left', 60],
                                 # bgc=[0.6, 0.42, 0.18],
                                 parent=row2)

    partsListCheck = pm.checkBox('partsListCheckBoxRnmWin',
                                 v=0,
                                 l='',
                                 cc=fieldstate,
                                 parent=row2)

    options = pm.optionMenu(parent=menuColumn,
                            width=100,
                            cc=partslistpopulate)

    pm.menuItem(l='arm',
                parent=options)
    pm.menuItem(l='arm2',
                parent=options)
    pm.menuItem(l='leg',
                parent=options)
    pm.menuItem(l='leg2',
                parent=options)
    pm.menuItem(l='foot',
                parent=options)
    pm.menuItem(l='foot',
                parent=options)

    partsList = pm.textField('partsListTextFieldRnmWin',
                             text='Comma Separated Parts',
                             width=100,
                             height=30,
                             enable=False,
                             # bgc=[0.7, 0.7, 0.7],
                             parent=column,
                             cc=previewtext)

    pm.button(l='rename',
              bgc=[0.1, 0.25, 0.2],
              c=renameobjs,
              parent=column)

    manualFrame = pm.frameLayout('manualFrameRnmWin', l='Manual Naming', parent=column, cll=True, cl=True,
                                 ec=partial(manualNamingFrame, True))

    manualFrameColumn = pm.columnLayout('manualFrameColumnRnmWin', adj=False, co=['left', 20])

    manualNameCheck = pm.radioButtonGrp('manualFrameRadioRnmWin', select=1, nrb=2,
                                        labelArray2=['Original', 'Generated'], cc1=previewtext,
                                        parent=manualFrameColumn)

    pm.separator(h=separatorHeight,
                 parent=column)

    pm.text(font='boldLabelFont', l='GLOBAL NAMING', parent=column)

    pm.separator(h=separatorHeight, style='none',
                 parent=column)

    pm.button(l='All Iks, Effectors and Constraints in Selection', parent=column)

    pm.button(l='All Utility Nodes in selection', parent=column)

    pm.separator(h=separatorHeight, style='none',
                 parent=column)

    pm.setParent('..')

    # Change preview text on open
    previewtext(None)
    partslistpopulate('arm')
    sJob = pm.scriptJob(e=['SelectionChanged', rnmScriptJob])

    return sJob

