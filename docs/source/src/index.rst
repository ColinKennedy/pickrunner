Pickrunner - The New Maya pickWalk Tool
=======================================

Maya's pickWalk tool is okay, but it doesn't work well for many common scenarios.
In particular, pickWalking is useless for rigs, because rig controllers are
rarely grouped so that a user can move between them easily.

For this reason and a few others, Pickrunner was created.

Pickrunner is very simple. You assign how to move between objects in your scene
once and then you can use your up/down/left/right keys to move between those
objects just like you normally would. If an object doesn't have any
Pickrunner data assigned to it, the tool will just use pickWalk, instead. That
way, even if Pickrunner is only partially implemented in a scene, it won't
interrupt the artist's process.


Installation
------------

Installing By Module
++++++++++++++++++++

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
+++++++++++++++++++

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


Scene Setup
-----------

If you installed Pickrunner through the "pickrunner.mod" file, you should
already have a new shelf called "Pickrunner" on-startup. Just click the
Pickrunner GUI button.

.. figure:: /../icons/pickrunner_icon.png

This button will load the Pickrunner GUI, which comes in two modes,
:ref:`assignmentmode` and :ref:`selectionmode`.

TODO: Make screenshot of the GUI in both modes


.. _assignmentmode :

Assignment Mode
+++++++++++++++

This is the default mode that you'll see when you open the Pickrunner GUI.
Assignment Mode is exactly as it sounds like. It's the mode that lets you set
up Pickrunner-object relationships.

While in Assignment Mode, you should see 4 direction buttons and a button
labelled "Load Selection".

Select an object, for example objectA, and then click "Load Selection". objectA
is now being editted by Pickrunner.

Select another object, for example objectB, and click any of the up, down, left,
or right buttons.

.. note ::
    If you've got "Auto-Pair" enabled, Pickrunner will reflect objects.
    So when you assign objectB as the "left" direction to objectA, "Auto-Pair"
    will also set objectA as the "right" direction to objectB.
    It's just a timesaver. Turn it off if you don't want it to do that.

Assuming you've done all of the connections you wanted, you're ready to start
using Pickrunner. If you have the direction hotkeys set up correctly, you
should be able to press up/down/left/right to move between objects or use
Pickrunner's "Selection Mode".


.. _selectionmode :

Selection Mode
++++++++++++++

This is a good mode to test your Pickrunner connections with. Select objects in
the scene that have Pickrunner data and press the direction keys. Your
selection should move from object to object.


Drawback To Pickrunner
----------------------

Pickrunner is implemented using node UUIDs, which means you can go from any
node to any node, even if the nodes are shading nodes (DG nodes).


The downside to using UUIDs though is that if you export your objects and
import them into another scene, Pickrunner won't work. Referencing your nodes
will still work though, and in practice that's usually good enough.


Developer Notes
---------------

.. toctree

    API Documentation <api>
