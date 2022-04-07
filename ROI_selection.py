"""
Justin CLay
Objective: Return the ROI from user input. User will click the mouse button, hold and drag across the image and
release when ROI is acheived. The program will then return the ROI
"""

import cv2
import math
import os
from pathlib import Path

top_corner = []
bottom_corner = []

file = '/Users/justinclay/CarbonContent/CSA with different Carbon content/PMC 0.6/M3_Cam_4_NG_2022-03-28_11-29-27-6203.jfz/Input0_Camera0.jpg'


def drawSquare(action, x, y, flags, userdata):
    global top_corner, bottom_corner, crop
    if action == cv2.EVENT_LBUTTONDOWN:
        top_corner = [(x, y)]

    elif action == cv2.EVENT_LBUTTONUP:
        bottom_corner = [(x, y)]
        # cv2.rectangle(source, top_corner[0], bottom_corner[0], (0, 0, 255), thickness=3)
        cv2.imshow("window", source)
        crop = source[top_corner[0][1]:bottom_corner[0][1], top_corner[0][0]:bottom_corner[0][0]]
        print(f'Image ROI:[{top_corner[0][1]}:{bottom_corner[0][1]}, {top_corner[0][0]}:{bottom_corner[0][0]}]')
        # save_template(crop)
        cv2.imshow('ROI', crop)
        cv2.waitKey(0)


def save_template(im):
    newFilePath = '/Users/justinclay/PycharmProjects/Open_CV/SideProjects/MAS/MAS_FinalInspection_ChipTemplate.jpg'
    cv2.imwrite(newFilePath, im)


source = cv2.imread(file, 1)
cv2.namedWindow("window", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("window", drawSquare)
k = 0

while k != 27:
    cv2.imshow("window", source)
    cv2.putText(source, 'Choose top left corner and drag', (100, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    k = cv2.waitKey(20) & 0xFF

cv2.destroyAllWindows()


