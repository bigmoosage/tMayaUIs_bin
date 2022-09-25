# !/usr/bin/env python
# -*-coding:utf-8-*-

"""
lt_customCurveLibrary Layout
"""

import random

# IMPORTS
import maya.cmds as cd

from tMayaUIs_bin.objects import obj_curves

from functools import partial

mSeed = random.seed(256)

# rigCurveTypes method.
def lt_customCurveLibrary(parentIn, uiType="win"):
    curves = {
        'joint': obj_curves.joint,
        'box': obj_curves.box,
        'arrow': obj_curves.arrow,
        'diamond': obj_curves.diamond,
        'tetrahedron': obj_curves.tetrahedron,
        'lineCircle': obj_curves.lineCircle,
        'loccrv': obj_curves.loccrv,
        'offArrow': obj_curves.offArrow,
        'cardinalArrow': obj_curves.cardinalArrow,
        'cardinalArrow02': obj_curves.cardinalArrow02,
        'cardinalArrow03': obj_curves.cardinalArrow03,
        'halfCircleArrow': obj_curves.halfCircleArrow,
        'circleArrow': obj_curves.circleArrow,
        'twoEndArrow': obj_curves.twoEndArrow,
        'threeDCircleArrow': obj_curves.threeDCircleArrow,
        'target': obj_curves.target,
        'oneAxisFinger': obj_curves.oneAxisFinger,
        'droplet': obj_curves.droplet,
        'man': obj_curves.man,
        'house': obj_curves.house,
        'puzzle': obj_curves.puzzle,
        'road': obj_curves.road,
        'rocket': obj_curves.rocket,
        'mountain': obj_curves.mountain,
        'tree': obj_curves.tree
    }

    cd.frameLayout(l='Custom Curves', cll=True, cl=True, parent=parentIn)
    cd.gridLayout(nc=2, cwh=[120, 30])
    for c in curves:
        name = "crv_%s01" % c
        bgc = [random.uniform(0.1, 0.5), random.uniform(0.1, 0.5), random.uniform(0.1, 0.5)]
        cd.button(l=c, c=partial(curves.get(c), name), bgc=bgc)
    cd.setParent('..')
    cd.setParent('..')
