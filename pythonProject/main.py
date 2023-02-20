import os
import csv
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas


#assignining to each path a variable
videos_path= "C:/Users/gabri/desktop/roba_seria/Python/Dataset/archive/top_view/videos"
csv_path = "C:/Users/gabri/desktop/roba_seria/Python/Dataset/archive/top_view/annotations"
output_path= "C:/Users/gabri/desktop/roba_seria/Python/Dataset/archive/top_view/yolo_annotations"


#check if the output destination folder already exists, if not it creates one
def checkFolder (folderFrame_path):
    if not os.path.exists(folderFrame_path):
        os.makedirs(folderFrame_path)


#return the single path of every csv receiving the csv folder path
def singleCsv (csv_path):
    csv_List = os.listdir(csv_path)
    for csv in csv_List:
        csv_file = csv_path + '/' + csv

        return csv_file


#for every csv file given, read it and save in a list the row
def extractData (csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        header = next(reader)
        header = next(reader)
        header = next(reader)
        csv_lines = []
        for row in reader:
            csv_lines.append(row)

    return csv_lines


#for every line of the csv file, calculate the right dimension of the box and save in a txt
def saveBoundingBoxes (csv_lines, output_path):
    for line in csv_lines:
        #first element of the csv list is always the class
        id = line[0]
        bounding_boxes = line[1:]
        txt_name = output_path + "/" + id + ".txt"
        with open(txt_name, 'w') as file:
            image_name1 = txt_name.replace(".txt", ".png")
            image_name = image_name1.replace("txts", "images")
            img = cv2.imread(image_name, 4)
            H, W, C = img.shape
            for i in range (0, len(bounding_boxes), 4):
                bb_height = float(float(bounding_boxes[i])/H)
                bb_left = float(float(bounding_boxes[i+1])/W)
                bb_top = float(float(bounding_boxes[i+2])/H)
                bb_width = float(float(bounding_boxes[i+3])/W)
                x_center = bb_left + (bb_width/2)
                y_center = bb_top + (bb_height/2)
                if (i == len(bounding_boxes)-4):
                    file.write(f"1 {x_center} {y_center} {bb_width} {bb_height}\n")
                else:
                    file.write(f"0 {x_center} {y_center} {bb_width} {bb_height}\n")

            print("Saved " + f"{id}.txt")


#for each video taken in input save the frames based on the refresh frequency
def video2Frames (video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    index = 0
    while cap.isOpened():
        Ret, Mat = cap.read()
        if Ret:
            index += 1
            if index % 1 != 0:
                continue
            cv2.imwrite(output_path + '/' + str(index) + '.png', Mat)
            print ("Saved frame n: ", index)
        else:
            break
    cap.release()
    return


def csv2txt (csv_path, output_path):
    csv_file = singleCsv(csv_path)
    csv_lines = extractData(csv_file)
    saveBoundingBoxes(csv_lines, output_path)

    return


#build up a list containing every video path
list_video = os.listdir(videos_path)
for video_name in list_video:
    #extract the name of every video due to give the name of every output folder
    file_name = video_name.replace(".mp4", "")
    csv_file = video_name.replace("mp4", "csv")
    outputImages_path = output_path + "/images/" + file_name
    outputTxt_path = output_path + "/txts/" + file_name
    checkFolder(outputImages_path)
    checkFolder(outputTxt_path)
    video2Frames(videos_path + "/" + video_name, outputImages_path)
    csv2txt(csv_path, outputTxt_path)