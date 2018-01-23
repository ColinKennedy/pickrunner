#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A set of small widgets that are meant to show/hide themselves.'''

# IMPORT THIRD-PARTY LIBRARIES
from Qt import QtWidgets
from Qt import QtCore


class ExpandCollapseWidget(QtWidgets.QWidget):

    '''A "show/hide" widget which opens and closes itself.

    It works by creating an inner widget which is hidden by default which you
    can expand/collapse using "toggle" or "set_children_visible". To add your
    widgets to the section that shows/hides itself, use "add_layout" or
    "add_widget".

    '''

    toggled = QtCore.Signal()

    def __init__(
            self,
            label='',
            side='left',
            layout=QtWidgets.QVBoxLayout,
            parent=None):
        '''Create the GUI's widgets.

        Args:
            label (:obj:`str`, optional):
                A word or phrase to put next to the button.
                Suggestion: "Advanced Settings". Default: "".
            side (:obj:`str`, optional):
                Which direction of the widget to display the show/hide button.
                Options: ('left', 'right'). Default: 'left'.
            layout (:obj:`<callable=QtWidgets.QBoxLayout>`, optional):
                The layout for all the widgets that will be shown/hidden.
                Default: 'QtWidgets.QVBoxLayout'.
            parent (:obj:`<QtCore.QObject>`, optional):
                The Qt-based associated object. Default is None.

        '''
        super(ExpandCollapseWidget, self).__init__(parent=parent)
        self.setLayout(layout())

        options = ('left', 'right')
        if side.lower() not in options:
            raise ValueError('Got side: "{side}" but expected an option, '
                             '"{opt}"'.format(side=side, opt=options))

        self.button = QtWidgets.QToolButton(parent=self)
        self.label = QtWidgets.QLabel(label, parent=self)

        self.expand_widget = QtWidgets.QWidget(parent=self)
        self.expand_widget.setLayout(self.layout().__class__())

        top_layout = QtWidgets.QHBoxLayout()

        if side.lower() == 'left':
            top_layout.addWidget(self.button)
            top_layout.addWidget(self.label)
        elif side.lower() == 'right':
            top_layout.addWidget(self.label)
            top_layout.addWidget(self.button)

        self.layout().addLayout(top_layout)
        self.layout().addWidget(self.expand_widget)

        self.init_default_settings()
        self.init_interactive_settings()

    def init_default_settings(self):
        '''Set-up our expand/collapse button's appearance.'''
        # Hide children by default
        self.set_children_visible(False)

        self.button.setArrowType(QtCore.Qt.RightArrow)

        self.button.setToolTip('Click to expand or collapse the section below')
        self.label.setToolTip('Click the expand button to show/hide widgets')

        self.button.setObjectName('expand_button')
        self.label.setObjectName('expand_label')
        self.expand_widget.setObjectName('expand_hide_widget')

        self.update_toggle_button(self.expand_widget.isVisible())

    def init_interactive_settings(self):
        '''Set our widget's toggle button to emit a signal when it is clicked.'''
        self.button.clicked.connect(self.toggled.emit)
        self.toggled.connect(self.toggle)

    def add_layout(self, layout, *args, **kwargs):
        '''Add Qt layout to the shown/hidden widgets.'''
        self.expand_widget.layout().addLayout(layout)

    def add_widget(self, widget, *args, **kwargs):
        '''Add Qt widget to the shown/hidden widgets.'''
        self.expand_widget.layout().addWidget(widget, *args, **kwargs)

    def set_children_visible(self, visible):
        '''Show/Hide the widgets contained in this object.

        This method will also update all GUI-appearance related code, like
        changing the button icon.

        Args:
            visible (bool): Show the widgets if True. Hide them if False.

        '''
        self.expand_widget.setVisible(visible)
        self.update_toggle_button(visible)

    def update_toggle_button(self, is_visible):
        '''Set the show/hide section to the given value.'''
        if is_visible:
            self.button.setArrowType(QtCore.Qt.DownArrow)
        else:
            self.button.setArrowType(QtCore.Qt.RightArrow)

    def toggle(self):
        '''If the inner-widget section is hidden, show it, and vice-versa.'''
        self.set_children_visible(not self.expand_widget.isVisible())
