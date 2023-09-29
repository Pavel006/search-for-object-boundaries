import cv2
import numpy as np
import json
from os import stat, path


def getJsonPicture(file_name):
    file_size = stat(file_name).st_size

    img = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = 200

    ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    jsonFile = {"file_name": file_name,
                "file_size": file_size,
                "regions": {},
                "file_attributes": {}
                }

    for i in range(0, len(contours)):
        x = []
        y = []
        jsonFile["regions"].update({f"{i}": {}})
        for k in contours[i]:
            for j in k:
                x.append(int(j[0]))
                y.append(int(j[1]))
        jsonFile["regions"][f"{i}"].update(
            {"name": "poligon",
             "all_points_x": x,
             "all_points_y": y
             }
        )

    with open(f"{file_name[0:file_name.find('.')]}.json", 'w') as outfile:
        json.dump(jsonFile, outfile)
        print(f"{file_name[0:file_name.find('.')]}.json сохранен!")


file_name = input("Введите название файла: ")
getJsonPicture(file_name)