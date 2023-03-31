"""
SHAPE SPECIFIC OPERATIONS
"""

# IMPORTS
from tMayaUIs_bin.manip import dt_namingConvention
from tMayaUIs_bin.operations import ops_select


# Maya Specific
import maya.cmds as cd
import pymel.core as pm


# EFFICIENT RENAMING OF SHAPE NODES
def shapePartRenamer(*args):
    # Alphabet inport
    alphabetList = dt_namingConvention.alphabet()
    # Available name types
    typeList = dt_namingConvention.prefix
    # Added Template
#    nameTemplate = "crvPart"
    # End string - conforms with Maya's Expectation of shape name
    nString = "01Shape"
    # Get the selected objects
    selectedObjs = cd.ls(sl=True, fl=True)
    # Loop through those objects
    for obj in selectedObjs:
        # List of all shape nodes associated with Transform Node
        shapeNodes = cd.listRelatives(obj, shapes=True)
        # List iterator
        n = 1
        # Loop to rename each shape
        for shape in shapeNodes:
            # Get the shape's type.
            typeString = dt_namingConvention.prefix(cd.objectType(shape))
            # Print the name for clarity
            print("{}_{}_{}{}".format(obj, typeString, alphabetList[n - 1], nString))
            # Rename each shape by above
            cd.rename(shape, "{}_{}_{}{}".format(obj, typeString, alphabetList[n - 1], nString))
            # Step forward on list iterator
            n = n + 1

# Separates all shapes in selection under new transforms
def unparentShapes(*args):

    selectedObjs = cd.ls(sl=True, fl=True)

    for obj in selectedObjs:

        cd.makeIdentity(obj, t=1, r=1, s=1, a=1)

        shapeNodes = cd.listRelatives(obj, shapes=True)

        for shapeN in shapeNodes:
            newXform = cd.group(em=True, world=True)

            together = cd.parent(shapeN, newXform, s=True, r=True)

            cd.rename(together, "{}{}".format(shapeN, "Shape"))

            cd.rename(newXform, shapeN)

            cd.xform(together, cpc=True, r=True)

def consolidator(*args):

    selection = cd.ls(sl=True, fl=True)

    # Initial loop to correct transforms and find bounding box for zoom correction
    for obj in selection:
        # Freeze transforms to prevent movement on run
        cd.makeIdentity(obj, a=1, t=1, r=1, s=1)

    # Stores final curve as parent
    parentTransform = selection[-1]

    # Stores objs to parent
    objsToParent = selection[0:-1]

    # Loop through each object
    for obj in objsToParent:

        # Shape nodes of each object
        shapeNodes = cd.listRelatives(o, s=True)

        # Loop through all shapes
        for shape in shapeNodes:
            # Parents the shape node under the parent's transform
            cd.parent(shape, parentTransform, s=True, r=True)

            # Delete the old empty transform
            cd.delete(obj)

            # Centre pivot on new transform
            cd.xform(cp=True)

            # Finally selects the object
            cd.select(parentTransform)

