"""
Name Changers for formatting.
"""

# Import statements
import pymel.core as pm

from tMayaUIs_bin.manip import dt_namingConvention as nc

# My modules.
from tMayaUIs_bin.manip import dt_objnaming


class Rename:

    def __init__(self,
                 selection=None,
                 prefix=None,
                 side=None,
                 specialpart=False,
                 part=None,
                 partslist=None,
                 letter=None,
                 endchain=False,
                 suffix=True,
                 separator=True,
                 perobject=False,
                 withconnections=False,
                 rename=True
                 ):

        # Definition for warning
        def warning(warningstring):
            pm.warning(warningstring)

        separator1 = separator2 = separator3 = separator
        self.oN = ''

        # IF NO CHANGES TO DEFAULTS
        if selection is None \
                and prefix is None \
                and side is None \
                and specialpart is None \
                and part is None \
                and partslist is None \
                and letter is None \
                and endchain == False \
                and suffix == True \
                and separator == True \
                and perobject == False \
                and rename == True:
            # Outputs Default name if no arguments given to Class.
            prefix = 'pre'
            side = 'side'
            part = 'part'
            letter = True
            suffix = nc.countString()

        # Queries selected objects if no other list given
        if selection is None:
            selection = pm.ls(sl=True, fl=True)

        # Queries if selection
        if len(selection) == 0:
            self.n = ['Select Some Objects', 'Please']
            return

        # loop length
        loop = len(selection)

        # Question prefix
        if prefix == 'bound':
            prefix = 'bn'
        elif prefix == 'driver':
            prefix = 'jDrv'
        elif perobject == True:
            pass

        # Question side
        if side == 'left':
            side = 'l'
        elif side == 'right':
            side = 'r'
        elif side == 'middle':
            side = 'c'

        # # Special Part
        # if specialpart is None:
        #     specialpart = ''

        # Basic part
        if part is None:
            part = ''

        # partslist queries
        if partslist is not None:
            if len(partslist) < len(selection):
                loop = len(partslist)

                moreNames = len(selection) - len(partslist)
                if moreNames > 1:
                    n = 'Names.'
                else:
                    n = 'Name.'
                self.oN = '\nNeeds ' + str(moreNames) + ' more ' + n

                if rename == 1:
                    warning('Less given names than Selected Objects')
            elif len(partslist) > len(selection):
                moreObjs = len(partslist) - len(selection)
                if moreObjs > 1:
                    n = 'Selections.'
                else:
                    n = 'Selection.'
                self.oN = '\nNeeds ' + str(moreObjs) + ' ' + n

                if rename == 1:
                    warning('Less Selected Objects than given names')

        # Question letter
        if letter == 1:
            letter = nc.alphabet()
        if letter == 1 and perobject == True:
            letter = nc.alphabet()[0]

        # Number string:
        if letter == 0 or (letter == 0 and part is not None):
            suffix = nc.countString()
        else:
            suffix = '01'
        if partslist is not None:
            suffix = '01'

        # Separator Vars definition
        if separator == False:
            separator1 = ''
            separator2 = ''
            separator3 = ''

        elif separator == True:
            separator1 = '_'
            separator2 = '_'
            separator3 = '_'
            if prefix is None or side is None:
                separator1 = ''
            if specialpart is None:
                separator2 = ''
            if prefix is None and side is None and specialpart is None:
                separator3 = ''
            if part is not None and perobject == 1:
                separator3 = '_'

        end = ''

        nameList = []  # Defines variable to hold list of names.

        for x in range(loop):

            # Perobject and prefix being true - Changes prefix to object specific prefix.
            if perobject == True:
                # print(pm.objectType(selection[x]))
                prefix = nc.prefix(dt_objnaming.findobjectype(selection[x]))
                # print(prefix) # Prefix specific to object per perobject flag

            # If object has a special part.
            if specialpart == True and dt_objnaming.findobjectype(selection[x]) in nc.specialPartNames().keys():
                specialpart = nc.specialPartNames().get(dt_objnaming.findobjectype(selection[x]))
                # Special part name for object per perobject flag
            else:
                separator2 = ''

            if withconnections == True:
                part = dt_objnaming.findconnectionsname(selection[x])
                side = nc.sidedict().get(dt_objnaming.SpecialNames(selection[x]).side)
                suffix = '01'

            if endchain == True and x == loop - 1 and prefix == 'bn':
                prefix = 'be'
                end = 'End'
                letter = None

            nameConstruct = [prefix,
                             separator1,
                             side,
                             separator2,
                             specialpart,
                             separator3,
                             part,
                             partslist,
                             end,
                             letter,
                             suffix]

            individualName = ''

            for elem in nameConstruct:

                if (elem != '' and elem is not None and type(elem) is not bool) and type(elem) is not list:
                    individualName = individualName + elem

                elif (elem != '' and elem is not None and type(elem) is not bool) and type(elem) is list:
                    individualName = individualName + elem[x]

            nameList.append(individualName)

        # Returns objects in selection
        self.objs = selection
        # Returns nameList produced by class
        self.n = nameList

        # Actual renaming of objects
        if rename == 1:

            # Removes errors from reloading object in Hypershade Property Panel by deleting panel.
            for form in pm.lsUI(type='formLayout'):
                if form.find('property') != -1 and len(form.split('|')) == 2:
                    pm.deleteUI(form)

            # Temporary namespace definition
            pm.namespace(add='rnmWinCorrect')

            # Renames objects in temporary namespace
            for x in range(loop):
                pm.rename(selection[x], 'rnmWinCorrect:' + nameList[x])

            # Tries to move renamed objects into root namespace
            try:
                pm.namespace(mv=('rnmWinCorrect', ':'))

            # Excepts if there is a namespace clash, forces change and gives specific warning
            except RuntimeError:
                pm.namespace(mv=('rnmWinCorrect', ':'), force=True)

                # Clashing objects definition
                clashes = []

                # Asks if nameList are already in scene and not in the selection
                for n in nameList:
                    if n not in selection:
                        clashes.append(n)

                # Warns about clash for clashing objects
                warning("NameSpace Clash - Renaming has been forced: Check for Objs:  " + ', '.join(clashes))

            # Set namespace back to root
            pm.namespace(set=':')

            # Removes temporary namespace
            pm.namespace(rm='rnmWinCorrect')
