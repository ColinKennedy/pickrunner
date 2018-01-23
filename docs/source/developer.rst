API Documentation
=================

Setting Up For Development
--------------------------

Make sure to grab the requirements.txt file before trying to build the docs

.. code-block :: bash

    pip -r docs/requirements.txt

There are some modules used by Pickrunner that are not mentioned in the
requirements.txt file. Namely shiboken, pymel, and maya.cmds. All of these are
provided by Maya so we just ignore them for building documentation.


Building The Documentation
--------------------------

Here are the steps to rebuild this documentation:

1. Make sure that the scripts folder is visible in the :obj:`PYTHONPATH`.
2. Run :obj:`make html` while cd'ed into the :obj:`docs` folder,
   or make.bat if you're on Windows
3. Alternatively, run :obj:`sphinx-build -b html docs/source docs/build`
4. If new Python modules are added, make sure to rebuild their pages, using
   :obj:`docs/regenerate.sh` or :obj:`docs/regenerate.bat` if you're on Windows.


Python Documentation
--------------------

Most (all?) of the documentation is just for the Pickrunner GUI so mileage will
vary. The main class of-interest are :class:`pickrunner.gui.BehaviorControl`.
For an example of how it's implemented, check out
:class:`pickrunner.mayarunner.MayaBehaviorControl`.


pickrunner\.gui module
++++++++++++++++++++++

.. automodule:: pickrunner.gui
    :members:
    :undoc-members:
    :show-inheritance:

pickrunner\.mayarunner module
+++++++++++++++++++++++++++++

.. automodule:: pickrunner.mayarunner
    :members:
    :undoc-members:
    :show-inheritance:

pickrunner\.mui module
++++++++++++++++++++++

.. automodule:: pickrunner.mui
    :members:
    :undoc-members:
    :show-inheritance:

pickrunner\.visibility\_widget module
+++++++++++++++++++++++++++++++++++++

.. automodule:: pickrunner.visibility_widget
    :members:
    :undoc-members:
    :show-inheritance:


Module contents
+++++++++++++++

.. automodule:: pickrunner
    :members:
    :undoc-members:
    :show-inheritance:
