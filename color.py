# coding=utf-8
import cv2
import numpy as np
import math


def interplateColor(color1, color2, weight=0.5):
    c1_1 = color1[0]
    c1_2 = color1[1]
    c1_3 = color1[2]

    c2_1 = color2[0]
    c2_2 = color2[1]
    c2_3 = color2[2]

    c3_1 = int((1 - weight) * c1_1 + weight * c2_1)
    c3_2 = int((1 - weight) * c1_2 + weight * c2_2)
    c3_3 = int((1 - weight) * c1_3 + weight * c2_3)
    return [c3_1, c3_2, c3_3]


def genPhColorPlate(phColor):
    color_bar_width = 50
    color_bar_height = 150
    color_bar_margin = 20
    height = 200
    width = len(phColor) * color_bar_width + (len(phColor) + 1) * color_bar_margin
    blank_img = np.zeros([height, width, 3], np.uint8) + 255
    for i in range(len(phColor)):
        center = color_bar_margin + color_bar_width / 2 + i * (color_bar_width + color_bar_margin)
        blank_img[color_bar_margin:color_bar_height,
        center - color_bar_width / 2:center + color_bar_width / 2] = \
            phColor[i]
        blank_img[:color_bar_height, center] = [0, 0, 255]
        if i >= 9:
            cv2.putText(blank_img, (i + 1).__str__(),
                        (center - 22, color_bar_height + 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 0), 1, cv2.LINE_AA)
        else:
            cv2.putText(blank_img, (i + 1).__str__(),
                        (center - 12, color_bar_height + 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 0), 1, cv2.LINE_AA)
    return blank_img


def getPhValueInt(color, phColor):
    dists = []
    for i in range(len(phColor)):
        dist = math.sqrt(
            pow(color[0] - phColor[i][0], 2) + pow(color[1] - phColor[i][1], 2) + pow(color[2] - phColor[i][2], 2))
        print dist
        dists.append(dist)
    return dists.index(min(dists)) + 1


def getPhValueFloat(color, phColor):
    dists = []
    for i in range(len(phColor)):
        dist = math.sqrt(
            pow(color[0] - phColor[i][0], 2) + pow(color[1] - phColor[i][1], 2) + pow(color[2] - phColor[i][2], 2))
        dists.append(dist)
    min_index1 = dists.index(min(dists))
    dist1 = dists[min_index1]
    dists[min_index1] = 999999
    min_index2 = dists.index(min(dists))
    dist2 = dists[min_index2]
    if min_index1 <= min_index2:
        final_ph = min_index1 + abs(min_index1 - min_index2) * (dist1 / (dist1 + dist2))
    else:
        final_ph = min_index1 - abs(min_index1 - min_index2) * (dist1 / (dist1 + dist2))
    return final_ph + 1, min_index1 + 1, min_index2 + 1


def drawPh(ph_color, ph_val, phColor):
    ph_img = genPhColorPlate(phColor)
    color_bar_width = 50
    color_bar_margin = 20
    color_bar_height = 150
    ph = ph_val[0] - 1
    ph1 = ph_val[1] - 1
    ph2 = ph_val[2] - 1
    if ph1 > ph2:
        tmp = ph1
        ph1 = ph2
        ph2 = tmp
    start_pix = color_bar_margin + color_bar_width / 2 + ph1 * (color_bar_width + color_bar_margin)
    end_pix = color_bar_margin + color_bar_width / 2 + ph2 * (color_bar_width + color_bar_margin)
    loc = int((ph - ph1) * (end_pix - start_pix) + start_pix)
    ph_img[:, loc - 1:loc + 1] = ph_color
    cv2.putText(ph_img, "PH=" + round(ph_val[0], 2).__str__(),
                (loc + 1, color_bar_height + 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4, ph_color, 1, cv2.LINE_AA)
    return ph_img


if __name__ == '__main__':
    phColor = []
    phColor.append([0, 4, 206])
    phColor.append([4, 41, 253])
    phColor.append([7, 64, 250])
    phColor.append([79, 83, 255])
    phColor.append([4, 112, 254])
    phColor.append([47, 171, 255])
    phColor.append([93, 216, 196])
    phColor.append([5, 201, 118])
    phColor.append([241, 59, 17])
    phColor.append([163, 0, 1])
    phColor.append([110, 3, 0])
    phColor.append([78, 25, 28])

    # 顺序为BGR
    ph_color = [79, 83, 200]
    ph_val = getPhValueFloat(ph_color, phColor)
    print 'ph', ph_val[0]
    ph_img = drawPh(ph_color, ph_val, phColor)
    cv2.imwrite("PH" + round(ph_val[0], 2).__str__() + ".png", ph_img)
