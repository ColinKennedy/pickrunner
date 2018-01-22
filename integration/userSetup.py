#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Integrate Pickrunner into Maya's startup sequence.'''

# IMPORT STANDARD LIBRARIES
import textwrap

# IMPORT THIRD-PARTY LIBRARIES
import pymel.core as pm


def override_pickwalk():
    '''Change the default pickWalk command to prefer Pickrunner.

    If the object that the user is pickWalking from has any defined Pickrunner
    settings, read them and use them.

    If there's no mapping for the pickWalk direction defined for Pickrunner,
    just pickWalk instead.

    '''
    command = pm.nameCommand(
        'pickrunner_Up',
        command='python("from pickrunner import mayarunner;mayarunner.do_pickrun_motion(\'up\')")',
        annotation='Use Pickrunner to go up')
    pm.hotkey(keyShortcut='Up', name=command)

    command = pm.nameCommand(
        'pickrunner_Down',
        command='python("from pickrunner import mayarunner;mayarunner.do_pickrun_motion(\'down\')")',
        annotation='Use Pickrunner to go down')
    pm.hotkey(keyShortcut='Down', name=command)

    command = pm.nameCommand(
        'pickrunner_Left',
        command='python("from pickrunner import mayarunner;mayarunner.do_pickrun_motion(\'left\')")',
        annotation='Use Pickrunner to go left')
    pm.hotkey(keyShortcut='Left', name=command)

    command = pm.nameCommand(
        'pickrunner_Right',
        command='python("from pickrunner import mayarunner;mayarunner.do_pickrun_motion(\'right\')")',
        annotation='Use Pickrunner to go right')
    pm.hotkey(keyShortcut='Right', name=command)




def main():
    '''Override pickWalk with Pickrunner.'''
    override_pickwalk()


if __name__ == '__main__':
    main()
