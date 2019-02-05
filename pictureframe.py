#!/usr/bin/env python
"""
Loop through images in a directory tree and display each like a picture frame

Author:        Paul Clenahan
Original Date: Feb 3, 2019
"""

import argparse
import os
import stat
import sys
import time
import random
import pygame

def get_image_file(top):
    """
    Pick a random image filename from directory structure.

    Arguments:
    top -- Top level folder to start from

    Based on "Picking a Random Line from a File" algorithm from Perl Cookbook
    by Nathan Torkington, Tom Christiansen. This approach avoids having to
    read the whole directory structure (which has an unknown number of files)
    into memory. Since the structure is read each time, also supports files
    being added to the structure while the program is running.

    Function assumes that directory was copied from a Mac system and ignores
    the various hidden system files that Mac OSX places in the tree. 
    """

    random.seed()

    n=0
    fullname = "None"
    extensions = [".JPG",".jpg", ".PNG", ".png"]

    for root, dirs, files in os.walk(top):
        for name in files:
            current_name = os.path.join(root, name)
            filename, fileext = os.path.splitext(current_name)
            # Only consider images and ignore Apple hidden files
            if fileext in extensions and not ".AppleDouble" in root \
                    and not filename.startswith("."):
                n=n+1
                if random.uniform(0, n) < 1:
                    fullname = current_name

    print("    Randomly Selected Image file:")
    print("     ", fullname)

    return fullname

def correct_orientation(image):
    """
    Checks EXIF information and rotates image accordingly.

    Arguments:
    image -- The pygame image object
    """

    # See if EXIF data is present
    try:
        orientation_tag = str(tags["Image Orientation"])
    except:
        orientation_tag = "None"
        print("    No EXIF data found - No changes to orientation made")
        return image
        
    # Rotate if necessary based on EXIF data    
    if (orientation_tag == "Rotated 90 CW"):
        print("    Correcting for EXIF Rotated 90 CW")
        image = pygame.transform.rotate(image, -90)
    elif (orientation_tag == "Rotated 90 CCW"):   
        print("    Correcting for EXIF Rotated 90 CCW")
        image = pygame.transform.rotate(image, 90)
    elif (orientation_tag == "Rotated 180"):   
        print("    Correcting for EXIF Rotated 180")
        image = pygame.transform.rotate(image, 180)
    else:
        print("    No image orientation correction needed")

    return image

def scale_image(image, t_width, t_height):
    """
    Scale pygame image up/down to fit display size.

    Arguments:
    image -- The pygame image object to be scaled
    t_width -- Target horizontal size (in whole pixels)
    t_height -- Target vertical size (in whole pixels)
    """

    original_width = image.get_width()
    original_height = image.get_height()

    print("    Original width : ", original_width)
    print("    Original height: ", original_height)

    # Find ratios of image to screen

    width_ratio = t_width / original_width
    height_ratio = t_height / original_height

    if (height_ratio <= width_ratio):
        # Height is the constraining dimension, so scale up/down based on that
        new_width = int(original_width * height_ratio)
        new_height = int(original_height * height_ratio)
        image = pygame.transform.smoothscale(image, (new_width, new_height))
    else:
        # Width is the constraining dimension, so scale up/down based on that
        new_width = int(original_width * width_ratio)
        new_height = int(original_height * width_ratio)
        image = pygame.transform.smoothscale(image, (new_width, new_height))

    print("    Scaled width : ", new_width)
    print("    Scaled height: ", new_height)

    return image

def fade(screen, image, fade_mode, display_width, display_height):
    """
    Fade image in/out of display.

    Arguments:
    screen -- pygame Surface for the display
    image -- pygame image Surface to be faded
    fade_mode -- "In" or "Out"
    display_width -- Horizontal size (in whole pixels) of display
    display_height -- Vertical size (in whole pixels) of display
    """

    if fade_mode == "In":
        start = 0
        stop = 255
        rate = 25
    else:
        start = 255
        stop = 0
        rate = -25

    x_pos = (display_width - image.get_width() ) // 2
    y_pos = (display_height - image.get_height() ) // 2

    for fade in range(start, stop, rate):
        image.set_alpha(fade)
        screen.fill((0,0,0))
        screen.blit(image, (x_pos, y_pos) )
        pygame.display.flip()
    else:
        # Final update - make sure we are max or min fade
        image.set_alpha(stop)
        screen.fill((0,0,0))
        screen.blit(image, (x_pos, y_pos) )
        pygame.display.flip()

def cleanup_and_exit():
    """
    Reset pygame display so screen works correctly and exit
    """
    pygame.mouse.set_visible(True)
    pygame.quit()
    sys.exit(1)

def main(top_path, frame_mode, display_time, screen_mode):
    """
    Main picture frame loop that does the real work.

    Arguments:
    top_path -- Top directory structure to look for images in
    frame_mode -- "Landscape", "Portrait", "All" determines what images to show
    display_time -- How many seconds to display each image
    screen_mode -- "Full" for fullscreen, "Half" for 50% screen
    """
    
    print("----- Setting things up -----")
    
    # Test for image support
    if not pygame.image.get_extended():
        print("No extended image support in pygame (which is needed)")
        sys.exit(1)

    # Initialize, get display properties and set up the display

    pygame.init()

    display_info = pygame.display.Info()

    if screen_mode == "Full":
        display_width = display_info.current_w
        display_height = display_info.current_h
        pygame.display.set_mode((display_width, display_height),
                                pygame.FULLSCREEN)
    else:
        display_width = display_info.current_w // 2
        display_height = display_info.current_h // 2
        pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption("Picture Frame")
    pygame.mouse.set_visible(False)

    screen = pygame.display.get_surface()

    print("Detected display resolution is:")
    print("    Width : ", display_width)
    print("    Height: ", display_height)

    # Done setting up the display screen, now we go into main display loop

    keep_looping = True
    n = 0
    
    while keep_looping:

        n = n+1

        print(" ")
        print("----- Iteration: ", n, " -----")

        image_file = get_image_file(top_path)
        
        if image_file == "None":
            print("Could not find any images to display. Exiting.")
            cleanup_and_exit()

        try:
            image = pygame.image.load(image_file)
        except pygame.error as message:
            print("Cannot load image: ", image_file)
            print("Message from pygame was: ", message)
            print("Exiting")
            cleanup_and_exit()
            
        image = image.convert()  # Make image suitable for alpha fade

        image = correct_orientation(image)

        if image.get_width() > image.get_height():
            image_type = "Landscape"
        else:
            image_type = "Portrait"

        print("    Image is: ", image_type)

        if (frame_mode == "All") or (image_type == frame_mode):
            
            image = scale_image(image, display_width, display_height)

            # Fade out previous image

            prev = screen.copy()
            fade(screen, prev, "Out", display_width, display_height)
            
            # Fade in new image

            fade(screen, image, "In", display_width, display_height)

            time.sleep(display_time)
        else:
            print("    Image skipped since we are in ", frame_mode, " mode")

        # Check for any key presses and handle accordingly

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

    cleanup_and_exit()

# Let's get started...

if __name__ == "__main__":

    # Grab any command line arguments
    
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
        help="What image types to display: Landscape, Portrait or All",
        dest="frame_mode"
    )
    parser.add_argument(
        "-t",
        nargs="?",
        default=10,
        type=int,
        help="Time (in seconds) to display each image.",
        dest="display_time"
    )
    parser.add_argument(
        "-s",
        nargs="?",
        default="Full",
        type=str,
        help="Screen mode to run in (Full = Fullscreen, Half = 50%)",
        dest="screen_mode"
    )

    args = parser.parse_args()
    
    print("----- Welcome to Picture Frame -----")
    print("Input arguments are:")
    print("    Path:   ", args.top_path)
    print("    Mode:   ", args.frame_mode)
    print("    Time:   ", args.display_time)
    print("    Screen: ", args.screen_mode)

    main(args.top_path, args.frame_mode, args.display_time, args.screen_mode)
