import os
import csv
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas


#assignining to each path a variable
videos_path= "C:/Users/gabri/desktop/roba_seria/Python/Dataset/archive/wide_view/videos"
csv_path = "C:/Users/gabri/desktop/roba_seria/Python/Dataset/archive/wide_view/annotations"
output_path= "C:/Users/gabri/desktop/roba_seria/Python/Dataset/archive/wide_view/yolo_annotations"


#check if the output destination folder already exists, if not it creates one
def checkFolder (folderFrame_path):
    if not os.path.exists(folderFrame_path):
        os.makedirs(folderFrame_path)


#return the single path of every csv receiving the csv folder path (correct)
def singleCsv (csv_path):
    csv_List = os.listdir(csv_path)
    for csv in csv_List:
        csv_file = csv_path + '/' + csv

        return csv_file


#for every csv file taken in input, read it and save in a list the row
def extractData (csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        #this 4 consecutive instructions make the reader able to start read the cvs from the 5th row because in csv the
        #first 4 row are useless for my purpose
        header = next(reader)
        header = next(reader)
        header = next(reader)
        header = next(reader)
        csv_lines = []
        cont = 0
        for row in reader:
            cont += 1
            if cont % 30 != 0:
                continue
            csv_lines.append(row)

    return csv_lines


#for every line of the csv file, calculate the right dimension of the box and save in a txt
def saveBoundingBoxes (csv_lines, output_path):
    for line in csv_lines:
        #first element of the csv list is always the class
        id = line[0]
        #the rest of the list is what we need to build the boxes so assign it to a new variable
        bounding_boxes = line[1:]
        #build up the txts output path
        txt_path = output_path + "/" + id + ".txt"
        with open(txt_path, 'w') as file:
            #build up the pngs output path from the txts path
            image_name1 = txt_path.replace(".txt", ".png")
            image_path = image_name1.replace("txts", "images")
            img = cv2.imread(image_path, 4)
            H, W, _ = img.shape

            for i in range (0, len(bounding_boxes), 4):
                #check if the specific element "i" inside the bounding_boxes list is empty
                if bounding_boxes[i] == "": continue
                bb_height = float(float(bounding_boxes[i])/H)
                bb_width = float(float(bounding_boxes[i+3])/W)
                bb_left = float(float(bounding_boxes[i+1])/W)
                bb_top = float(float(bounding_boxes[i+2])/H)

                x_center = bb_left + (bb_width/2)
                y_center = bb_top + (bb_height/2)

                if (i == len(bounding_boxes)-4):
                    file.write(f"1 {x_center} {y_center} {bb_width} {bb_height}\n")
                else:
                    file.write(f"0 {x_center} {y_center} {bb_width} {bb_height}\n")

            print("Saved " + f"{id}.txt")








def csv2txt (csv_file, output_path):
    #csv_file = singleCsv(csv_path)
    csv_lines = extractData(csv_file)
    saveBoundingBoxes(csv_lines, output_path)


    return
#for each video taken in input save a  specific amount of frames
def video2Frames (video_path, output_path):
    #function to "capture" video that create a capture object. Its argument can be either the device index or the name
    #of the video (device index is just a number to specify from which camera I am capturing stream if we have just one
    #device I can give 0, (-1) as argument.
    cap = cv2.VideoCapture(video_path)
    index = 0
    #until the capture object is open ....
    while cap.isOpened():
        #read() returns as first value, a boolean that estabilish if the frame read is correct, as second the frame itself
        Ret, Mat = cap.read()
        #if read is correct
        if Ret:
            index += 1
            #setting %30 I save one frame every second of video for a total of 30 frames per sec
            if index % 30 != 0:
                continue
            #the moment index is 30 or multiple, does not do the "continue" and save that specific frame in the folder
            #I decided before
            cv2.imwrite(output_path + '/' + str(index) + ".png", Mat)
            print ("Saved frame n: ", index)
        else:
            break

    cap.release()
    return


#append every line of txt file in a list called "lines", then repeat the process splitting every line into elements:
#c, x, y, w, h and append them in "boxes" list
def Extract_boxes(path_txt, W, H):
    #opening the specific txt
    with open(path_txt) as file_in:
        lines = []
        #append in the list "lines" every single row as one element
        for line in file_in:
            lines.append(line)

    boxes = []
    #for every element (lines in this case) in "lines" list obtain the necessary values to create the box and append
    #as one element the whole 5 key values
    for line in lines:
        c, xc, yc, w, h = line.split(' ')
        x = float(xc) - float(w) / 2
        y = float(yc) - float(h) / 2
        w = float(w)
        h = float(h)

        boxes.append([c, x, y, w, h])

    return boxes


#receive in input the correct 5 key value to establish the coordinates of every figure (player or baloon) and return the
#image with the box drawn
def DrawImage(image, boxList):
        # im = image.copy
        for box in boxList:
            xmin = box[1]
            ymin = box[2]
            w = box[3]
            h = box[4]

            #takes the true dimension of the image before applying the boxes
            H, W, _ = image.shape
            #with H, W of the image obtain true values of the boxes
            xmin = int(xmin * W)
            ymin = int(ymin * H)
            xmax = int(xmin + w * W)
            ymax = int(ymin + h * H)
            #return the image with the boxes drawn
            color = (255, 0, 0)
            thickness = 2
            image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, thickness)

        return image

#(/images/D_20220220_1_0000_0030, /imagesRect ..., /txts/D_20220220_1_0000_0030 )
def img2ImgRectangle (folderimages_path, outputimagesRect_path, foldertxt_path):
    #create a list with every frame contained in the specific directory
    images_list = os.listdir(folderimages_path)
    for image in images_list:
        #obtain the single path of every images
        singleimage_path = folderimages_path + "/" + image
        im = cv2.imread(singleimage_path, 4)
        H, W, C = im.shape
        singletxt_path1 = singleimage_path.replace("images", "txts")
        singletxt_path = singletxt_path1.replace(".png", ".txt")

        #function that extract the coordinates needed to draw the boxes around tha player
        boxes_list = Extract_boxes(singletxt_path, W, H)
        img = DrawImage(im, boxes_list)
        singleimageRect_path = singleimage_path.replace("images", "imagesRect")
        cv2.imwrite(singleimageRect_path, img)
        print("Saved frame rect n: ", os.path.basename(singleimageRect_path))


#build up a list which element correspond to a different video path (es. "D_20220220_1_1650_1680.mp4")
list_video = os.listdir(videos_path)
#for every video in the list
for video_name in list_video:
    #extract the name of this specific video due to give the name of every output folder (es. "D_20220220_1_1650_1680)
    file_name = video_name.replace(".mp4", "")

    #csv_file = video_name.replace("mp4", "csv")

    #estabilish the correct output folder path for: frame, txt, frame rectangolati
    outputImages_path = output_path + "/images/" + file_name
    outputImagesRect_path = output_path + "/imagesRect/" + file_name
    outputTxt_path = output_path + "/txts/" + file_name

    #check if the path already exists and if not create the folder to contain the output files
    checkFolder(outputImages_path)
    checkFolder(outputImagesRect_path)
    checkFolder(outputTxt_path)

    #function to save the amount of frames I need from the videos       ok
    video2Frames(videos_path + "/" + video_name, outputImages_path)

    #function that receive in input the csv file folder path and returns the txts
    csv2txt(csv_path + "/" + video_name.replace(".mp4", ".csv"), outputTxt_path)

    #function that return the images rectangolate receiving txts and normal images path in input
    img2ImgRectangle(outputImages_path, outputImagesRect_path, outputTxt_path)
