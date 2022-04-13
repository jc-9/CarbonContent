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
import cv2
import numpy as np
import os

template_path = '/Users/justinclay/PycharmProjects/CarbonContent/ReferenceImages/template.bmp'
source_folder = '/Users/justinclay/PycharmProjects/CarbonContent/CSA with different Carbon content'
# source_folder = '/Users/justinclay/PycharmProjects/CarbonContent/CSA with different Carbon content/test'
reference_template = cv2.imread(template_path, 0)

# Variables
matchThresh = 0.80
k = 0
rotateList = np.array([0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5], dtype=float)  # values (degrees)
totalcount = 0
border = 0
ittercount = 0
rot = None
paddedIm = None
adjustlist = []
img_show = True  # Show image
write_file = False  # Write files with ROI
ROI1_x1 = \
    ROI1_y1 = \
    ROI1_x2 = \
    ROI1_y2 = \
    ROI2_x1 = \
    ROI2_y1 = \
    ROI2_x2 = \
    ROI2_y2 = \
    orginx = \
    orginy = \
    None

ROI1 = np.index_exp[312:348, 695:868]
ROI2 = np.index_exp[308:339, 1169:1328]
ROI3 = np.index_exp[401:668, 1563:1619]
ROI4 = np.index_exp[775:806, 1176:1343]
ROI5 = np.index_exp[768:808, 699:857]
ROI6 = np.index_exp[456:676, 420:483]
templateROI = np.index_exp[288:801, 345:1688]


# Rotate Image
def Rotate_Image(template, rotation=float):
    global paddedIm, border
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


def list_files(path):
    lfile = []
    global result

    for (dirpath, dirnames, filenames) in os.walk(path):
        try:
            if re.findall(".DS_Store", filenames[0]):
                print('.DS Store Found')
                pass
            else:
                lfile += [os.path.join(dirpath, file) for file in filenames]
        except IndexError:
            print('Index Error for .DS_store')
            pass
    return lfile


def offset(x, y):
    roi1_x1 = x + (ROI1[1].start - templateROI[1].start)
    roi1_y1 = y - (templateROI[0].start - ROI1[0].start)
    roi1_x2 = roi1_x1 + (ROI1[1].stop - ROI1[1].start)
    roi1_y2 = roi1_y1 + (ROI1[0].stop - ROI1[0].start)

    roi2_x1 = x + (ROI2[1].start - templateROI[1].start)
    roi2_y1 = y - (templateROI[0].start - ROI2[0].start)
    roi2_x2 = roi2_x1 + (ROI2[1].stop - ROI2[1].start)
    roi2_y2 = roi2_y1 + (ROI2[0].stop - ROI2[0].start)

    return roi1_x1, \
           roi1_y1, \
           roi1_x2, \
           roi1_y2, \
           roi2_x1, \
           roi2_y1, \
           roi2_x2, \
           roi2_y2


def find_pattern(image_path):
    try:
        img1 = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img_copy = img1.copy()

        for rot in rotateList:
            imgrotated_bw = Rotate_Image(img_copy, rot)
            result = cv2.matchTemplate(imgrotated_bw, reference_template, cv2.TM_CCOEFF_NORMED)

            if (result.max() >= matchThresh).any():
                if rot != 0:
                    adjustlist.append(image_path.split("/")[-1] + str(rot))
                print(f'Result:{result.max()} --> file:{image_path}')
                loc = np.where(result == result.max())
                loc_list = [i for i in zip(*loc)]
                orginx = loc_list[0][1]
                orginy = loc_list[0][0]
                ImageRotateBack = Rotate_Image(img1, -rot)
                break
    except Exception as E:
        print(f"Exception for function find_pattern:{E}")
        return orginx,orginy

def point_rotation (rotate_angle,x1,y1):



listOfFiles = list_files(source_folder)
for i in listOfFiles:
    print(i)
    if k != 81:
        # try:
        #     img1 = cv2.imread(i, cv2.IMREAD_GRAYSCALE)
        #     img_copy = img1.copy()
        #     for rot in rotateList:
        #         # Rotate the image & add border. Border is required to preserve image data during rotation.
        #         imgrotated_bw = Rotate_Image(img_copy, rot)
        #         result = cv2.matchTemplate(imgrotated_bw, reference_template, cv2.TM_CCOEFF_NORMED)
        #         # ittercount += 1
        #         if (result.max() >= matchThresh).any():
        #             if rot != 0:
        #                 adjustlist.append(i.split("/")[-1] + str(rot))
        #             print(f'Result:{result.max()} --> file:{i}')
        #             # Show image ROI's - Warning, this has a memory leak, only use to verify a sample of images
        #             # but dont let it run during data collection
        #             try:
        #                 loc = np.where(result == result.max())
        #                 loc_list = [i for i in zip(*loc)]
        #                 orginx = loc_list[0][1]
        #                 orginy = loc_list[0][0]
        orginx, orginy = find_pattern(i)
        if img_show:
            ROI1_x1, \
            ROI1_y1, \
            ROI1_x2, \
            ROI1_y2, \
            ROI2_x1, \
            ROI2_y1, \
            ROI2_x2, \
            ROI2_y2 = offset(orginx, orginy)
            # Convert the Black
            img_color_srch = cv2.cvtColor(imgrotated_bw, cv2.COLOR_BGR2RGB)
            cv2.rectangle(img_color_srch,
                          (orginx, orginy),
                          (orginx + (templateROI[1].stop - templateROI[1].start),
                           (orginy + (templateROI[0].stop - templateROI[0].start))),
                          (255, 0, 255), thickness=3, lineType=cv2.LINE_4)
            cv2.rectangle(img_color_srch,
                          (ROI1_x1, ROI1_y1),
                          (ROI1_x2, ROI1_y2),
                          (255, 0, 255),
                          thickness=3,
                          lineType=cv2.LINE_4
                          )
            cv2.rectangle(img_color_srch,
                          (ROI2_x1, ROI2_y1),
                          (ROI2_x2, ROI2_y2),
                          (255, 0, 255),
                          thickness=3,
                          lineType=cv2.LINE_4
                          )
            # Rotate the color ROI back into the original postision
            colorImageRotateBack = Rotate_Image(img_color_srch, -rot)
            # Delete the border
            crop_color = colorImageRotateBack[2 * border:colorImageRotateBack.shape[0] - 2 * border,
                         2 * border:colorImageRotateBack.shape[1] - 2 * border]
            print('delta', orginy - ROI1_y1)
            cv2.imshow('PatternFind', crop_color)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            # break
        # except Exception as e:
        #     print(f'error 111: {e}')
                break

        except Exception as e:
            print('Error 001:', e)
            totalcount -= 1
    else:
        cv2.destroyAllWindows()
        break

    # import matplotlib.pylab as plt
    # plt.imshow(crop_color)
