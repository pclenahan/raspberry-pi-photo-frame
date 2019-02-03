import os
import random

def getImageFileName(top):

    random.seed()

    for attempts in range(10):   # Try up to 10 times to find an image
        n=0
        print("Attempt: ", attempts + 1)
        for root, dirs, files in os.walk(top):
            for name in files:
                n=n+1
                if random.uniform(0, n) < 1:
                    fullName = os.path.join(root, name)
                    fileName, fileExt = os.path.splitext(fullName)
                    print(n)
                    print(fullName)
                    print(fileName)
                    print(fileExt)
                    print("-" * 20)
        if fileExt in (".JPG",".jpg", ".PNG", ".png"):
            print("Found an image on attempt: ", attempts + 1) 
            break                # If we found an image we are done
        else:
            fullName = "None"

    return fullName


imageFileName = getImageFileName("/home/pi/TestImages")
print("Final Image:", imageFileName)
