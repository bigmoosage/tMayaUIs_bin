import maya.cmds as cd
from functools import partial
import warnings


class Vertibird:

    def __init__(self, s_object, ax, direction):
        if s_object in cd.ls(type="transform"):
            self.obj = s_object
        else:
            raise AttributeError("SELECT SOMETHING")

        cd.select(cl=True)

        self.shape = cd.listRelatives(self.obj, s=True)[0]

        self.sel_vtx = cd.ls('{}.vtx[:]'.format(self.shape), fl=True)

        self.vertP = []

        for v in self.sel_vtx:
            self.vertP.append(cd.xform(v, q=True, t=True))

        self.axis = ax

        self.dir = direction

        self.pivot = []

        self.bb = []

        self.cAvg = []

    # SELECTS ONE SIDE OF OBJECTs VERTS ACROSS THE PIVOT
    def across_pivot(self):

        # Transform pivot to query relative positions
        self.pivot = cd.xform(self.obj, q=True, piv=True, ws=True)
        self.select_verts(self.pivot)


    def bounding(self):
        pass

    def multi_axis(self):
        pass

    def select_verts(self, point):
        # LOOP FOR VERTS
        for v in self.sel_vtx:
            p = cd.xform(v, q=True, ws=True, t=True)
            if self.dir == 0:
                if p[self.axis] <= point[self.axis]:
                    cd.select(v, add=True)
            elif self.dir == 1:
                if p[self.axis] >= point[self.axis]:
                    cd.select(v, add=True)


def dothething(objField, radio, check, *args):
    objOut = cd.textField(objField, q=True, tx=True)
    axis = cd.radioButtonGrp(radio, q=True, select=True) - 1
    dir = cd.checkBoxGrp(check, q=True, v1=True)
    verts = Vertibird(objOut, axis, dir)
    verts.across_pivot()


# CLEAR SELECTION
def clearPlease(*args):
    cd.select(cl=True)


# TEXT CHANGER
def changeText(b, *args):
    try:
        o = cd.ls(sl=True)[0]
        cd.textField(b, e=True, tx=o)
    except:
        cd.textField(b, e=True, tx="Select Something.")


# CLOSE WINDOW DEF
def closeWin(Window, *args):
    cd.deleteUI(Window)


# GUI WINDOW
def SeanWindow():
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
    cd.separator(h=10)
    # ROW START
    ROW1 = cd.rowLayout(p=COL1, nc=3)
    objField = cd.textField(tx="OBJECT HERE", p=ROW1, w=100)
    getBut = cd.button(p=ROW1, l="Get Selection")
    clearBut = cd.button(p=ROW1, l="Clear Selection")
    cd.setParent('..')
    cd.separator(h=10)


    pivotRadio = cd.radioButtonGrp(numberOfRadioButtons=3, label=" ", labelArray3=['Piv', 'Bound', 'Avg'], p=COL1,
                                   columnWidth4=[55, 40, 60, 40], select=1)
    cd.separator(h=10)
    axisButton = cd.radioButtonGrp(numberOfRadioButtons=3, label=" ", labelArray3=['x', 'y', 'z'], p=COL1,
                                   columnWidth4=[65, 40, 40, 40], select=1)
    spacerRow = cd.rowLayout(nc=2)
    cd.separator(p=spacerRow, w=50, style="none")
    dirButton = cd.checkBoxGrp(numberOfCheckBoxes=1, label=" ", label1='POS/NEG', p=spacerRow,
                               columnWidth2=[40, 20],
                               columnAlign2=["left", "left"], v1=1)

    cd.button(l="SELECT VERTS", p=COL1, c=partial(dothething, objField, axisButton, dirButton))
    cd.separator(h=10, p=COL1)
    cd.button(clearBut, edit=True, c=clearPlease)
    cd.button(getBut, edit=True, c=partial(changeText, objField, axisButton))
    cd.button(l="close", c=partial(closeWin, WindowName), p=COL1)


if __name__ == "__main__":
    SeanWindow()
