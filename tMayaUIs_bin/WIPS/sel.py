from functools import partial
import maya.cmds as cd


def clearPlease(*args):
    cd.select(cl=True)


def changeText(b, *args):
    try:
        o = cd.ls(sl=True)[0]
        cd.textField(b, e=True, tx=o)
    except:
        cd.textField(b, e=True, tx="Select Somthing.")


def closeWin(Window, *args):
    cd.deleteUI(Window)

    WindowName = "symSelector"

    try:
        closeWin(WindowName)
    except:
        pass

    if WindowName in cd.lsUI(windows=True):
        closeWin(WindowName)

    myWin = cd.window(WindowName, t="Sean's Verts")
    cd.showWindow(myWin)
    COL1 = cd.columnLayout(p=myWin, adj=True)

    # ROW START
    ROW1 = cd.rowLayout(p=COL1, nc=3)
    objField = cd.textField(tx="OBJECT HERE", p=ROW1, w=100)
    getBut = cd.button(p=ROW1, l="Get Selection")
    clearBut = cd.button(p=ROW1, l="Clear Selection")
    cd.setParent('..')

    doROW = cd.rowLayout(p=COL1, nc=2)
    chckCol = cd.columnLayout(p=doROW)
    cd.radioButtonGrp(numberOfRadioButtons=3, label="AXIS:  ", labelArray3=['x', 'y', 'z'], p=chckCol,
                      columnWidth4=[40, 30, 30, 30], select=1)
    cd.checkBoxGrp(numberOfCheckBoxes=1, label="   DIR:  ", label1='POS/NEG', p=chckCol, columnWidth2=[40, 20],
                   columnAlign2=["left", "left"], v1=1)
    butCol = cd.columnLayout(p=doROW)
    cd.button(l="SELECT", p=butCol)

    cd.button(clearBut, edit=True, c=clearPlease)
    cd.button(getBut, edit=True, c=partial(changeText, objField))
    closeBut = cd.button(l="close", c=partial(closeWin, WindowName), p=COL1)
