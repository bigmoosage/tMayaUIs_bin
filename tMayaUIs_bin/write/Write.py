"""
Simple create python file script.
"""


# Built-in imports
import os


class WriteFile:

    def __init__(self,
                 work=True,
                 new=True,
                 name='file',
                 module=None,
                 path=None,
                 inputstring=None
                 ):

        if work is False:
            print('DID NOT WRITE')
            return

        if new is True:
            operation = 'w+'
        elif new is False:
            operation = 'a'
            inputstring = '\n' + inputstring
        else:
            raise AttributeError("\"new\" Arg must be a BOOL")

        path = str(os.path.split(os.path.abspath(__file__))[0]) + '\\' + module + '\\' + name + '.py'
        print(path)

        with open(path, operation) as appended:
            appended.write(inputstring)
