from flask import current_app as app
import numpy as np
import cv2 as cv
import os
import uuid


def object_detect(path):
    conf_threshhold = 0.4
    nms_threshhold = 0.4

    class_names = []

    # read data
    # with open('./model/coco.names', 'r') as f:
    with open('./model/plastic.names', 'r') as f:
        class_names = [cname.strip() for cname in f.readlines()]

    my_img = cv.imread(path)

    # net = cv.dnn.readNet('yolov4-p6.weights', 'yolov4-p6.cfg')
    # net = cv.dnn.readNet('./model/yolov4-tiny.weights', './model/yolov4-tiny.cfg')

    # custom yolov4 detector
    net = cv.dnn.readNet('./model/plastic.weights', './model/plastic.cfg')
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)

    model = cv.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

    classes, scores, boxes = model.detect(my_img, conf_threshhold, nms_threshhold)

    for (class_id, score, box) in zip(classes, scores, boxes):
        print(f"{class_id} {score} {box}")

    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    i = 0
    for (class_id, score, box) in zip(classes, scores, boxes):
        color = colors[i]
        label = f'{class_names[class_id[0]]}: {round(float(score*100), 2)}%'
        cv.rectangle(my_img, box, color, 1)
        cv.putText(my_img, label, (box[0], box[1]-10), cv.FONT_HERSHEY_COMPLEX, 0.5, color, 2)
        i += 1

    objects = [class_names[x[0]] for x in classes]
    c_pos = (10,50)
    res2 = cv.putText(my_img, 'COUNT', c_pos, cv.FONT_HERSHEY_SIMPLEX, 0.5, (209, 80, 0, 255), 2)

    remove_dups = sorted(list(set(objects)))
    y_axis = 70
    for x in range(len(remove_dups)):

        obj_pos = (10,y_axis)
        res3 = cv.putText(my_img, f"{remove_dups[x]}: {objects.count(remove_dups[x])}", obj_pos, cv.FONT_HERSHEY_SIMPLEX, 0.5, (209, 80, 0, 255), 2)
        y_axis += 20
    # cv.imwrite('output.png', text)

    filename = str(uuid.uuid4().hex) + '.jpg'
    path = os.path.join(app.config["OUTPUT_PATH"], filename)

    cv.imwrite(path, res2)

    return path
