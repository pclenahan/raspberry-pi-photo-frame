#!/usr/bin/env python
#



import argparse
import os
import stat
import sys
import time
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

def get_image_file(top):

    random.seed()

    for attempts in range(10):   # Try up to 10 times to find an image
        n=0
        for root, dirs, files in os.walk(top):
            for name in files:
                n=n+1
                if random.uniform(0, n) < 1:
                    full_name = os.path.join(root, name)
                    file_name, file_ext = os.path.splitext(full_name)
        if file_ext in (".JPG",".jpg", ".PNG", ".png"):
            break                # If we found an image we are done
        else:
            full_name = "None"

    print("    Image file: ", full_name)

    return full_name

def correct_orientation(image):

    # See if EXIF data is present
    try:
        OrientationTag = str(tags["Image Orientation"])
    except:
        OrientationTag = "None"
        print("    No EXIF data found - No changes to orientation made")
        return image
        
    # Rotate if necessary based on EXIF data    
    if (OrientationTag == "Rotated 90 CW"):
        print("    Correcting for EXIF Rotated 90 CW")
        image = pygame.transform.rotate(image, -90)
    elif (OrientationTag == "Rotated 90 CCW"):   
        print("    Correcting for EXIF Rotated 90 CCW")
        image = pygame.transform.rotate(image, 90)
    elif (OrientationTag == "Rotated 180"):   
        print("    Correcting for EXIF Rotated 180")
        image = pygame.transform.rotate(image, 180)
    else:
        print("    No image orientation correction needed")

    return image

def scale_image(display_width, display_height, image):

    current_width = image.get_width()
    current_height = image.get_height()

    print("    Original width : ", current_width)
    print("    Original height: ", current_height)

    # Prepare Image by Scaling it up/down as needed to fit the screen

    width_ratio = display_width / current_width
    height_ratio = display_height / current_height

    if (height_ratio <= width_ratio):
        # Height is the constraining dimension, so scale up/down based on that
        new_width = int(current_width * height_ratio)
        new_height = int(current_height * height_ratio)
        image = pygame.transform.smoothscale(image, (new_width, new_height))
    else:
        # Width is the constraining dimension, so scale up/down based on that
        new_width = int(current_width * width_ratio)
        new_height = int(current_height * width_ratio)
        image = pygame.transform.smoothscale(image, (new_width, new_height))

    print("    Scaled width : ", new_width)
    print("    Scaled height: ", new_height)

    return image

def cleanUpAndExit():
    pygame.mouse.set_visible(True)
    pygame.quit()
    sys.exit(1)

##### Real work starts here #####

def main(top_path, frame_mode, display_time):

    print("----- Setting things up -----")
    
    # Test for image support
    if not pygame.image.get_extended():
        print("No extended image support in pygame (which is needed)")
        sys.exit(1)

    # Initialize, get display properties and set up the display

    pygame.init()

    display_info = pygame.display.Info()
    display_width = display_info.current_w
    display_height = display_info.current_h

    modes = pygame.display.list_modes()
    pygame.display.set_mode(max(modes), pygame.FULLSCREEN)
    pygame.display.set_caption("Picture Frame")
    pygame.mouse.set_visible(False)

    screen = pygame.display.get_surface()

    print("Detected display resolution is: ", modes)
    print("    Width : ", display_width)
    print("    Height: ", display_height)

    # Done setting up the display screen, now we go into main image loop

    keep_looping = True
    
    while keep_looping:

        print(" ")
        print("----- Iteration: ", iter, " -----")

        image_file = get_image_file(top_path)
        
        if image_file == "None":
            print("Could not find any images to display. Exiting.")
            cleanUpAndExit()

        image = pygame.image.load(image_file)

        image = correct_orientation(image)

        if image.get_width() > image.get_height():
            image_type = "Landscape"
        else:
            image_type = "Portrait"

        print("    Image is: ", image_type)

        if (frame_mode == "All") or (image_type == frame_mode):
            image = scale_image(display_width, display_height, image)
            screen.fill((0,0,0))
            screen.blit(image, ((display_width - image.get_width() )/2,(display_height-image.get_height())/2))
            pygame.display.flip()
            time.sleep(display_time)
        else:
            print("    Image skipped since we are in ", frame_mode, " mode")

        # Check for any key being pressed to exit while loop.

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    frame_mode = "Landscape"
                elif event.key == pygame.K_p:
                    frame_mode = "Portrait"
                elif event.key == pygame.K_a:
                    frame_mode = "All"
                else:
                    keep_looping = False
                break
  
        # Hey, we are done - let"s reset display and exit

    cleanUpAndExit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Displays images for a picture frame"
    )

    parser.add_argument(
        "-p",
        nargs="?",
        default="/home/pi/Pictures",
        type=str,
        help="Path to top of a directory tree that contains images",
        dest="top_path"
    )
    parser.add_argument(
        "-m",
        nargs="?",
        default="All",
        type=str,
        help="Mode that determines what image types to display: Landscape, Portrait or All",
        dest="frame_mode"
    )
    parser.add_argument(
        "-t",
        nargs="?",
        default=2,
        type=int,
        help="Amount of time (in seconds) to display each image.",
        dest="display_time"
    )
    args = parser.parse_args()
    print("----- Welcome to Picture Frame -----")
    print("Path: ", args.top_path)
    print("Mode: ", args.frame_mode)
    print("Time: ", args.display_time)

    main(args.top_path, args.frame_mode, args.display_time)
