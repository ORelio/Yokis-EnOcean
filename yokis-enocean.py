#!/usr/bin/env python3

# =======================================================================
# Yokis Enocean
#
# Service for passing Enocean Switch/Button events to Yokis-Hack commands
# Allows replacing stock Yokis switches with batteryless Enocean switches
#
# By ORelio (c) 2023-2024 - CDDL 1.0
# ==================================================================

import os

# Make sure working directory is script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Static module initialization
import switches
