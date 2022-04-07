"""
Justin Clay
April 7, 2022
justinmelmarclay@gmail.com
gihub: jc-9

Objective: Quanitfy the color differences between CSA's with different carbon % underneath the same production lighting
"""

import cv2
import matplotlib.pyplot as plt
import os
import re

folder = '/Users/justinclay/Downloads/CSA with different Carbon content'
listOfFiles = []


def filelist(path):
    global listOfFiles
    for (dirpath, dirnames, filenames) in os.walk(path):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    for i in enumerate(listOfFiles):
        if re.findall(".DS_Store", i[1]):
            listOfFiles.pop(i[0])
    return listOfFiles


def main():
    file_list = filelist(folder)
    for i in file_list:
        print(i)


if __name__ == '__main__':
    main()
