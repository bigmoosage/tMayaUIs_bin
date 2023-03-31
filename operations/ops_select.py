"""
Scripts for selection queries in Maya
Tom Wood 2020
"""

import maya.cmds as cd
import pymel.core as pm

def simpletypelist(*args):

    basicTypes = [

        'mesh',
        'nurbsCurve',
        'transform',
        'joint',
        'locator',
        'nurbsSurface'

    ]

    return basicTypes

class Selected:

    """
    Gets and stores all the useful info from selected objects, for use and/or manipulation.
    """

    def __init__(self, shps=True, xforms=True, type="ALL", space="world"):

        # DATA
        self.typelist = simpletypelist()

        # For specific single obj operations
        self.single = False

        # To limit selection type to specified type.
        if type != "ALL":
            if type not in simpletypelist():
                raise Exception('ObjectType {} not recognised, must be in {}'.format(type, simpletypelist()))

            self.typeLimit = type

        # Transform Nodes
        self.objs = []
        self.sel()

        # Number of objects selcted
        self.objN = len(self.objs)

        # Tests for single object selection
        if len(self.objs) == 1:
            self.single = True
            self.transformNode = self.objs[0]
            self.singleObj()

        # Transforms, World and Relative
        # Get the transforms for multiple objs
        elif self.objN > 1:
            self.single = False

            if xforms:
                # get all the transform stuff
                self.piv = []
                self.pos = []
                self.rot = []
                self.scale = []
                self.getXforms()

        if shps:
            # Get all the shapes
            self.shapes = []
            self.types = []
            self.shapeInfo()

    def __str__(self):
        if self.single and len(self.types) == 1:
            return f'{self.transformNode} is a {self.types[0]}'
        else:
            return f'The selection is made up of {self.objN} Objects'

    def __repr__(self):
        return f'Selection (Objs: {len(self.objs)}. Single Selection: {self.single})'

    def sel(self):

        self.objs = pm.ls(sl=True, fl=True)

    def singleObj(self):

        self.shapes = cd.listRelatives(self.transformNode, shapes=True)
        for shape in self.shapes:

            if shape in simpletypelist():

                self.types.append(cd.objectType(shape))

    # Grabs all the shapeNodes for the given selection.
    def shapeInfo(self):
        for obj in self.objs:
            for shapes in cd.listRelatives(obj, shapes=True):
                self.shapes.append(shapes)

    # Gets the types of all the shapes in selection
    def getTypes(self):
        for shape in self.shapes:
            self.types.append(pm.objectType(shape))

    # Returns xform of objects inputted - can use qXform(sel())
    def getXforms(self):

        if self.singleObj:
            self.piv = pm.xform(self.transformNode, q=True, piv=True, ws=True)
            self.pos = pm.xform(self.transformNode, q=True, t=True, ws=True)
            self.rot = pm.xform(self.transformNode, q=True, ro=True, euler=True, ws=True)
        else:
            for transform in self.objs:
                self.piv.append(pm.xform(transform, q=True, piv=True, ws=True))
                self.pos.append(pm.xform(transform, q=True, t=True, ws=True))
                self.rot.append(pm.xform(transform, q=True, ro=True, euler=True, ws=True))