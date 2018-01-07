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
    def _override_hotkey(direction):
        '''Force the direction key .

        Args:
            direction (str):
                The key/direction to override.
                Options: ["Up", "Down", "Left", "Right"].

        '''
        # Clear the existing hotket
        pm.hotkey(keyShortcut=direction, name='')

        # Construct the new hotkey
        command_name = 'pickrun_{direction}'.format(direction=direction)
        annotation = 'Try to use Pickrunner to move "{direction}"'

        # nameCommand requires MEL so we have to use MEL to call Python
        command = textwrap.dedent(
            '''
            from pickrunner import mayarunner
            mayarunner.do_pickrun_motion("{direction}")
            '''
        ).format(direction=direction.lower())
        command = ';'.join(command.split('\n'))
        command = 'python("{command}")'.format(command=command)

        # Make the command + hotkey with the new command
        pm.nameCommand(command_name, annotation=annotation, command=command)
        pm.hotkey(keyShortcut=direction, name=command_name)

    for direction in ["Up", "Down", "Left", "Right"]:
        _override_hotkey(direction)


def main():
    '''Override pickWalk with Pickrunner.'''
    override_pickwalk()


if __name__ == '__main__':
    main()
