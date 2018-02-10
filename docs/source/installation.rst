Installation
============

Installing By Module
--------------------

Download the pickrunner project from online.

.. code-block :: bash

    git clone https://github.com/ColinKennedy/pickrunner.git


Pickrunner comes with a .mod file located "modules/pickrunner.mod".
Just add the full path to the `modules` folder to the
:obj:`MAYA_MODULE_PATH` environment variable.

In Windows DOS

::

    set MAYA_MODULE_PATH=C:\Path\to\pickrunner\modules:%MAYA_MODULE_PATH%

In bash

::

    export MAYA_MODULE_PATH=/Path/to/pickrunner/modules:$MAYA_MODULE_PATH

In tcsh/csh

::

    setenv MAYA_MODULE_PATH /Path/to/pickrunner/modules:$MAYA_MODULE_PATH

Now restart Maya and Pickrunner will have installed a brand new shelf with the GUI tool.


.. note ::

    All of the paths listed in pickrunner.mod are relative to the main
    project folder. So if you need to move pickrunner.mod someplace else,
    make sure to replace the `..\\` and `../` parts with the absolute path to
    wherever you placed the pickrunner project folder.


Installing Manually
-------------------

If you're not a fan of adding a whole extra shelf just for a single button, I
don't blame you. Pickrunner's installation can be customized but the process
is more manual than just setting the module file.


1. Add the "scripts" folder onto your :obj:`PYTHONPATH` environment variable.

   - Doing this steup will make Pickrunner's GUI load. otherwise,
     you'll get an ImportError if you try to run the Pickrunner shelf
     button.

2. Add the directory to Pickrunner's "userSetup.py" file onto your
   :obj:`PYTHONPATH`.

   - This step will override your hotkeys on Maya's startup so that you can
     use Pickrunner without the GUI.

3. Add the path to the "pickrunner_icon.png" in the :obj:`XBMLANGPATH` environment variable.

   - Only do this if you want to use the Pickrunner icon / shelf button.
     Note, you'll need to add "%B" to the end of the directory of "pickrunner_icon.png". See `Autodesk's documentation on the XBMLANGPATH environment variable <https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2015/ENU/Maya/files/GUID-228CCA33-4AFE-4380-8C3D-18D23F7EAC72-htm.html>`_ for details.

4. Make a new shelf button and add these Python commands onto it.

::

    from pickrunner import mayarunner
    mayarunner.show()

4b. If you want, use the pickrunner_icon.png file for your new shelf button.


And that's it, you're done.


Examples
--------


Module Example (Windows)
++++++++++++++++++++++++


::

    set MAYA_MODULE_PATH=C:\Users\korinkite\Dropbox\Private\my_ENV\env_ROOT\python\packages\pickrunner\modules


Manual Example (Windows)
++++++++++++++++++++++++


::

    set XBMLANGPATH=C:\Users\korinkite\Dropbox\Private\my_ENV\env_ROOT\python\packages\pickrunner\icons\%B
    set PYTHONPATH=C:\Users\korinkite\Dropbox\Private\my_ENV\env_ROOT\python\packages\pickrunner\scripts;%PYTHONPATH%
    set PYTHONPATH=C:\Users\korinkite\Dropbox\Private\my_ENV\env_ROOT\python\packages\pickrunner\integration;%PYTHONPATH%
