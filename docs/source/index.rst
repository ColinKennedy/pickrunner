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


.. toctree::

    Installation <installation>


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


Final Notes
-----------

If you're looking to contribute or would like the source, please check out
this page, first.

.. toctree::
    :maxdepth: 2
    :caption: Developer Guide

    Documentation And API Reference <developer>

