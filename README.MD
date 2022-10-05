Tom Wood 2020 - Distributed under the MIT License

Small Plug-in that creates and stores UI's based on a list of custom UI layouts.

TO INSTALL:
1. Unpack zip file (SKIP IF NOT USING ZIP DISTRO)

2. COPY tMayaUIs_PLUG.py to MAYA_PLUG_IN_PATH:
	_MAYA_APP_DIR_/bin/plug-ins

3. COPY tMayaUIs_bin directory to a scripts directory:

	WINDOWS:
	Users/_CURRENT_USER_/Documents/maya/_MAYA_VERSION_/scripts

	MAC:
	Library/Preferences/Autodesk/maya/_MAYA_VERSION_/scripts
	
4. If not already installed, install pymel (the more "pythonic" port of maya.cmds by Luma Pictures)
	for Maya 2023: https://help.autodesk.com/view/MAYAUL/2023/ENU/?guid=GUID-2AA5EFCE-53B1-46A0-8E43-4CD0B2C72FB4

5.  Make Sure Maya is closed.
    -A: IF NO userSetup.py in Scripts directory (Folder from step 3) - copy userSetup.py from distro into that folder AND YOU'RE DONE
    -B: If userSetup.py already exists, copy text from userSetup.py provided from distro into that file and save.

Load the plug-in in maya and enjoy!
