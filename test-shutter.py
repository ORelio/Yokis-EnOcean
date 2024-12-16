#!/usr/bin/env python3

# =======================================================
# Test Shutter - Test calibration for a specified shutter
# By ORelio (c) 2023-2024 - CDDL 1.0
# =======================================================

import sys

from shutters import ShutterState
from logs import logs

import shutters
import time

def wait_for_state_percent(shutter: str, state_percent: int):
    while shutters.get_current_state_percent(shutter) != state_percent:
        time.sleep(0.1)

# For each shutter:
#
# 1. Measure each value roughly using a stopwatch
#    When unsure, better use values slightly too high than too low
#
# 2. Set values for then shutter in configuration
#    and restart the service
#
# 3. Using this script, fine tune in order: close, offset, open
#    Update value in config, restart, repeat test until satisfied
#
# 4. Test that everything works as intended using the "half" test
#    Set desired "halfopen" value in config and test that it works
#
def run(shutter: str, test: str):
    if not shutter:
        logs.error('No shutter specified')
        return

    if not test:
        logs.error('No test specified')
        return

    test = test.lower()

    if not test in ['close', 'offset', 'open', 'half']:
        logs.error('Unknown test "{}"'.format(test))
        return

    shutter = shutter.lower()

    if not shutter in shutters._shutters:
        logs.error('Shutter not found: {}'.format(shutter))
        return

    if test == 'close':
        logs.info('Opening shutter to test "close" parameter')
        shutters.operate(shutter, ShutterState.OPEN)
        wait_for_state_percent(shutter, 0)
        logs.info('Moving to closed with blades open')
        logs.info('=> If shutter stops too high, increase "close" parameter')
        logs.info('=> If shutter stops too low, decrease "close" parameter')
        shutters.operate(shutter, ShutterState.HALF, target_half_state=99)
        wait_for_state_percent(shutter, 99)

    if test == 'offset':
        logs.info('Closing shutter to test "offset" parameter')
        shutters.operate(shutter, ShutterState.CLOSE)
        wait_for_state_percent(shutter, 100)
        logs.info('Moving to closed with blades open')
        logs.info('=> If shutter stops too high, decrease "offset" parameter')
        logs.info('=> If shutter stops without opening all blades, increase "offset" parameter')
        shutters.operate(shutter, ShutterState.HALF, target_half_state=99)
        wait_for_state_percent(shutter, 99)

    if test == 'open':
        logs.info('Closing shutter to test "open" parameter')
        shutters.operate(shutter, ShutterState.CLOSE)
        wait_for_state_percent(shutter, 100)
        logs.info('Moving to fully open, then immediately to 10%')
        logs.info('=> If shutter does not reach fully open, increase "open" parameter')
        logs.info('=> If shutter has a noticeable delay before going down, decrease "open" parameter')
        shutters.operate(shutter, ShutterState.HALF, target_half_state=0)
        wait_for_state_percent(shutter, 0)
        shutters.operate(shutter, ShutterState.HALF, target_half_state=10)
        wait_for_state_percent(shutter, 10)

    if test == 'half':
        logs.info('Opening shutter to test OPEN->HALF')
        shutters.operate(shutter, ShutterState.OPEN)
        wait_for_state_percent(shutter, 0)
        logs.info('=> Testing HALF state from OPEN state for shutter {}'.format(shutter))
        shutters.operate(shutter, ShutterState.HALF)
        wait_for_state_percent(shutter, shutters.get_halfway_percent(shutter))
        logs.info('Closing shutter to test CLOSE->HALF')
        shutters.operate(shutter, ShutterState.CLOSE)
        wait_for_state_percent(shutter, 100)
        logs.info('=> Testing HALF state from CLOSE state for shutter {}'.format(shutter))
        shutters.operate(shutter, ShutterState.HALF)
        wait_for_state_percent(shutter, shutters.get_halfway_percent(shutter))

    logs.info('End of test'.format(shutter))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('{} <shutter> <test>'.format(sys.argv[0]))
        print('shutter: shutter name in shutters.ini')
        print('test: close|offset|open|half (launch them in that order)')
        sys.exit(2)
    else:
        run(sys.argv[1], sys.argv[2])
