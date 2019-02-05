#!/usr/bin/env python
"""
Utility to do quick reset of pygame and display.
"""

import os
import stat
import sys
import pygame


def cleanup_and_exit():
    """
    Reset pygame display so screen works correctly and exit
    """
    pygame.mouse.set_visible(True)
    pygame.quit()
    sys.exit(1)

print("Resetting....")

pygame.init()

cleanup_and_exit()

