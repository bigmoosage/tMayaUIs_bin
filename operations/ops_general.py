import pymel.core as pm

from tMayaUIs_bin.operations import ops_select
from tMayaUIs_bin.write import Write
from tMayaUIs_bin.conv import conv_melCrvToPython

def unlockAttrs():
    attrlist = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v']

    for s in ops_select.sel():
        for a in attrlist:
            pm.setAttr(s + a, k=True)
            pm.setAttr(s + a, lock=False)


def melCrvToPython():
    namePrompt = pm.promptDialog(
            title='Curve Name',
            message='Enter Name:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')

    if namePrompt == 'OK':
        name = pm.promptDialog(q=True, text=True)
        input = conv_melCrvToPython.findmelfunction(name=name)
        Write.WriteFile(new=False, module='objs', name='curves', inputstring=input[1], work=input[0])