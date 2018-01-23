Installation
============

Installing By Module
--------------------

Download the pickrunner project from online.

..

    git clone https://github.com/ColinKennedy/pickrunner.git


Pickrunner comes with a module file located in the "modules" folder called
"pickrunner.mod". Just add the full path to the "modules" folder to the
MAYA_MODULE_PATH environment variable and restart Maya.

Pickrunner will build a brand new shelf for you to use its GUI.

The paths listed in "pickrunner.mod" are all relative to the main folder so, if
you need to place the "pickrunner.mod" file someplace else, just make sure to
replace the relative path "..\" and "../" to wherever you place the other
files.

Installing Manually
-------------------

If you don't want to use the module file, no problem. Just do this:

1. Put the "pickrunner" folder located in "scripts/pickrunner" someplace on the
   MAYA_SCRIPT_PATH
   - This makes it so that the Pickrunner GUI will load
2. Add the directory to the "userSetup.py" file onto your MAYA_SCRIPT_PATH
   - This step will override your hotkeys on Maya's startup
3. Place the "pickrunner_icon.png" in the XBMLANGPATH environment variable
   - Only do this if you want to use the Pickrunner icon(s)
4. Add these commands to a new shelf button

..

    from pickrunner import mayarunner
    mayarunner.show()

And you're done.

