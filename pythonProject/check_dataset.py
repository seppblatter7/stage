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


def img2ImgRectangle (folderimages_path, outputimagesRect_path, foldertxt_path):
    images_list = os.listdir(folderimages_path)
    for image in images_list:
        index = 1
        singleimage_path = folderimages_path + "/" + image
        im = cv2.imread(singleimage_path, 4)
        H, W, _ = im.shape
        singletxt_path = foldertxt_path + "/" +str(index) + ".txt"
        boxes_list = Extract_boxes(singletxt_path, W, H)
        img = DrawImage(im, boxes_list)
        cv2.imwrite(outputimagesRect_path + "/" + str(index) + ".png", img)
        print("Saved frame rect n: ", index)
        #plt.figure(figsize=(8, 4.5), edgecolor=("white"))
        #plt.imshow(img)
        #plt.show()

        def DrawImage(image, boxList):
            # im = image.copy
            for box in boxList:
                print(box)
                xmin = box[1]
                ymin = box[2]
                w = box[3]
                h = box[4]

                H, W, C = image.shape
                xmin = int(xmin * W)
                ymin = int(ymin * H)
                xmax = int(xmin + w * W)
                ymax = int(ymin + h * H)
                print(xmin, ymin, xmax, ymax, W, H)

                color = (255, 0, 0)
                thickness = 2
                image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, thickness)

            return image

