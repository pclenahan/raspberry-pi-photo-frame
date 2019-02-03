#!/usr/bin/env python
#FlipFrame Python Slideshow Code
#Written By Tim Giles, 10/10/16
#www.wildcircuits.com
#www.hackaday.io/wildcircuits
#based on code by Brad Montgomery, https://github.com/bradmontgomery/pgSlideShow

import argparse
import os
import stat
import sys
import time
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

pygame.init()
modes = pygame.display.list_modes()
screen = pygame.display.set_mode(max(modes))
#print(pygame.event.get())

#pygame.mouse.set_visible(True)
#pygame.quit()
#sys.exit(1)
n=0
dummy = True

while dummy:
    n = n+1
    print("Looping: ", n)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            dummy = False
            print(event.key==pygame.K_l)
            break
pygame.quit()
