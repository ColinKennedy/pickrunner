#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A Maya implementation for Pickrunner.

The user, usually an animator or rigger, can use this GUI to assign
object-to-object relationships. Once those relationships are defined, they
can use the arrow-keys on their keyboard to move between those objects.

Functionally, this is exactly the same as Maya's built-in pickWalk command.
The difference here however is that pickWalk is notoriously useless because
it relies on Maya's DAG hierarchy, which doesn't always make navigation easy.

Pickrunner doesn't care about hierarchy. It can even be used for DG nodes.
Take that, pickWalk!

'''

# IMPORT STANDARD LIBRARIES
import json

# IMPORT THIRD-PARTY LIBRARIES
from Qt import QtCore
from maya import cmds
import pymel.core as pm

# IMPORT LOCAL LIBRARIES
from . import gui
from . import mui

WINDOW_TITLE = 'Pickrunner'


class MayaBehaviorControl(gui.BehaviorControl):

    '''A controller that implements Maya-specific functions to Pickrunner.'''

    reserved_attribute_name = '__mayarunner_info'

    def __init__(self):
        '''Initialize the object and do nothing else.'''
        super(MayaBehaviorControl, self).__init__()

    @classmethod
    def _create_hidden_metadata_attribute(cls, node):
        '''Get the hidden attribute that we store Pickrunner values onto.

        If the attribute doesn't exist, create it and hide it from the user
        so they can't mess with it easily.

        Args:
            node (<pm.general.PyNode>): The node to add the attribute onto.

        '''
        try:
            node.attr(cls.reserved_attribute_name)
        except pm.MayaAttributeError:
            node.addAttr(cls.reserved_attribute_name, dataType='string')

        attr = node.attr(cls.reserved_attribute_name)
        pm.setAttr(attr, keyable=False, channelBox=False)
        attr.setLocked(True)

    @classmethod
    def get_selection(cls):
        '''list[<pm.general.PyNode>]: The selected objects in the Maya scene.'''
        return pm.selected()

    @classmethod
    def get_settings(cls, node):
        '''dict[str]: Get the settings for the given node, if any.'''
        known_exceptions = (
            # If the node isn't a PyMEL node
            AttributeError,
            # If the Maya node doesn't have the reserved attribute
            pm.MayaAttributeError,

            # If the value retrieved from our reserved attribute isn't a string
            TypeError,

            # If the JSON string found has syntax errors or is empty
            ValueError,
        )

        try:
            value = json.loads(node.attr(cls.reserved_attribute_name).get())
        except known_exceptions:  # pylint: disable=E0712
            return dict()

        return value

    @classmethod
    def get_object_name(cls, obj):
        '''str: Find the unique-name of the given object.'''
        try:
            return obj.nodeName()
        except AttributeError:
            pass

        try:
            obj = pm.ls(obj)[0]
        except IndexError:
            return obj

        return obj.nodeName()

    @classmethod
    def assign(cls, from_object, direction, to_object, settings=None):
        '''Set an object to be remapped to another object, given some direction.

        Once an object is remapped to another object, we can use that to move
        Maya's selection around whenever the user asks to.

        Args:
            from_object:
                The object that will have the direction and to_object stored onto.
            direction:
                Some unique key to store onto from_object. This direction should
                always point towards to_object. (How direction points to
                to_object is up to the developer to implement).
            to_object:
                The object to remap to when direction and from_object are given
                to :func:`BehaviorControl.do_motion`.

        '''
        if not settings:
            settings = cls.get_settings(from_object)

        settings[direction] = get_uuid(to_object)

        # Dump settings onto the node
        cls._create_hidden_metadata_attribute(from_object)
        attr = from_object.attr(cls.reserved_attribute_name)
        is_locked = attr.isLocked()
        attr.setLocked(False)
        attr.set(json.dumps(settings))
        attr.setLocked(is_locked)

    @classmethod
    def do_motion(cls, direction, obj):
        '''Change selection to an associated node of obj, given some direction.

        Args:
            direction (str): The direction to move to.
            obj (<pm.general.PyNode>): The object to get the associated object from.

        '''
        uuid_of_the_node_to_select = cls.get_settings(obj).get(direction)

        try:
            node = pm.ls(uuid_of_the_node_to_select)[0]
        except IndexError:
            return

        pm.select(node)

        return node


class PickrunnerMayaWindow(gui.AssignmentManagerWidget):

    '''A GUI implementation of Pickrunner, for Maya.'''

    def __init__(self, parent=None):
        '''Create the window and its default widgets.

        Args:
            parent (:obj:`<QtCore.QObject>`, optional):
                Qt-based associated object. Default is None.

        '''
        super(PickrunnerMayaWindow, self).__init__(
            controller=MayaBehaviorControl(),
            parent=parent)

        # Whenever the user changes selection, try to update the GUI
        self.jobs = []

        selection_job_id = pm.scriptJob(
            event=['SelectionChanged', self.update_appearance])
        new_scene_job_id = pm.scriptJob(
            event=['deleteAll', self.update_appearance])
        self.jobs.append(selection_job_id)
        self.jobs.append(new_scene_job_id)

        selection = self.controller.get_selection()
        if selection:
            self.set_loaded_object(selection[0])

    def init_default_settings(self):
        '''Set the window size to be larger, by default.'''
        super(PickrunnerMayaWindow, self).init_default_settings()
        self.toggle_mode()  # Place into "Assignment Mode" by default
        self.resize(320, 100)

    def closeEvent(self, event):
        '''When the window is closed, stop trying to update the GUI.'''
        for job_id in self.jobs:
            pm.scriptJob(kill=job_id)

        super(PickrunnerMayaWindow, self).closeEvent(event)


def get_uuid(node):
    '''str: Get the UUID of the given node, if the node exists.'''
    try:
        node = node.nodeName()
    except AttributeError:
        pass

    try:
        return cmds.ls(node, uuid=True)[0]
    except IndexError:
        return ''


def do_pickrun_motion(direction):
    '''Try to pickrun in a given direction. Otherwise, pickWalk.

    Args:
        direction (str):
            The direction to walk. Options are: ("up", "down", "left", "right").

    '''
    try:
        node = pm.selected()[-1]
    except IndexError:
        pm.pickWalk(direction=direction)
        return

    new_node = MayaBehaviorControl.do_motion(direction, node)
    if not new_node:
        # Pickrun failed for some reason so lets pickWalk, instead
        pm.pickWalk(direction=direction)


@mui.delete_ui_if_exists(WINDOW_TITLE)
def show():
    '''Create and show the Pickrunner GUI for Maya.'''
    window = PickrunnerMayaWindow(mui.get_main_window())
    window.setWindowFlags(QtCore.Qt.Window)
    window.setWindowTitle(WINDOW_TITLE)
    window.setObjectName(WINDOW_TITLE)
    window.manager.main_widget.setFocus()
    window.show()
