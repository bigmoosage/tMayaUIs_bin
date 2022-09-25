import maya.cmds as cd


class winAll3D:
    def __init__(self):
        result = cd.promptDialog(title='Really?',
                                 message='Enter Name:',
                                 button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel',
                                 dismissString='Cancel')
