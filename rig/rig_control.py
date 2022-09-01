"""
Module to create rig controls
"""

# built-ins
import inspect

# Maya built-in
import pymel.core as pm

# My modules
from tMayaUIs_bin.objects import obj_curves
from tMayaUIs_bin.operations import ops_select
from tMayaUIs_bin.manip import dt_objnaming
from tMayaUIs_bin.manip import dt_namingConvention as nc

class Control:
    """
    class to build rigging controls
    """

    def __init__(self,
                 ctype='',
                 name='new',
                 side='',
                 scale=1.0,
                 translateto=None,
                 rotateto=None,
                 channels=None,
                 haveControl=None,
                 createCurve=True,
                 obj=None,
                 directionaxis=(0, 0, 0),
                 constrain=False,
                 pivotPos=None
                 ):

        if obj is None and translateto is None and rotateto is None:
            translateto = ops_select.sel()[0]
            rotateto = ops_select.sel()[0]

        if obj is not None:
            translateto = obj
            rotateto = obj

        name = translateto.split('_')[2][:-2]

        side = dt_objnaming.findside(translateto)

        if channels is None:
            channels = ['s', 'v']

        if directionaxis[0] is not 0 and directionaxis[2] is not 0:
            print ("directionAxis is the axis along which the control is visually:"
                   "\nFOR \'DIRECTIONAL\' CONTROLS"
                   "\nWORKS AS EXPECTED IF CURVE IS FLAT TO Y AND POINTING ALONG X"
                   "\ne.g:"
                   "\n(0,0,0) - DEFAULT: pointing along x and "
                   "\n(0,1,0) - Control up in y"
                   "\n(0,0,1) - Control pointed along z"
                   "\n(-1,1,0) - Control up in y and pointed along -x"
                   )

        curveTypes = {}

        def str_to_func(fName):
            return getattr(obj_curves, fName)

        for f in dir(obj_curves):
            if inspect.isfunction(str_to_func(f)) is True:
                curveTypes[f] = str_to_func(f)

        # Available sides for class
        sides = {
            'left': '_l_',
            'right': '_r_',
            'mid': '_mid_'
        }

        # Stores side of object to name based on side value
        if side in sides:

            sideName = sides.get(side)

        else:

            sideName = '_'

        # Creates transform object to hold controller offset.
        ctrlOffset = pm.spaceLocator(n='offsetLoc' + sideName + name + '01')
        pm.setAttr(ctrlOffset.getShape() + '.overrideEnabled', 1)
        pm.setAttr(ctrlOffset.getShape() + '.overrideVisibility', 0)

        # Query for the creation of the curve to represent the control object.
        if createCurve is True:
            if ctype in curveTypes:

                ctrlObject = curveTypes.get(ctype)('ctrl' + sideName + name + '01')
                if pivotPos is not None:
                    pm.xform(ctrlObject, rp=pivotPos, ws=True)
                    pm.xform(ctrlObject, translation=[pivotPos[0]*-1, pivotPos[1]*-1, pivotPos[2]*-1])
                pm.setAttr(ctrlObject + '.scaleX', scale)
                pm.setAttr(ctrlObject + '.scaleY', scale)
                pm.setAttr(ctrlObject + '.scaleZ', scale)
                pm.setAttr(ctrlObject + '.rotateX', 90 * directionaxis[1])
                pm.setAttr(ctrlObject + '.rotateY', -90 * directionaxis[2])
                if directionaxis[0] == -1:
                    pm.setAttr(ctrlObject + '.rotateY', 180)
                pm.makeIdentity(ctrlObject, a=True, s=True, r=True, t=True)



            else:
                ctrlObject = pm.circle(n='ctrl' + sideName + name + '01', ch=False, normal=[1, 0, 0], radius=scale)[0]

            # Changes colour based on name input left(l_)=Red, right(r_) = Blue
            ctrlObjectShape = ctrlObject.getShapes()

            for shape in ctrlObjectShape:

                pm.setAttr(shape + '.overrideEnabled', 1)

                pm.setAttr(shape + '.overrideRGBColors', 1)

                if side == 'left':

                    pm.setAttr(shape + '.overrideColorRGB', [1, 0, 0])

                elif side == 'right':

                    pm.setAttr(shape + '.overrideColorRGB', [0, 0, 1])

                else:

                    pm.setAttr(shape + '.overrideColorRGB', [0, 1, 1])

        # Parents Controller to Offset
        pm.parent(ctrlObject, ctrlOffset)

        # Move Controls Offset to Position of inputted object
        if pm.objExists(translateto):
            # Creates and removes point constraint of offset to inputted object
            pntCnstr = pm.pointConstraint(translateto, ctrlOffset, offset=[0, 0, 0], weight=1)
            pm.delete(pntCnstr)

        # Rotate Control Offset to Rotation of inputted object
        if pm.objExists(rotateto):
            # Creates and removes orient constraint of offset to inputted object
            pm.delete(pm.orientConstraint(rotateto, ctrlOffset))
            #pm.pointConstraint(translateto, ctrlObject)
        # Creates object to hold joint offset
        if constrain is True:
            # Creates and removes parent constraint
            # jointOffset = pm.delete(pm.parentConstraint(translateto, pm.group(n='chode', em=True, w=True)))
            pm.orientConstraint(ctrlObject, translateto)


        # Lock Channels inputted into class
        channelToLock = []

        for lockChan in channels:

            if lockChan in ['t', 'r', 's']:

                for axis in ['x', 'y', 'z']:
                    attr = lockChan + axis
                    channelToLock.append(attr)

            elif lockChan is 'v':

                channelToLock.append('v')

        for chan in channelToLock:
            pm.setAttr(ctrlObject + '.' + chan, l=True, k=False)

        # add public members
        self.C = ctrlObject
        self.Off = ctrlOffset

# # USEAGE:
# from tMayaUIs_bin.rig import rig_control as rc
#
# fingerList = []
#
# for sel in cd.ls(sl=True):
#     controlGrp = rc.Control(obj=sel, ctype="lineCircle", directionaxis=(0, -1, 1), scale=0.05, constrain=True)
#     finger = controlGrp.Off.split("_")[-1][:-3]
#     offO = controlGrp.Off
#     if finger not in fingerList:
#         fingerList.append(finger)
#     else:
#         pm.parent(nt.Transform(offO), nt.Transform(parentO))
#
#     parentO = controlGrp.C