"""
DEFINED NAMING CONVENTIONS - CHANGED FOR PROCEDURAL RIGGING PREFERENCES
"""

import pymel.core as pm


def camel(string):
    words = string.split(' ')
    if len(words) == 1:
        return string[0].lower() + string[1:]
    words[0] = words[0].lower()
    for x in range(1, len(words), 1):
        first = words[x][0].upper()
        words[x] = first + words[x][1:]
    camelStr = ''
    for w in words:
        camelStr = camelStr + w
    return camelStr


def shortName(string):
    shortNameStr = camel(string)

    chars = ['a', 'e', 'i', 'o', 'u', '', '_']

    for s in shortNameStr:

        if s in chars:
            shortNameStr = shortNameStr.replace(s, '')

    return shortNameStr


def rSpace(string):
    return string.replace(' ', '')


def pathCorrect(string):
    path = string.split('|')

    path[0] = u'MayaWindow'

    correctedPath = ''

    for path in path:
        correctedPath = correctedPath + '|' + path

    correctedPath = correctedPath[1:]

    return correctedPath


def names(chain):
    acceptedStrings = ['arm', 'arm2', 'leg', 'leg2', 'foot', 'hand', 'head']

    if chain not in acceptedStrings:
        print('Needs Correct Input: Options are: arm, arm2, leg, leg2, foot, hand, head')
        return

    elif chain == 'arm':
        return ['shoulder', 'elbow', 'hand']

    elif chain == 'arm2':
        return ['shoulder', 'elbowA', 'elbowB', 'hand']

    elif chain == 'leg':
        return ['hip', 'knee', 'ankle', 'ball', 'toe', 'toe']

    elif chain == 'leg2':
        return ['hip', 'kneeA', 'kneeB', 'ankle', 'ball', 'toe', 'toe']

    elif chain == 'foot':
        return ['foot', 'heel', 'toe', 'ball']

    elif chain == 'hand':
        return ['thumb', 'index', 'middle', 'ring', 'pinky']

    elif chain == 'head':
        return ['neck', 'neckEnd', 'head', 'head']


def alphabet():
    """
    Alphabet with 52 members for counting and name additions.
    :return: List of length 52
    """
    return ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
            'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Aa',
            'Bb', 'Cc', 'Dd', 'Ee', 'Ff', 'Gg', 'Hh', 'Ii',
            'Ll', 'Mm', 'Nn', 'Oo', 'Pp', 'Qq', 'Rr', 'Ss',
            'Tt', 'Uu', 'Vv', 'Ww', 'Xx', 'Yy', 'Zz']


def empty():
    return ['', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '']


def countInt():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
            31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
            41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
            51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
            61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
            71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
            81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
            91, 92, 93, 94, 95, 96, 97, 98, 99, 100]


def countString():
    return ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
            '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
            '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
            '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
            '51', '52', '53', '54', '55', '56', '57', '58', '59', '60',
            '61', '62', '63', '64', '65', '66', '67', '68', '69', '70',
            '71', '72', '73', '74', '75', '76', '77', '78', '79', '80',
            '81', '82', '83', '84', '85', '86', '87', '88', '89', '90',
            '91', '92', '93', '94', '95', '96', '97', '98', '99', '100']


# Defines prefix
def prefix(type):
    prefixes = {

        # BASIC OBJS
        'mesh': 'geo',
        'nurbsCurve': 'crv',
        'transform': 'grp',
        'joint': 'jnt',
        'locator': 'loc',

        # SPECIAL JOINTS
        'boundJoint': 'bn',
        'endJoint': 'be',
        'jointDriver': 'jDrv',
        'jointControl': 'jCtrl',

        # CONTROLLER
        'controller': 'ctrl',

        # IKS
        'ikRPsolver': 'ikRp',
        'ikSplineSolver': 'ikSp',
        'ikSCsolver': 'ikSc',
        'ikEffector': 'eff',

        # DEFORMERS
        'clusterHandle': 'dfmr',

        # CONSTRAINTS
        'pointConstraint': 'link',
        'parentConstraint': 'link',
        'orientConstraint': 'link',
        'aimConstraint': 'link',
        'scaleConstraint': 'link',

        # SPECIAL TRANSFORM OBJECTS
        'locOffset': 'locOff',
        'groupOffset': 'grpOffset',
        'locMatch': 'locMatch',
        'groupMatch': 'grpMatch',

        # UTILITY NODES
        'utilityNode': 'util',
        'arrayMapper': 'util',
        'bump2d': 'util',
        'bump3d': 'util',
        'condition': 'util',
        'distanceBetween': 'util',
        'heightField': 'util',
        'lightInfo': 'util',
        'multiplyDivide': 'util',
        'place2dTexture': 'util',
        'place3dTexture': 'util',
        'plusMinusAverage': 'util',
        'projection': 'util',
        'reverse': 'util',
        'samplerInfo': 'util',
        'setRange': 'util',
        'stencil': 'util',
        'uvChooser': 'util',
        'vectorProduct': 'util'
    }

    return prefixes.get(type)


# Special Additional Part Names for required nodes.
def specialPartNames():
    # Utilities
    specialPart = {

        # IKs
        'ikRPsolver': 'ikRotP',
        'ikSplineSolver': 'ikSpline',
        'ikSCsolver': 'ikSingChan',
        'ikEffector': 'iKEff',
        'ikHandle': 'ikHandle',

        # Utilities
        'arrayMapper': 'arrayMapper',
        'bump2d': 'bmp2D',
        'bump3d': 'bmp3D',
        'condition': 'condition',
        'distanceBetween': 'distBet',
        'heightField': 'heightField',
        'lightInfo': 'lgtInfo',
        'multiplyDivide': 'multDiv',
        'place2dTexture': 'pl2DText',
        'place3dTexture': 'pl3DText',
        'plusMinusAverage': 'plusMinusAvg',
        'projection': 'proj',
        'reverse': 'rev',
        'samplerInfo': 'sampInf',
        'setRange': 'setRange',
        'stencil': 'stencil',
        'uvChooser': 'uvChoser',
        'vectorProduct': 'vctProd',

        # Constraints
        'pointConstraint': 'ptConstraint',
        'parentConstraint': 'prntConstraint',
        'orientConstraint': 'oriConstraint',
        'aimConstraint': 'aimConstraint',
        'scaleConstraint': 'sclConstraint',

        # DEFORMERS
        'clusterHandle': 'cluster',

    }
    return specialPart


# Dictoinary of which parts would be associated with which limb.
def partsDict():
    bodyPart = {
        'arm': ['shoulder', 'elbow', 'hand', 'arm', 'wrist', 'clavicle', 'armPole', 'fkWrist'],
        'hand': ['thumb', 'index', 'middle', 'ring', 'pinky'],
        'leg': ['hip', 'knee', 'ankle', 'foot', 'leg', 'legPole'],
        'head': ['head', 'neck', 'neckEnd', 'headEnd'],
        'spine': ['sp'],
        'foot': ['toe', 'heel', 'ball'],
        'core': ['chest', 'hip', 'hips', 'cog']
    }
    return bodyPart


def partHierarchy():
    return [
        ('all', ''), ('core', ''), ('spine', ''), ('head', ''), ('arm', ''), ('leg', ''), ('hand', 'arm'),
        ('foot', 'leg')
    ]


def constraints():
    return [
        'pointConstraint',
        'parentConstraint',
        'orientConstraint',
        'aimConstraint',
        'scaleConstraint'
    ]


def acceptedTypes():
    accepted = ['ikHandle',
                'ikEffector',
                'pointConstraint',
                'parentConstraint',
                'scaleConstraint',
                'aimConstraint',
                'orientConstraint']

    return accepted


def sidedict():
    sides = {
        'left': 'l',
        'right': 'r',
        'centre': 'c',
        'middle': 'c',
        'up': 'u',
        'down': 'd',
    }

    return sides


def basicAttrs():
    return [
        'translateX',
        'translateY',
        'translateZ',
        'rotateX',
        'rotateY',
        'rotateZ',
        'scaleX',
        'scaleY',
        'scaleZ',
        'visibility'
    ]


def fieldTypeByData():
    return {
        'bool': pm.checkBox,
        'double': pm.floatField
    }


def fieldTypeByField():
    return {
        'floatField': pm.floatField,
        'checkBox': pm.checkBox,
    }
