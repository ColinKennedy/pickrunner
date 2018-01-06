#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The Pickrunner base interface.

This module contains an abstract controller that is used to implement different
DCC environments, such as Maya, and a GUI that the controller can be used for.

'''


# TODO : Replace palettes with properties and stylesheets
# IMPORT STANDARD LIBRARIES
import textwrap
import abc

# IMPORT THIRD-PARTY LIBRARIES
from qt.widgets import visibility_widget
from Qt import QtWidgets
from Qt import QtGui
import six


class DirectionPad(QtWidgets.QWidget):

    '''A widget that shows buttons in a grid for up/down/left/right.

    Like the name implies, this widget lays out its default directions like a "+"
    sign, with "main_widget" in the middle.

    By default this widget doesn't do anything. It's meant to be added to other
    widgets and have functions connected to its buttons.

    '''

    def __init__(self, parent=None):
        '''Create the default children for this widget.

        Args:
            parent (:obj:`<QtCore.QObject>`, optional):
                Qt-based associated object. Default is None.

        '''
        super(DirectionPad, self).__init__(parent=parent)
        self.directions = dict()

        self.setLayout(QtWidgets.QVBoxLayout())
        self.main_widget = QtWidgets.QPushButton('Load selection')
        self.direction_layout = QtWidgets.QGridLayout()

        left = QtWidgets.QPushButton('Left')
        right = QtWidgets.QPushButton('Right')
        up = QtWidgets.QPushButton('Up')
        down = QtWidgets.QPushButton('Down')

        widgets = [
            ('center', self.main_widget),
            ('left', left),
            ('right', right),
            ('up', up),
            ('down', down),
        ]

        for storage_name, widget in widgets:
            self.directions[storage_name] = widget
            widget.setObjectName(storage_name)

        self.direction_layout.addWidget(up, 0, 1)
        self.direction_layout.addWidget(left, 1, 0)
        self.direction_layout.addWidget(self.main_widget, 1, 1)
        self.direction_layout.addWidget(right, 1, 2)
        self.direction_layout.addWidget(down, 2, 1)

        self.layout().addLayout(self.direction_layout)

        self.main_widget.setObjectName('load_selection_widget')


class BehaviorControl(object):

    '''An abstract controller that must be implemented in subclasses.

    This controller is used to interface with Pickrunner.

    '''

    def __init__(self):
        '''Initialize the object and do nothing else.'''
        super(BehaviorControl, self).__init__()

    @classmethod
    @abc.abstractmethod
    def get_selection(cls):
        '''list: The selected objects in the Maya scene.'''
        return []

    @classmethod
    @abc.abstractmethod
    def get_settings(cls, obj):
        '''dict: Any information stored in the given object that can be used.'''
        return dict()

    @classmethod
    @abc.abstractmethod
    def get_object_name(cls, obj):
        '''str: Find the unique-name of the given object.'''
        return ''

    @classmethod
    @abc.abstractmethod
    def assign(cls, from_object, direction, to_object, settings=None):
        '''Set an object to be remapped to another object, given some direction.

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
        pass

    @classmethod
    @abc.abstractmethod
    def do_motion(cls, direction, obj):
        '''Move the object to a given direction.

        How exactly it should "move" must be implemented in subclasses.
        For example, in Maya, this method will select a node that is associated
        with the given node-direction pair.

        Args:
            direction: The direction to move to.
            obj: The object to move from.

        '''
        pass


class AssignmentManagerWidget(QtWidgets.QWidget):

    '''A Qt widget used to pair objects together.

    For example, in Maya, this widget is used as a GUI to implement
    a special-pickwalk function.

    '''

    object_loaded_color = QtGui.QColor(0, 255, 0)
    nothing_loaded_color = QtGui.QColor(255, 255, 0)
    selection_mode_label = 'Selection Mode'
    assignment_mode_label = 'Assignment Mode'
    mode_options = (selection_mode_label, assignment_mode_label)

    def __init__(self, controller, parent=None):
        '''Create the base window and its child widgets.

        By default, when the GUI loads, it is set to selection mode.

        Args:
            controller (BehaviorControl):
                A environment controller. Basically, any function that is unique
                to a particular DCC like "get_selection", "set_info" is put here.
            parent (:obj:`<QtCore.QObject>`, optional):
                Qt-based associated object. Default is None.

        '''
        super(AssignmentManagerWidget, self).__init__(parent=parent)
        self.loaded_object = None
        self.controller = controller
        self._current_mode = self.selection_mode_label

        self.setLayout(QtWidgets.QVBoxLayout())

        self.mode_button = QtWidgets.QPushButton(self.selection_mode_label)
        self.loaded_object_widget = QtWidgets.QLineEdit()

        self.manager = DirectionPad()
        self.assignment_info_widget = visibility_widget.ExpandCollapseWidget('Assignment Info')

        self.layout().addWidget(self.mode_button)
        self.layout().addStretch(1)
        self.load_widget = QtWidgets.QWidget()
        self.load_widget.setLayout(QtWidgets.QHBoxLayout())
        self.load_widget.layout().addWidget(QtWidgets.QLabel('Loaded object:'))
        self.load_widget.layout().addWidget(self.loaded_object_widget)
        self.layout().addWidget(self.load_widget)
        self.layout().addWidget(self.manager)
        self.layout().addWidget(self.assignment_info_widget)

        self.init_default_settings()
        self.init_interactive_settings()

    def init_default_settings(self):
        '''Update this widget to make sure its default display matches its input.

        Also set toolTips, objectNames, and other information of widgets.

        '''
        # Modify the info widget to be a grid so that, when we add objects onto
        # it, the columns will stay aligned
        #
        self.assignment_info_widget.expand_widget.setLayout(QtWidgets.QGridLayout())

        self.loaded_object_widget.setReadOnly(True)
        self.update_appearance()

        self.mode_button.setToolTip(textwrap.dedent(
            '''
            Click to change Pickrunner's modes

            Assignment mode lets you edit object-direction relationships like
            clicking left on "objectA" will move to "objectB".

            Selection mode will actually change your selection from "objectA"
            to "objectB" when you click the left button, assuming you've created
            this relationship in advance.

            '''))
        self.mode_button.setObjectName('mode_button')
        self.manager.setObjectName('manager_widget')
        self.assignment_info_widget.setObjectName('info_widget')

    def init_interactive_settings(self):
        '''Create all of the button load/selection functionality of this GUI.'''
        def load_selection():
            '''Load the selection into our GUI and update its appearance.'''
            try:
                obj = self.controller.get_selection()[-1]
            except IndexError:
                return

            self.set_loaded_object(obj)

        self.manager.main_widget.clicked.connect(load_selection)
        self.mode_button.clicked.connect(self.toggle_mode)

        for widget in six.itervalues(self.manager.directions):
            widget.clicked.connect(self.do_action)

    def _add_info_line_widget(self, label, obj):
        '''Create a widget that will display the direction and object info.'''
        obj_widget = QtWidgets.QLineEdit()
        obj_widget.setText(self.controller.get_object_name(obj))
        obj_widget.setReadOnly(True)

        layout = self.assignment_info_widget.expand_widget.layout()
        row = layout.rowCount()
        layout.addWidget(QtWidgets.QLabel(label), row, 0)
        layout.addWidget(obj_widget, row, 1)

    def has_loaded_object(self):
        '''bool: If this widget has an associated object.'''
        return self.loaded_object is not None

    def set_loaded_object(self, obj):
        self.loaded_object = obj
        self.update_appearance()

    def set_mode(self, mode):
        '''Set the current mode of this GUI to the given mode.

        Raises:
            ValueError:
                If the given mode wasn't one of the expected modes.
                This method expects a mode that's defined in "mode_options".

        '''
        if mode not in self.mode_options:
            raise ValueError('Mode: "{mode}" was invalid. Options were, "{opt}".'
                             ''.format(mode=mode, opt=self.mode_options))

        self._current_mode = mode
        self.update_appearance()

    def clear_info_widgets(self):
        expand_layout = self.assignment_info_widget.expand_widget.layout()

        # TODO : Fix
        # for index in reversed(six.moves.range(expand_layout.count())):
        #     try:
        #         expand_layout.itemAt(index).widget().deleteLater()
        #     except AttributeError:
        #         pass

    def do_action(self):
        '''Do the associated action for the button that called this method.

        Note:
            This method relies on the objectName of the widget that calls it.
            The objectName is used by the controller to modify the loaded object.

        Raises:
            RuntimeError: If this method was not called from a Qt widget.

        '''
        if not self.has_loaded_object():
            return

        self.sender()
        try:
            direction = self.sender().objectName()
        except AttributeError:
            raise RuntimeError('do_action must be called from a Qt-signal')

        if self._current_mode == self.selection_mode_label:
            self.controller.do_motion(direction, self.loaded_object)
            return

        # Add the selected object as the "object to jump to" for our loaded
        # object + the given direction
        #
        driven_object = self.controller.get_selection()[-1]
        self.controller.assign(self.loaded_object, direction, driven_object)

        self.update_appearance()

    def toggle_mode(self):
        '''Change from Selection Mode to Assignment Mode or vice-versa.'''
        index_for_the_new_mode = 1 - self.mode_options.index(self._current_mode)
        self.set_mode(self.mode_options[index_for_the_new_mode])

    def update_appearance(self):
        '''Set the GUI's widget colors and options based on our stored info.'''
        self.loaded_object_widget.setText('<NO OBJECT FOUND>')

        # Repopulate the assignment details for the loaded object
        self.clear_info_widgets()

        info = self.controller.get_settings(self.loaded_object)

        for key in sorted(six.iterkeys(info)):
            if key == self.manager.main_widget.objectName():
                continue

            assigned_direction_object = info[key]
            self._add_info_line_widget(key, assigned_direction_object)

        is_assignment_mode = self._current_mode == self.assignment_mode_label

        if is_assignment_mode and self.has_loaded_object():
            self.loaded_object_widget.setText(
                self.controller.get_object_name(self.loaded_object))

        self.load_widget.setVisible(is_assignment_mode)
        self.manager.main_widget.setEnabled(is_assignment_mode)
        self.manager.main_widget.setVisible(is_assignment_mode)

        if not is_assignment_mode:
            self.manager.main_widget.setPalette(QtGui.QColor(100, 100, 100))
        elif not self.has_loaded_object():
            self.manager.main_widget.setPalette(self.nothing_loaded_color)
        else:
            self.manager.main_widget.setPalette(self.object_loaded_color)

        self.mode_button.setText(self._current_mode)
