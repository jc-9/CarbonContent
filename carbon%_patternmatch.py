"""
Justin Clay
justinmelmarclay@gmail.com

April 7, 2022- Image analysis to evaluate if the camera image is sensistve enough to detect changes in carbon %
"""
import re
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

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
hist_roi1_06 = []
hist_roi2_06 = []
hist_roi3_06 = []
hist_roi4_06 = []
hist_roi5_06 = []
hist_roi6_06 = []
hist_roi1_07 = []
hist_roi2_07 = []
hist_roi3_07 = []
hist_roi4_07 = []
hist_roi5_07 = []
hist_roi6_07 = []
hist_roi1_08 = []
hist_roi2_08 = []
hist_roi3_08 = []
hist_roi4_08 = []
hist_roi5_08 = []
hist_roi6_08 = []
hist_roi1_09 = []
hist_roi2_09 = []
hist_roi3_09 = []
hist_roi4_09 = []
hist_roi5_09 = []
hist_roi6_09 = []
hist_roi1_10 = []
hist_roi2_10 = []
hist_roi3_10 = []
hist_roi4_10 = []
hist_roi5_10 = []
hist_roi6_10 = []
img_show = False  # Show image
write_file = False  # Write files with ROI
dict_1 = {"roi1": [], 'roi2': [], 'roi3': [], 'roi4': [], 'roi5': [], 'roi6': []}
legend_list = ['0.6%', '0.7%', '0.8%', '0.9%', '1.0%']
ROI1_x1 = \
    ROI1_y1 = \
    ROI1_x2 = \
    ROI1_y2 = \
    ROI2_x1 = \
    ROI2_y1 = \
    ROI2_x2 = \
    ROI2_y2 = \
    ROI3_x1 = \
    ROI3_x2 = \
    ROI3_y1 = \
    ROI3_y2 = \
    ROI4_x1 = \
    ROI4_x2 = \
    ROI4_y1 = \
    ROI4_y2 = \
    ROI5_x1 = \
    ROI5_x2 = \
    ROI5_y1 = \
    ROI5_y2 = \
    ROI6_x1 = \
    ROI6_x2 = \
    ROI6_y1 = \
    ROI6_y2 = \
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

roilist = [ROI1, ROI2, ROI3, ROI4, ROI5, ROI6]
histlist_06 = [hist_roi1_06,
               hist_roi2_06,
               hist_roi3_06,
               hist_roi4_06,
               hist_roi5_06,
               hist_roi6_06,
               hist_roi1_07,
               hist_roi2_07,
               hist_roi3_07,
               hist_roi4_07,
               hist_roi5_07,
               hist_roi6_07,
               hist_roi1_08,
               hist_roi2_08,
               hist_roi3_08,
               hist_roi4_08,
               hist_roi5_08,
               hist_roi6_08,
               hist_roi1_09,
               hist_roi2_09,
               hist_roi3_09,
               hist_roi4_09,
               hist_roi5_09,
               hist_roi6_09,
               hist_roi1_10,
               hist_roi2_10,
               hist_roi3_10,
               hist_roi4_10,
               hist_roi5_10,
               hist_roi6_10
               ]


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

    roi3_x1 = x + (ROI3[1].start - templateROI[1].start)
    roi3_y1 = y - (templateROI[0].start - ROI3[0].start)
    roi3_x2 = roi3_x1 + (ROI3[1].stop - ROI3[1].start)
    roi3_y2 = roi3_y1 + (ROI3[0].stop - ROI3[0].start)

    roi4_x1 = x + (ROI4[1].start - templateROI[1].start)
    roi4_y1 = y - (templateROI[0].start - ROI4[0].start)
    roi4_x2 = roi4_x1 + (ROI4[1].stop - ROI4[1].start)
    roi4_y2 = roi4_y1 + (ROI4[0].stop - ROI4[0].start)

    roi5_x1 = x + (ROI5[1].start - templateROI[1].start)
    roi5_y1 = y - (templateROI[0].start - ROI5[0].start)
    roi5_x2 = roi5_x1 + (ROI5[1].stop - ROI5[1].start)
    roi5_y2 = roi5_y1 + (ROI5[0].stop - ROI5[0].start)

    roi6_x1 = x + (ROI6[1].start - templateROI[1].start)
    roi6_y1 = y - (templateROI[0].start - ROI6[0].start)
    roi6_x2 = roi6_x1 + (ROI6[1].stop - ROI6[1].start)
    roi6_y2 = roi6_y1 + (ROI6[0].stop - ROI6[0].start)

    return roi1_x1, \
           roi1_y1, \
           roi1_x2, \
           roi1_y2, \
           roi2_x1, \
           roi2_y1, \
           roi2_x2, \
           roi2_y2, \
           roi3_x1, \
           roi3_y1, \
           roi3_x2, \
           roi3_y2, \
           roi4_x1, \
           roi4_y1, \
           roi4_x2, \
           roi4_y2, \
           roi5_x1, \
           roi5_y1, \
           roi5_x2, \
           roi5_y2, \
           roi6_x1, \
           roi6_y1, \
           roi6_x2, \
           roi6_y2


listOfFiles = list_files(source_folder)
for i in listOfFiles:
    print(i)
    if k != 81:
        try:
            img1 = cv2.imread(i, cv2.IMREAD_GRAYSCALE)
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
                    try:
                        loc = np.where(result == result.max())
                        loc_list = [i for i in zip(*loc)]
                        orginx = loc_list[0][1]
                        orginy = loc_list[0][0]
                        if i.split('/')[6] == 'PMC 0.6':
                            hist_ROI1 = cv2.calcHist([imgrotated_bw[ROI1]], [0], None, [255], [0, 255])
                            hist_ROI2 = cv2.calcHist([imgrotated_bw[ROI2]], [0], None, [255], [0, 255])
                            hist_ROI3 = cv2.calcHist([imgrotated_bw[ROI3]], [0], None, [255], [0, 255])
                            hist_ROI4 = cv2.calcHist([imgrotated_bw[ROI4]], [0], None, [255], [0, 255])
                            hist_ROI5 = cv2.calcHist([imgrotated_bw[ROI5]], [0], None, [255], [0, 255])
                            hist_ROI6 = cv2.calcHist([imgrotated_bw[ROI6]], [0], None, [255], [0, 255])
                            hist_roi1_06 = + hist_ROI1
                            hist_roi2_06 = + hist_ROI2
                            hist_roi3_06 = + hist_ROI3
                            hist_roi4_06 = + hist_ROI4
                            hist_roi5_06 = + hist_ROI5
                            hist_roi6_06 = + hist_ROI6

                        elif i.split('/')[6] == 'PMC 0.7':
                            hist_ROI1 = cv2.calcHist([imgrotated_bw[ROI1]], [0], None, [255], [0, 255])
                            hist_ROI2 = cv2.calcHist([imgrotated_bw[ROI2]], [0], None, [255], [0, 255])
                            hist_ROI3 = cv2.calcHist([imgrotated_bw[ROI3]], [0], None, [255], [0, 255])
                            hist_ROI4 = cv2.calcHist([imgrotated_bw[ROI4]], [0], None, [255], [0, 255])
                            hist_ROI5 = cv2.calcHist([imgrotated_bw[ROI5]], [0], None, [255], [0, 255])
                            hist_ROI6 = cv2.calcHist([imgrotated_bw[ROI6]], [0], None, [255], [0, 255])
                            hist_roi1_07 = + hist_ROI1
                            hist_roi2_07 = + hist_ROI2
                            hist_roi3_07 = + hist_ROI3
                            hist_roi4_07 = + hist_ROI4
                            hist_roi5_07 = + hist_ROI5
                            hist_roi6_07 = + hist_ROI6

                        elif i.split('/')[6] == 'PMC 0.8':
                            hist_ROI1 = cv2.calcHist([imgrotated_bw[ROI1]], [0], None, [255], [0, 255])
                            hist_ROI2 = cv2.calcHist([imgrotated_bw[ROI2]], [0], None, [255], [0, 255])
                            hist_ROI3 = cv2.calcHist([imgrotated_bw[ROI3]], [0], None, [255], [0, 255])
                            hist_ROI4 = cv2.calcHist([imgrotated_bw[ROI4]], [0], None, [255], [0, 255])
                            hist_ROI5 = cv2.calcHist([imgrotated_bw[ROI5]], [0], None, [255], [0, 255])
                            hist_ROI6 = cv2.calcHist([imgrotated_bw[ROI6]], [0], None, [255], [0, 255])
                            hist_roi1_08 = + hist_ROI1
                            hist_roi2_08 = + hist_ROI2
                            hist_roi3_08 = + hist_ROI3
                            hist_roi4_08 = + hist_ROI4
                            hist_roi5_08 = + hist_ROI5
                            hist_roi6_08 = + hist_ROI6

                        elif i.split('/')[6] == 'PMC 0.9':
                            hist_ROI1 = cv2.calcHist([imgrotated_bw[ROI1]], [0], None, [255], [0, 255])
                            hist_ROI2 = cv2.calcHist([imgrotated_bw[ROI2]], [0], None, [255], [0, 255])
                            hist_ROI3 = cv2.calcHist([imgrotated_bw[ROI3]], [0], None, [255], [0, 255])
                            hist_ROI4 = cv2.calcHist([imgrotated_bw[ROI4]], [0], None, [255], [0, 255])
                            hist_ROI5 = cv2.calcHist([imgrotated_bw[ROI5]], [0], None, [255], [0, 255])
                            hist_ROI6 = cv2.calcHist([imgrotated_bw[ROI6]], [0], None, [255], [0, 255])
                            hist_roi1_09 = + hist_ROI1
                            hist_roi2_09 = + hist_ROI2
                            hist_roi3_09 = + hist_ROI3
                            hist_roi4_09 = + hist_ROI4
                            hist_roi5_09 = + hist_ROI5
                            hist_roi6_09 = + hist_ROI6

                        elif i.split('/')[6] == 'PMC 1.0':
                            hist_ROI1 = cv2.calcHist([imgrotated_bw[ROI1]], [0], None, [255], [0, 255])
                            hist_ROI2 = cv2.calcHist([imgrotated_bw[ROI2]], [0], None, [255], [0, 255])
                            hist_ROI3 = cv2.calcHist([imgrotated_bw[ROI3]], [0], None, [255], [0, 255])
                            hist_ROI4 = cv2.calcHist([imgrotated_bw[ROI4]], [0], None, [255], [0, 255])
                            hist_ROI5 = cv2.calcHist([imgrotated_bw[ROI5]], [0], None, [255], [0, 255])
                            hist_ROI6 = cv2.calcHist([imgrotated_bw[ROI6]], [0], None, [255], [0, 255])
                            hist_roi1_10 = + hist_ROI1
                            hist_roi2_10 = + hist_ROI2
                            hist_roi3_10 = + hist_ROI3
                            hist_roi4_10 = + hist_ROI4
                            hist_roi5_10 = + hist_ROI5
                            hist_roi6_10 = + hist_ROI6

                        if img_show:
                            ROI1_x1, \
                            ROI1_y1, \
                            ROI1_x2, \
                            ROI1_y2, \
                            ROI2_x1, \
                            ROI2_y1, \
                            ROI2_x2, \
                            ROI2_y2, \
                            ROI3_x1, \
                            ROI3_y1, \
                            ROI3_x2, \
                            ROI3_y2, \
                            ROI4_x1, \
                            ROI4_y1, \
                            ROI4_x2, \
                            ROI4_y2, \
                            ROI5_x1, \
                            ROI5_y1, \
                            ROI5_x2, \
                            ROI5_y2, \
                            ROI6_x1, \
                            ROI6_y1, \
                            ROI6_x2, \
                            ROI6_y2 = offset(orginx, orginy)
                            # Convert the Black and white search ROI into color
                            img_color_srch = cv2.cvtColor(imgrotated_bw, cv2.COLOR_BGR2RGB)
                            # cv2.rectangle(img_color_srch,
                            #               (orginx, orginy),
                            #               (orginx + (templateROI[1].stop - templateROI[1].start),
                            #                (orginy + (templateROI[0].stop - templateROI[0].start))),
                            #               (255, 0, 255), thickness=3, lineType=cv2.LINE_4)
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
                            cv2.rectangle(img_color_srch,
                                          (ROI3_x1, ROI3_y1),
                                          (ROI3_x2, ROI3_y2),
                                          (255, 0, 255),
                                          thickness=3,
                                          lineType=cv2.LINE_4
                                          )
                            cv2.rectangle(img_color_srch,
                                          (ROI4_x1, ROI4_y1),
                                          (ROI4_x2, ROI4_y2),
                                          (255, 0, 255),
                                          thickness=3,
                                          lineType=cv2.LINE_4
                                          )
                            cv2.rectangle(img_color_srch,
                                          (ROI5_x1, ROI5_y1),
                                          (ROI5_x2, ROI5_y2),
                                          (255, 0, 255),
                                          thickness=3,
                                          lineType=cv2.LINE_4
                                          )
                            cv2.rectangle(img_color_srch,
                                          (ROI6_x1, ROI6_y1),
                                          (ROI6_x2, ROI6_y2),
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
                    except Exception as e:
                        print(f'error 111: {e}')
                break

        except Exception as e:
            print('Error 001:', e)
            totalcount -= 1
    else:
        cv2.destroyAllWindows()
        break
dict_1['roi1'].append(hist_roi1_06)
dict_1['roi2'].append(hist_roi2_06)
dict_1['roi3'].append(hist_roi3_06)
dict_1['roi4'].append(hist_roi4_06)
dict_1['roi5'].append(hist_roi5_06)
dict_1['roi6'].append(hist_roi6_06)

dict_1['roi1'].append(hist_roi1_07)
dict_1['roi2'].append(hist_roi2_07)
dict_1['roi3'].append(hist_roi3_07)
dict_1['roi4'].append(hist_roi4_07)
dict_1['roi5'].append(hist_roi5_07)
dict_1['roi6'].append(hist_roi6_07)

dict_1['roi1'].append(hist_roi1_08)
dict_1['roi2'].append(hist_roi2_08)
dict_1['roi3'].append(hist_roi3_08)
dict_1['roi4'].append(hist_roi4_08)
dict_1['roi5'].append(hist_roi5_08)
dict_1['roi6'].append(hist_roi6_08)

dict_1['roi1'].append(hist_roi1_09)
dict_1['roi2'].append(hist_roi2_09)
dict_1['roi3'].append(hist_roi3_09)
dict_1['roi4'].append(hist_roi4_09)
dict_1['roi5'].append(hist_roi5_09)
dict_1['roi6'].append(hist_roi6_09)

dict_1['roi1'].append(hist_roi1_10)
dict_1['roi2'].append(hist_roi2_10)
dict_1['roi3'].append(hist_roi3_10)
dict_1['roi4'].append(hist_roi4_10)
dict_1['roi5'].append(hist_roi5_10)
dict_1['roi6'].append(hist_roi6_10)

fig, axs = plt.subplots(ncols=1, nrows=6, figsize=(10, 15),
                        constrained_layout=True)
plt.subplots_adjust(hspace=0.5)

for i2, i3 in list(zip(dict_1['roi1'], legend_list)):
    axs[0].plot(i2, label=i3)
    axs[0].legend(loc='upper right')
    axs[0].set_title('ROI1')
for i2, i3 in list(zip(dict_1['roi2'], legend_list)):
    axs[1].plot(i2, label=i3)
    axs[1].legend(loc='upper right')
    axs[1].set_title('ROI2')
for i2, i3 in list(zip(dict_1['roi3'], legend_list)):
    axs[2].plot(i2, label=i3)
    axs[2].legend(loc='upper right')
    axs[2].set_title('ROI3')
for i2, i3 in list(zip(dict_1['roi4'], legend_list)):
    axs[3].plot(i2, label=i3)
    axs[3].legend(loc='upper right')
    axs[3].set_title('ROI4')
for i2, i3 in list(zip(dict_1['roi5'], legend_list)):
    axs[4].plot(i2, label=i3)
    axs[4].legend(loc='upper right')
    axs[4].set_title('ROI5')
for i2, i3 in list(zip(dict_1['roi6'], legend_list)):
    axs[5].plot(i2, label=i3)
    axs[5].legend(loc='upper right')
    axs[5].set_title('ROI6')

