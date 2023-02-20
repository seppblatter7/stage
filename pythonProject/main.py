import os
import csv
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas


videos_path= "C:/Users/gabri/desktop/roba_seria/Python/Dataset/archive/top_view/videos"
csv_path = "C:/Users/gabri/desktop/roba_seria/Python/Dataset/archive/top_view/annotations"
output_path= "C:/Users/gabri/desktop/roba_seria/Python/Dataset/archive/top_view/yolo_annotations"



def checkFolder (folderFrame_path):
    if not os.path.exists(folderFrame_path):
        os.makedirs(folderFrame_path)


def pathVideoCsv (csv_path):
    csv_List = os.listdir(csv_path)
    for csv in csv_List:
        csv_file = csv_path + '/' + csv
        return csv_file


#def makeRectDir (outputImages_path, outputImagesRect_path):



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


def saveBoundingBoxes (csv_lines, output_path):
    for line in csv_lines:
        id = line[0]
        bounding_boxes = line[1:]
        txt_name = output_path + "/" + id + ".txt"
        with open(txt_name, 'w') as file:
            image_name1 = txt_name.replace(".txt", ".png")
            image_name = image_name1.replace("txts", "images")
            print (image_name)
            #converto il nome del file nel nome dell immagine
            img = cv2.imread(image_name, 4)
            H, W, C = img.shape
            #imread dell immagine e ne calcolo la shape
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
    csv_file = pathVideoCsv(csv_path)
    csv_lines = extractData(csv_file)
    saveBoundingBoxes(csv_lines, output_path)

    return





list_video = os.listdir(videos_path)
for video_name in list_video:
    file_name = video_name.replace(".mp4", "")
    csv_file = video_name.replace("mp4", "csv")
    outputImages_path = output_path + "/images/" + file_name
    outputTxt_path = output_path + "/txts/" + file_name
    checkFolder(outputImages_path)
    checkFolder(outputTxt_path)
    video2Frames(videos_path + "/" + video_name, outputImages_path)
    csv2txt(csv_path, outputTxt_path)








#A partire dalla cartella video salvare in una lista tutti i video contenuti

#for video in videoList chiamando per ciscuno video2Frame e gli passo percorso della cartella video + nome singolo video
    #Convertire il nome del video nel nome del csv (con basename o replace a mia scelta)
    #usando basename creo una cartella con il nome video con dentro 2 sottocartelle images, labels(txt)
    #chiamare video2frame (path_video + nomevideo, pathoutput + images)
    #faccio e chiamo una nuova fun zione per salvare i txt csv2Txt (path_csv+nome_csv, pathoutput+labels)





