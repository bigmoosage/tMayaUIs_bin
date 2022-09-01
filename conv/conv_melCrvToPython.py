"""
Script for converting last mel curve command into useable curve in curves.py
"""

# built-in imports
import pymel.core as pm
import re
import inspect

# My Modules
from tomLib.objs import curves

# Method for finding the last mel curve function
def findmelfunction(name):

    scriptHistory = pm.cmdScrollFieldReporter('cmdScrollFieldReporter1', q=True, text=True)

    cmdIndex = [m.start() for m in re.finditer('curve ', scriptHistory)][-1]

    lineEnd = scriptHistory[cmdIndex:].find('\n')

    return melcrv(name, scriptHistory[cmdIndex:lineEnd+cmdIndex])


def melcrv(name, melCommand):
    reload(curves)
    for f in inspect.getmembers(curves):
        if f[0] == name:
            print('ALREADY HAS A CURVE NAMED THIS')
            return False, 'ALREADY HAS A CURVE NAMED THIS'

    def stringBuild(name, degree, ps):
        pPosString = ''
        for p in ps:
            pPosString = pPosString + '\t\t\t' + str(p) + ',\n'

        mainString = '# Create ' + name + ' curve.'\
                     '\ndef ' + name + '(name):' \
                     '\n\tcurveMake = pm.curve(' \
                     '\n\t\tname=name,\r\t\td=' + degreeN + ',\n\t\tp=[' \
                     '\n' + pPosString + '\t\t]\n\t)' \
                     '\n\tshapeNode = pm.listRelatives(curveMake, shapes=True)' \
                     '\n\tcontrol = pm.rename(shapeNode, curveMake + "Shape01")' \
                     '\n\treturn curveMake'
        return mainString

    # Finds degree


    # Finds Parameters for curve from mel command
    individualElements = melCommand.split(' ')

    degreeFlag = individualElements.index('-d')
    degreeN = individualElements[degreeFlag + 1]


    for x in range(len(individualElements)):
        if individualElements[x] == '-p':
            firstP = x
            break

    for x in range(len(individualElements)):
        if individualElements[x] == '-k':
            firstK = x
            break

    pAlone = individualElements[firstP:firstK]

    pPos = []
    for x in range(len(pAlone)):
        if pAlone[x] == '-p':
            pPos.append(x)

    ps = []
    for p in pPos:
        ps.append((float(pAlone[p + 1]), float(pAlone[p + 2]), float(pAlone[p + 3])))

    return True, stringBuild(name, degreeN, ps)
