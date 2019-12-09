#!/usr/bin/env python
"""
Utility to loop through all images in a directory tree and check that pygame
can load each the image file.

This is a companion to the picture frame program that prevents unexpected
exits due to corrupt or unreadable images files. Run this utility on your photo
directory tree prior to using picture frame.

Author:        Paul Clenahan
Original Date: Feb 5, 2019
"""

import argparse
import os
import sys
import pygame

def scan_image_files(top):

    images_checked = 0
    bad_images_count = 0
    extensions = [".JPG",".jpg", ".PNG", ".png"]

    for root, dirs, files in os.walk(top):
        for filename in files:
            filebase, fileext = os.path.splitext(filename)
            # Only consider images and ignore Apple hidden files
            if fileext in extensions and not ".AppleDouble" in root \
                    and not filename.startswith("."):
                images_checked = images_checked +1
                fullname = os.path.join(root, filename)
                try:
                    image = pygame.image.load(fullname)
                except pygame.error as message:
                    bad_images_count = bad_images_count + 1
                    print("Cannot load image: ", fullname)

                if (images_checked // 100) == (images_checked / 100):
                    # Periodically print status
                    print("Images checked: ", images_checked)

    return images_checked, bad_images_count


def cleanup_and_exit():
    """
    Reset pygame display so screen works correctly and exit
    """
    pygame.mouse.set_visible(True)
    pygame.quit()
    sys.exit(1)

def main(top_path):
    
    print("----- Setting things up -----")
    
    # Test for image support
    if not pygame.image.get_extended():
        print("No extended image support in pygame (which is needed)")
        sys.exit(1)

    pygame.init()

    print("----- Beginning Image File Scan -----")
    
    file_count, bad_files = scan_image_files(top_path)

    print("----- Done Image File Scan -----")

    print("    Number of images scanned: ", file_count)
    print("    Number of bad images found: ", bad_files)

    cleanup_and_exit()

# Let's get started...

if __name__ == "__main__":

    # Grab any command line arguments
    
    parser = argparse.ArgumentParser(
        description="Utility to check all images can be loaded by pygame"
    )

    parser.add_argument(
        "-p",
        nargs="?",
        default="/home/pi/FramePictures",
        type=str,
        help="Path to top of a directory tree that contains images",
        dest="top_path"
    )


    args = parser.parse_args()
    
    print("----- Welcome to Image Checker Utility -----")
    print("Input arguments are:")
    print("    Path:   ", args.top_path)


    main(args.top_path)
