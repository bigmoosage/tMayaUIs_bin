import pymel.core as pm
import maya.cmds as cd


def controlWalkGen(inUI):
    parentUI = inUI
    yield parentUI
    try:
        level1 = cd.layout(parentUI, q=True, ca=True)
    except RuntimeError:
        level1 = []
    if level1:
        for lvl1 in level1:
            yield lvl1
            try:
                level2 = cd.layout(lvl1, q=True, ca=True)
            except RuntimeError:
                level2 = []
            if level2:
                for lvl2 in level2:
                    yield lvl2
                    try:
                        level3 = cd.layout(lvl2, q=True, ca=True)
                    except RuntimeError:
                        level3 = []
                    if level3:
                        for lvl3 in level3:
                            yield lvl3
                            try:
                                level4 = cd.layout(lvl3, q=True, ca=True)
                            except RuntimeError:
                                level4 = []
                            if level4:
                                for lvl4 in level4:
                                    yield lvl4
                                    try:
                                        level5 = cd.layout(lvl4, q=True, ca=True)
                                    except RuntimeError:
                                        level5 = []
                                    if level5:
                                        for lvl5 in level5:
                                            yield lvl5
                                            try:
                                                level6 = cd.layout(lvl5, q=True, ca=True)
                                            except RuntimeError:
                                                level6 = []
                                            if level6:
                                                for lvl6 in level6:
                                                    yield lvl6
                                                    try:
                                                        level7 = cd.layout(lvl6, q=True, ca=True)
                                                    except RuntimeError:
                                                        level7 = []
                                                    if level7:
                                                        for lvl7 in level7:
                                                            yield lvl7
                                                            try:
                                                                level8 = cd.layout(lvl7, q=True, ca=True)
                                                            except RuntimeError:
                                                                level8 = []
                                                            if level8:
                                                                for lvl8 in level8:
                                                                    yield lvl8
                                                                    try:
                                                                        level9 = cd.layout(lvl8, q=True, ca=True)
                                                                    except RuntimeError:
                                                                        level9 = []
                                                                    if level9:
                                                                        for lvl9 in level9:
                                                                            yield lvl9
                                                                            try:
                                                                                level10 = cd.layout(lvl9, q=True, ca=True)
                                                                            except RuntimeError:
                                                                                level10 = []
                                                                            if level10:
                                                                                for lvl10 in level10:
                                                                                    yield lvl10
                                                                                    try:
                                                                                        level11 = cd.layout(lvl9,
                                                                                                            q=True,
                                                                                                            ca=True)
                                                                                    except RuntimeError:
                                                                                        level11 = []
                                                                                    if level11:
                                                                                        for lvl11 in level11:
                                                                                            yield lvl11
                                                                                            try:
                                                                                                level12 = cd.layout(
                                                                                                    lvl11, q=True,
                                                                                                    ca=True)
                                                                                            except RuntimeError:
                                                                                                level12 = []
                                                                                            if level12:
                                                                                                for lvl12 in level12:
                                                                                                    yield lvl12
                                                                                                    try:
                                                                                                        level13 = cd.layout(
                                                                                                            lvl12,
                                                                                                            q=True,
                                                                                                            ca=True)
                                                                                                    except RuntimeError:
                                                                                                        level13 = []
                                                                                                    if level13:
                                                                                                        for lvl13 in level13:
                                                                                                            yield lvl13