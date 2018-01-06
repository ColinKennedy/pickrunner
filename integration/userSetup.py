#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Integrate Pickrunner into Maya's startup sequence.'''


def override_pickwalk():
    '''Change the default pickWalk command to prefer Pickrunner.

    If the object that the user is pickWalking from has any defined Pickrunner
    settings, read them and use them.

    If there's no mapping for the pickWalk direction defined for Pickrunner,
    just pickWalk instead.

    '''
    raise NotImplementedError('Need to write this')


def main():
    '''Override pickWalk with Pickrunner.'''
    override_pickwalk()


if __name__ == '__main__':
    main()
