"""
Justin Clay
March 8 2022
justinmelmarclay@gmail.com

April 7, 2022- modification of the pattern match program modified to fit weld b (top, L, R, bottom)

Pattern matcher, uses a rotation list and search area to find pattern.
1 - Open image and cut seach area out of the image
2 - Using search area, attempt template match, if fail then rotate search area image
3 - Once the template has been located, draw shapes and re-stich search area back into original image
"""
import re
import shutil

import cv2
import matplotlib.pyplot as plt
import numpy
import numpy as np
import os
import gc
import time

template_path = '/Users/justinclay/CarbonContent/ReferenceImages/template.bmp'
source_folder = '/Users/justinclay/CarbonContent/CSA with different Carbon content'
reference_template = cv2.imread(template_path, 0)

# Variables
matchThresh = 0.80
k = 0
rotateList = np.array([0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5], dtype=float)  # values (degrees)
border = 0
totalcount = 0
currentcount = 0
goodcount = 0
ittercount = 0
listOfFiles = []
failedlist = []
adjustlist = []
searchArea = np.index_exp[625:1370, 954:1811]
itr = 5  # Iterations for morph operation
action_list = ["dilate", 'erode', 'morph', 'none']
Action = action_list[1]
showcolor = True
img_show = True  # Show image
write_file = False  # Write files with ROI
templateROI = np.index_exp[288:801, 345:1688]


# def numcal(x, y):
#     n = x - y
#     if n <= 0:
#         n = 0
#         return n
#     else:
#         return n


# Rotate Image
def Rotate_Image(template, rotation=float):
    global paddedIm, border
    # border = int((min(template.shape[0], template.shape[1])) / 50)
    border = 50
    paddedIm = np.zeros((template.shape[0] + border * 2, template.shape[1] + border * 2))
    paddedIm = cv2.copyMakeBorder(template, border, border, border, border, cv2.BORDER_CONSTANT, value=0)
    angleInRadians = rotation * np.pi / 180.0
    cosTheta = np.cos(angleInRadians)
    sinTheta = np.sin(angleInRadians)
    centerX = paddedIm.shape[1] / 2
    centerY = paddedIm.shape[0] / 2
    tx = (1 - cosTheta) * centerX - sinTheta * centerY
    ty = sinTheta * centerX + (1 - cosTheta) * centerY
    warpMat = np.float64(
        [
            [cosTheta, sinTheta, tx],
            [-sinTheta, cosTheta, ty]
        ])
    result1 = cv2.warpAffine(paddedIm, warpMat, (paddedIm.shape[1], paddedIm.shape[0]), flags=cv2.INTER_NEAREST)

    return result1


global result
for (dirpath, dirnames, filenames) in os.walk(source_folder):
    try:
        if re.findall(".DS_Store", filenames[0]):
            print('.DS Store Found')
            pass
        else:
            listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    except IndexError:
        print('Index Error for .DS_store')
        pass

for i in listOfFiles:
    print(i)
    if k != 81:
        try:
            img1 = cv2.imread(i, cv2.IMREAD_UNCHANGED)
            img_copy = img1.copy()
            for rot in rotateList:
                # Rotate the image & add border. Border is required to preserve image data during rotation.
                imgrotated_bw = Rotate_Image(img_copy, rot)
                result = cv2.matchTemplate(imgrotated_bw, reference_template, cv2.TM_CCOEFF_NORMED)
                ittercount += 1
                if (result.max() >= matchThresh).any():
                    if rot != 0:
                        adjustlist.append(i.split("/")[-1] + str(rot))
                    print(f'Result:{result.max()} --> file:{i}')
                    # Show image ROI's - Warning, this has a memory leak, only use to verify a sample of images
                    # but dont let it run during data collection
                    try:
                        loc = np.where(result == result.max())
                        loc_list = [i for i in zip(*loc)]
                        if img_show:
                            # Convert the Black and white search ROI into color
                            img_color_srch = cv2.cvtColor(imgrotated_bw, cv2.COLOR_BGR2RGB)
                            cv2.rectangle(img_color_srch,
                                          (loc_list[0][1], loc_list[0][0]),
                                          (loc_list[0][1] + (templateROI[1].stop - templateROI[1].start),
                                           (loc_list[0][0] + (templateROI[0].stop - templateROI[0].start))),
                                          (255, 0, 255), thickness=3, lineType=cv2.LINE_4)
                            # Rotate the color ROI back into the original postision
                            colorImageRotateBack = Rotate_Image(img_color_srch, -rot)
                            # Delete the border
                            crop_color = colorImageRotateBack[2 * border:colorImageRotateBack.shape[0] - 2 * border,
                                         2 * border:colorImageRotateBack.shape[1] - 2 * border]
                            cv2.imshow('PatternFind', crop_color)
                            cv2.waitKey(0)
                            cv2.destroyAllWindows()
                            # break
                    except Exception as e:
                        print(f'error 111: {e}')
                break

        except Exception as e:
            print('Error 001:', e)
            totalcount -= 1
    else:
        cv2.destroyAllWindows()
        break
