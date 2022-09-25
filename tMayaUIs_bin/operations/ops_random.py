import maya.cmds as cd
import random

random.seed(255)


def randomiser(t=False, r=False, s=False, scale=1.0, uniform=True, axes=None):
    if axes is None:
        axes = [1, 1, 1]
    elif not isinstance(axes, list) or len(axes) != 3:
        raise TypeError("Axes must be a List of len 3.")
    for sel in cd.ls(sl=True, fl=True):
        if t is not False:
            randList = [
                random.uniform(-1.0, 1.0) * scale,
                random.uniform(-1.0, 1.0) * scale,
                random.uniform(-1.0, 1.0) * scale
            ]
            cd.xform(
                sel,
                t=[randList[0] * axes[0], randList[1] * axes[1], randList[2] * axes[2]],
            )
        if r is not False:
            randList = [
                random.uniform(-1.0, 1.0) * scale,
                random.uniform(-1.0, 1.0) * scale,
                random.uniform(-1.0, 1.0) * scale
            ]
            cd.xform(
                sel,
                ro=[randList[0] * axes[0], randList[1] * axes[1], randList[2] * axes[2]],
            )
        if s is not False:
            if uniform is True:
                rnd = random.uniform(0.0, 1.0)
                currentScale = cd.xform(sel, q=True, r=True, s=True)[0]
                randList = [rnd * scale + currentScale, rnd * scale + currentScale, rnd * scale + currentScale]
            else:
                randList = [
                    random.uniform(0.0, 1.0) * scale + currentScale,
                    random.uniform(0.0, 1.0) * scale + currentScale,
                    random.uniform(0.0, 1.0) * scale + currentScale
                ]
            cd.xform(
                sel,
                s=[randList[0] * axes[0], randList[1] * axes[1], randList[2] * axes[2]]
            )