#!/usr/bin/env python3

# ===============================================================
# action - map config entries to actions for use by other modules
# By ORelio (c) 2024 - CDDL 1.0
# ===============================================================

import json

from logs import logs
from shutters import ShutterState

import shutters

def str2action(action: str, setting_name: str = None) -> 'Action':
    '''
    Convert setting (str) to action (object)
    type:name[:data] => object representation
    raises ValueError for invalid syntax or unavailable action type

    Supported actions:
     shutter:shutter_name:operation[/operation_on_release_long_press]

    Notes:
     ([text in brackets] means optional part in action data)
     shutter_name can be several shutters: shutterone+shuttertwo
    '''
    if not setting_name:
        setting_name = '<unknown setting>'

    action_fields = action.split(':')
    if len(action_fields) < 1:
        raise ValueError('Invalid action format for "{}", expecting {}, got "{}"'.format(
            setting_name, 'type:[name[:data]]', action))

    action_type = action_fields[0].lower()
    action_name = action_fields[1] if len(action_fields) > 1 else None
    action_data = action[len(action_type) + len(action_name) + 2:] if len(action_fields) > 2 else None
    action_name_and_data = action[len(action_type) + 1:] if len(action_fields) > 1 else None

    if action_type == 'shutter':
        return ShutterAction(action_name, action_data)
    else:
        raise ValueError('Unknown action type for "{}", expecting {}, got "{}"'.format(
        setting_name, 'shutter', action_type))

class Action:
    '''
    Represents a generic action having a run() function
    secondary_action is set by switches.py when releasing a button. Must be ignored when not used.
    '''
    def __init__(self, name: str, data: str = None):
        raise NotImplementedError('__init__ not implemented.')
    def run(self, secondary_action: bool = False):
        raise NotImplementedError('run() not implemented.')
    def __repr__(self):
        raise NotImplementedError('__repr__ not implemented.')

class ShutterAction(Action):
    '''
    Move a shutter (shutters.py)
    '''
    def __init__(self, name: str, data: str = None):
        self.shutters = name.split('+')
        if data is None:
            raise ValueError('ShutterAction: Missing action for "{}"'.format(name))
        states = data.split('/')
        if len(states) > 2:
            raise ValueError('ShutterAction: Invalid operation format for "{}", got "{}", expecting {}'.format(
                name, data, 'op or op/op_long'))
        self.state = ShutterState[states[0].upper()]
        self.state_long = ShutterState[states[1].upper()] if len(states) > 1 else None
    def run(self, secondary_action: bool = False):
        if secondary_action:
            if self.state_long is not None:
                for shutter in self.shutters:
                    shutters.operate(shutter, self.state_long)
            else:
                logs.info('ShutterAction({}): No Release action'.format(', '.join(self.shutters)))
        else:
            for shutter in self.shutters:
                shutters.operate(shutter, self.state)
    def __repr__(self):
        return 'ShutterAction(Shutter: {}, State: {}, StateReleaseLong: {})'.format(
            ', '.join(self.shutters), self.state, self.state_long)
