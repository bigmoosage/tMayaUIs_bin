"""Return names string list for renaming"""


# Returns list of names held based on input of chain: Accepted types: arm, arm2, leg, leg2, foot, hand, head
def names(chain):

    acceptedStrings = ['arm', 'arm2', 'leg', 'leg2', 'foot', 'hand', 'head']

    if chain not in acceptedStrings:
        print ('Needs Correct Input: Options are: arm, arm2, leg, leg2, foot, hand, head')
        return

    elif chain == 'arm':
        return ['shoulder', 'elbow', 'hand']

    elif chain == 'arm2':
        return ['shoulder', 'elbowA', 'elbowB', 'hand']

    elif chain == 'leg':
        return ['hip', 'knee', 'ankle', 'ball', 'toe', 'toeEnd']

    elif chain == 'leg2':
        return ['hip', 'kneeA', 'kneeB', 'ankle', 'ball', 'toe', 'toeEnd']

    elif chain == 'foot':
        return ['foot', 'heel', 'toe', 'ball']

    elif chain == 'hand':
        return ['thumb', 'index', 'middle', 'ring', 'pinky']

    elif chain == 'head':
        return ['neck', 'neckEnd', 'head', 'headEnd']
