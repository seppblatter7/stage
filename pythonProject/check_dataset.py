import os
import csv
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas

#append every line of txt file in a list called "lines", then repeat the process splitting every line into
#5 elements: c, x, y, w, h and append them in "boxes" list
def Extract_boxes(path_txt, W, H):
    with open(path_txt) as file_in:
        lines = []
        for line in file_in:
            lines.append(line)

    boxes = []
    for line in lines:
        c, xc, yc, w, h = line.split(' ')
        x = float(xc) - float(w) / 2
        y = float(yc) - float(h) / 2
        w = float(w)
        h = float(h)
        print(x, y, w, h)

        boxes.append([c, x, y, w, h])

    return boxes


#taken in input "boxes" (list), firstly  assign the value of xMin, yMin, w, h
def DrawImage(image, boxList):
        # im = image.copy
        for box in boxList:
            xmin = box[1]
            ymin = box[2]
            w = box[3]
            h = box[4]

            #takes the true dimension of the image before applying the boxes
            H, W, C = image.shape
            #with H, W of the image obtain true values of the boxes
            xmin = int(xmin * W)
            ymin = int(ymin * H)
            xmax = int(xmin + w * W)
            ymax = int(ymin + h * H)
            print(xmin, ymin, xmax, ymax, W, H)

            #return the image with the boxes drawn
            color = (255, 0, 0)
            thickness = 2
            image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, thickness)

        return image

#take in input path of both the txt and the images as well as the output boxes images path
def img2ImgRectangle (folderimages_path, outputimagesRect_path, foldertxt_path):
    #create a list that contains every
    index = 30
    images_list = os.listdir(folderimages_path)
    for image in images_list:
        singleimage_path = folderimages_path + "/" + image
        im = cv2.imread(singleimage_path, 4)
        H, W, _ = im.shape
        singletxt_path = foldertxt_path + "/" + str(index) + ".txt"
        boxes_list = Extract_boxes(singletxt_path, W, H)
        img = DrawImage(im, boxes_list)
        cv2.imwrite(outputimagesRect_path + "/" + str(index) + ".png", img)
        print("Saved frame rect n: ", index)
        index += 30

img2ImgRectangle()