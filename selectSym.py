import maya.cmds as cd
import pymel.core as pm
from pymel.core import nodetypes as nt


def SELECT_ONE_SIDE(axis):

    xform_node = pm.ls(sl=True)[0]

    shape_node = pm.ls(sl=True, dag=True, type='mesh')[0]

    t_piv = xform_node.getPivots(worldSpace=True)[0]

    for mVert in shape_node.vtx:
        if mVert[axis] < t_piv[axis]:
            pm.select(mVert, add=True)