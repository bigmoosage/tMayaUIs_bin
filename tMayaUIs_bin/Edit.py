#!/usr/bin/env python
# -*-coding:utf-8-*-

"""
Wrapper for format editing of python files.
"""

# Python Mods
import os


class Editor:
    # Use pathto='Z:\\...' directory and filename='foo' any string, tries to resolve typos.
    # Or Use abspath=completepathtofile. e.g. 'Z:\\foo\\foo.py'
    def __init__(self,
                 pathto=None,
                 filename=None,
                 abspath=None
                 ):

        self.Original = ''
        self.Docstring = ''
        self.Imports = ''
        self.Functions = {}

        # Finds the filename within directories under pathto.
        if abspath is None and pathto is not None and filename is not None:
            listOccurances = []
            for root, directories, filenames in os.walk(os.path.abspath(pathto)):
                for walkfile in filenames:
                    # print(walkfile)
                    # If filename is in directory.
                    if walkfile.find(filename) != -1 and walkfile[-1] != 'c':
                        print('FOUND: ' + os.path.join(root, walkfile))
                        listOccurances.append(os.path.join(root, walkfile))

            # If there is only one file of given name.
            if len(listOccurances) == 1:
                self.editfile = listOccurances[0]
            # If there is no file with given name.
            elif len(listOccurances) == 0:
                print ('%s doesn\'t exist.' % filename)
                self.editfile = None
                return
            # If there are multiple files of same name within pathto.
            else:
                print ('Multiple instances of given filename: %s - Use Editor(abspath=path) to resolve.' % filename)
                self.editfile = None
                return
        # If abspath is used.
        elif abspath is not None:
            try:
                fileopenTry = open(abspath, 'r')
            except IOError:
                print('FILE DOESN\'T EXIST - Check abspath')
                return
            fileopenTry.close()
            self.editfile = abspath
        else:
            print('Incorrect inputs supplied - Needs pathto=path and filename=file or abspath=path')

        # Stores original text of file for Undo operation.
        with open(self.editfile, 'r') as originalfind:
            self.Original = originalfind.read()

        # Stores Docstring.
        with open(self.editfile, 'r') as docstringfind:
            cnt = 0
            lines = docstringfind.read().split('\n')
            docstringpos = []
            for x in range(len(lines)):
                if lines[x].find('"""') == 0:
                    docstringpos.append(x)
                    cnt += 1
            self.Docstring = '\n'.join(lines[docstringpos[0]:docstringpos[1] + 1]) + '\n\n'

        # Stores and Formats Imports.
        with open(self.editfile, 'r') as importsfind:
            cnt = 0
            lines = importsfind.read().split('\n')
            for x in range(len(lines)):
                if lines[x].find('import') == 0 or lines[x].find('from') == 0:
                    if lines[x - 1] == '':
                        self.Imports += '\n# Imports\n'
                    elif lines[x - 1].find('#') == 0:
                        self.Imports += '\n' + lines[x - 1] + '\n'
                        if lines[x - 2].find('#') == 0:
                            self.Imports += lines[x - 2] + '\n'
                    self.Imports += lines[x] + '\n'

        # Stores and Formats Methods
        with open(self.editfile, 'r') as methodsfind:
            lines = methodsfind.read().split('\n')

            cnt = 0
            defStart = []
            for x in range(0, len(lines), 1):

                if lines[x].find('def ') == 0:

                    if lines[x - 2].find('#') == 0:
                        defStart.append([x - 2])
                    elif lines[x - 1].find('#') == 0:
                        defStart.append([x - 1])
                    else:
                        defStart.append([x])

                cnt += 1

            cnt = 1
            for d in defStart:

                if cnt <= len(defStart) - 1:
                    d.append(defStart[cnt][0] - 1)

                else:
                    d.append(len(lines))
                cnt += 1

            for defs in defStart:

                if lines[defs[0]].find('#') == 0 and lines[defs[0] + 1].find('#') == 0:
                    key = lines[defs[0] + 2].split('(')[0][4:]

                elif lines[defs[0]].find('#') == 0:
                    key = lines[defs[0] + 1].split('(')[0][4:]

                else:
                    key = lines[defs[0]].split('(')[0][4:]

                self.Functions[key] = defs

    # Undos any operation done to inputted file - writes file to value taken in at first run.
    def undo(self):
        with open(self.editfile, 'w') as undofile:
            undofile.write(self.Original)

    # def format(self):

    # Alphabetises definitions within a file for easier reading.
    def alphabetise(self):

        with open(self.editfile, 'r') as fileedit:
            lines = fileedit.read().split('\n')

            alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                        'h', 'i', 'j', 'k', 'l', 'm', 'n',
                        'o', 'p', 'q', 'r', 's', 't', 'u',
                        'v', 'w', 'x', 'y', 'z']

            methodsstring = ''

            for a1 in alphabet:
                for a2 in alphabet:
                    for a3 in alphabet:
                        for defs, vals in self.Functions.items():
                            if lines[vals[0]].find('#') != 0:
                                addComment = '\n\n# %s method.\n' % defs
                            else:
                                addComment = '\n\n'
                            if len(defs) == 1 and a2 == alphabet[0] and a3 == alphabet[0]:
                                if defs.lower()[0] == a1:
                                    methodsstring += addComment + '\n'.join(
                                        lines[self.Functions[defs][0]:self.Functions[defs][1]]) + ''

                            elif len(defs) == 2 and a3 == alphabet[0]:
                                if defs[0].lower() == a1 and defs[1].lower() == a2:
                                    methodsstring += addComment + '\n'.join(
                                        lines[self.Functions[defs][0]:self.Functions[defs][1]]) + ''

                            elif len(defs) > 2:
                                if defs.lower()[0] == a1 \
                                        and defs.lower()[1] == a2 \
                                        and defs.lower()[2] == a3:
                                    methodsstring += addComment + '\n'.join(
                                        lines[self.Functions[defs][0]:self.Functions[defs][1]]) + ''

        with open(self.editfile, 'w+') as filewrite:
            filewrite.write(self.Docstring + self.Imports + methodsstring)

    # Find specific
    def findAndRemove(self, sname='', stofind='def'):

        with open(self.editfile, 'r') as fileedit:
            lines = fileedit.read().split('\n')
