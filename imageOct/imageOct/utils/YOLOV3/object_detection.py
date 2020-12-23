# This code is written at BigVision LLC. It is based on the OpenCV project. It is subject to the license terms in the LICENSE file found in this distribution and at http://opencv.org/license.html

import os

import cv2 as cv
import numpy as np

basedir = os.path.dirname(os.path.abspath(__file__))

imgs = os.path.join(basedir, 'imgs')
# Initialize the parameters
confThreshold = 0.5  # Confidence threshold
nmsThreshold = 0.4  # Non-maximum suppression threshold
inpWidth = 544  # Width of network's input image
inpHeight = 544  # Height of network's input image






# Load names of classes
classesFile = os.path.join(basedir, "data/coco.names")
# classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Give the configuration and weight files for the model and load the network using them.
modelConfiguration = os.path.join(basedir, "cfg/yolov3.cfg")
modelWeights = os.path.join(basedir, "yolov3.weights")

# print(classesFile, modelConfiguration, modelWeights)

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# Draw the predicted bounding box
def drawPred(classId, conf, left, top, right, bottom, frame):
    # here
    label_Probability = dict()
    # Draw a bounding box.
    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

    label = '%.2f' % conf

    # Get the label for the class name and its confidence
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)
        # print('The label is : ', label)
        label_Probability[label.split(':')[0]] = label.split(':')[1]
        # print(label_Probability)
    # Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(frame, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine),
                 (255, 255, 255), cv.FILLED)
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)
    # here
    return label_Probability


# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    result = []
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        x = drawPred(classIds[i], confidences[i], left, top, left + width, top + height, frame)
        result.append(x)
    return result



def detection_single_image(img_path):
    cap = cv.VideoCapture(img_path)
    hasFrame, frame = cap.read()
    print("img_path===",img_path)
    name = img_path.split('\\')[-1].split('.')[0]
    print("name==",name)
    print(type(frame))
    blob = cv.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=True)
    # Sets the input to the network
    net.setInput(blob)
    # Runs the forward pass to get output of the output layers
    outs = net.forward(getOutputsNames(net))
    # Remove the bounding boxes with low confidence
    result = postprocess(frame, outs)
    # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
    # print('The label is : ', label) time
    # cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
    # print("推理时间为",label)
    print("result==",result)
    if len(result) > 0:
        img_label = list(result[0].keys())[0]
    else:
        img_label = "normal"
    print("img_label==",img_label)
    if img_label =="Scratches":
        outputFile = os.path.join("E:/imageOct/imageOct/static/scratch", '{}.jpg'.format(name))
    elif img_label == "Bubbles":
        outputFile = os.path.join("E:/imageOct/imageOct/static/bubble", '{}.jpg'.format(name))
    else:
        outputFile = os.path.join("E:/imageOct/imageOct/static/download", '{}.jpg'.format(name))
    cv.imwrite(outputFile, frame.astype(np.uint8))
    d = {list(i.keys())[0]: list(i.values())[0] for i in result}
    return d



