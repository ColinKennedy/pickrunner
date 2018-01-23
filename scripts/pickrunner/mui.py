#!/usr/bin/env mpcpython
# -*- coding: utf-8 -*-

'''Maya-UI functions.'''

# IMPORT THIRD-PARTY LIBRARIES:
from maya import OpenMayaUI as omui

# Try to get our binding queue from Qt.py. If we can't, fallback to a
# regular try/except import strategy
#
try:
	from shiboken2 import wrapInstance
except AttributeError:
	from shiboken import wrapInstance

from Qt import QtWidgets
import pymel.core as pm


def get_main_shelf_name():
    '''Get Maya's main shelf widget.

    This is just a convenience method for querying $gShelfTopLevel.

    Example:
        >>> pm.shelfLayout('some_shelf', parent=get_main_shelf_name()).

    Returns:
        str: The name/path to the main Maya shelf.

    '''
    return pm.mel.eval('global string $gShelfTopLevel;$temp=$gShelfTopLevel')


def get_main_window():
    '''<QtWidgets.QWidget> or NoneType: Cast Maya's window to widget.'''
    window_ptr = omui.MQtUtil.mainWindow()

    # The pointer returns None in command-line (mayapy) under situational
    # circumstances (I'm being vague because I don't know why this sometimes
    # happens). In which case, just return None
    #
    if window_ptr is None:
        return

    try:
        obj = long(window_ptr)
    except TypeError:
        return

    return wrapInstance(obj, QtWidgets.QWidget)


def get_main_menu_bar():
    '''<QtWidgets.QMenuBar> or NoneType: The top bar.'''
    maya_window = get_maya_main_window()
    menus = maya_window.findChildren(QtWidgets.QMenu)
    menu_name = [menu.objectName() for menu in menus]
    try:
        index = menu_name.index('mainEditMenu')  # Guaranteed to exist
    except ValueError:
        return None  # mainEditMenu was not found

    edit_menu = menus[index]
    return edit_menu.parent()


def delete_ui_if_exists(*uis):
    '''Delete UIs using a function wrapper to delete Maya UIs, if they exist.

    Args:
        *uis (list[str]): The UI names to delete.

    Returns:
        callable: The wrapped function.

    '''
    def actual_decorator(func):
        '''The function that will be passed.'''
        def wrapped_func(*args, **kwargs):
            '''Delete all uis paseed to delete_ui_if_exists.

            Args:
                *args (list[str]): The position args to process in the function.
                **kwargs (list[str]): The keywords to process in the function.

            Returns:
                callable: The original function.

            '''
            for ui in uis:
                while True:
                    try:
                        pm.deleteUI(ui)
                    except RuntimeError:
                        break

            return func(*args, **kwargs)
        return wrapped_func
    return actual_decorator


def delete_ui_if_exists_qt(uis):
    '''Delete UIs using a function wrapper to delete Maya UIs, if they exist.

    Args:
        *uis (list[str]): The UI names to delete.

    Returns:
        callable: The wrapped function.

    '''
    def actual_decorator(func):
        '''The function that will be passed.'''
        def wrapped_func(*args):
            '''Delete all uis paseed to delete_ui_if_exists.

            Args:
                *args (list[str]): The position args to process in the function.
                **kwargs (list[str]): The keywords to process in the function.

            Returns:
                callable: The original function.

            '''
            maya_main_window = get_main_window()
            widgets = maya_main_window.children()

            for widget in widgets:
                if widget.objectName() in uis:
                    widget.deleteLater()
                    widget = None
                    del widget

            return func(*args)
        return wrapped_func
    return actual_decorator


if __name__ == '__main__':
    print(__doc__)

