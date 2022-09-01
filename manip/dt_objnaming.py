"""
Names for sides in rig.
"""

# Maya imports
import pymel.core as pm

# My imports
from tMayaUIs_bin.manip import dt_namingConvention as namingConvention
#from tomLib import namingConvention
from tMayaUIs_bin.operations import ops_select as select


# Find side of connected.
def findsideofconnected(obj):
    name = ''
    if pm.objectType(obj) in namingConvention.specialPartNames().keys():

        ot = pm.objectType(obj)

        if ot == 'ikHandle':
            name = pm.listConnections(obj)[0]
            print(name)

        elif ot == 'ikEffector':
            name = pm.listConnections(obj)[1]

        else:
            for conn in pm.listConnections(obj):
                if pm.objectType(conn) == 'transform' or pm.objectType(conn) == 'joint':
                    name = conn
                    break

    return findside(name)


# Find the object types of object.
def findobjectype(obj):
    otype = ''  # Var to hold node type.

    ot = pm.objectType(obj)

    utilityNodes = ['utilityNode', 'arrayMapper', 'bump2d', 'bump3d', 'condition',
                    'distanceBetween', 'heightField', 'lightInfo', 'multiplyDivide',
                    'place2dTexture', 'place3dTexture', 'plusMinusAverage', 'projection',
                    'reverse', 'samplerInfo', 'setRange', 'stencil', 'uvChooser', 'vectorProduct']

    if ot == 'ikHandle':

        if 'ikSplineSolver' in obj.listConnections():
            otype = 'ikSplineSolver'

        elif 'ikRPsolver' in obj.listConnections():
            otype = 'ikRPsolver'

        elif 'ikSCsolver' in obj.listConnections():
            otype = 'ikSCsolver'

    elif ot in utilityNodes:

        otype = ot

    elif obj.getShape():  # Has Shape? Yes for mesh, nurbs curves etc no for iK Handles, joints, groups etc.

        otype = pm.objectType(obj.getShape())  # Adds object type to list.

    else:

        otype = ot

    return otype


# Returns the name or names associated with nodes
# that have relevant connections for naming purposes.
def findconnectionsname(obj):
    name = ''

    relatedObjName = ''
    if pm.objectType(obj) in namingConvention.specialPartNames().keys():

        ot = pm.objectType(obj)

        if ot == 'ikHandle':
            name = pm.listConnections(obj)[0].split('_')[-1]

        elif ot == 'ikEffector':
            name = pm.listConnections(obj)[1].split('_')[-1]

        elif ot in namingConvention.constraints():

            if pm.objectType(pm.listConnections(obj)[0]) in ['joint', 'transform']:
                first = pm.listConnections(obj)[0]

            else:
                first = pm.listConnections(obj)[1]

            for conn in pm.listConnections(obj):
                if conn != first:
                    second = conn
                    break

            return namingConvention.camel(str(' '.join(second.split('_')))[:-2])

        else:
            for conn in pm.listConnections(obj):
                if pm.objectType(conn) == 'transform':
                    name = conn.split('_')[-1]

        for part, subpart in namingConvention.partsDict().items():
            for x in range(len(subpart)):
                if name.find(subpart[x]) != -1:
                    relatedObjName = part
                    return relatedObjName


# Finds side objects input.
def findside(obj):
    # ONE OBJECT
    side = obj.split('_')[1]  # Sends side down for query later.

    # Identifies side and expands for string query later
    if side == 'l':
        side = 'left'

    elif side == 'r':
        side = 'right'

    elif side == 'c':
        side = 'centre'

    elif side == 'f':
        side = 'front'

    elif side == 'b':
        side = 'back'

    else:
        pm.warning(
            'NO OUTPUT: Did not recognise side from l, r, c, f or b\nReturned second element in split after \'_\'')
        return

    return side  # Returns the side that the object/objects are on in Rig


# Find part name from String.
def strFindPartName(str):
    if len(str.split('.')) != 1:
        outputStr = str.split('.')[0].split('_')[-1][:-2]
    else:
        outputStr = str.split('_')[-1][:-2]

    if outputStr[-1] in namingConvention.alphabet():
        outputStr = outputStr[:-1]

    for part, subpart in namingConvention.partsDict().iteritems():
        for sp in subpart:
            if outputStr in sp:
                return part


# Find indivpart name from string.
def strFindSubPartName(str):
    if len(str.split('.')) != 1:
        outputStr = str.split('.')[0].split('_')[-1][:-2]
    else:
        outputStr = str.split('_')[-1][:-2]

    if outputStr[-1] in namingConvention.alphabet():
        outputStr = outputStr[:-1]

    return outputStr


# Swaps side of object
def nameSideSwap():

    for name in select.sel():

        parts = name.split("_")

        type = parts[0]

        side = parts[1]

        part = parts[2][:-2]

        if side in ["r", "l", "c"]:
            if side == "r":
                newside = "l"
            elif side == "l":
                newside = "r"
            else:
                newside = side
        else:
            print("No Side For Construction")
            newSide = ""

        newName = "{}_{}_{}".format(type, newside, part + namingConvention.countString()[0])
        pm.rename(name, newName)


# Class to output specific names for object
class SpecialNames:

    def __init__(self,
                 object=None
                 ):

        # Selects objects if no inputted list
        if object is None:

            objects = select.sel()

        elif type(object) is list:

            objects = object

        else:

            objects = [object]  # If input is not a list, converts single to list for loop.

        # Definitions for output
        objTypes = []
        partNames = []
        sides = []

        # Loops through list of objects.
        for obj in objects:  # Per object in list, append outputs for each.

            objTypes.append(findobjectype(obj))  # Basic object types.

            partNames.append(findconnectionsname(
                obj))  # Name of part if object has connections - iKs, effectors, constraints, utils.

            sides.append(findsideofconnected(obj))  # Sides for each object.

        # Single object
        if len(objects) == 1:  # If only one object outputs single string.

            objTypes = objTypes[0]

            partNames = partNames[0]

            sides = sides[0]

        # Self definitions
        self.findtype = objTypes
        self.partname = partNames
        self.side = sides


