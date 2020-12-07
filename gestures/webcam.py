#!/bin/sh -c '`dirname $0`/python2.7 $0'

import sys
sys.path.append('venv/Lib/site-packages')


import time

import numpy as np
import os

import requests
import six.moves.urllib as urllib
import tarfile
import tensorflow as tf
import cv2
import json

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


with open('/home/pi/detection-rpi-client-server/conf/config.json') as f:
    params = json.load(f)
    IP = params['ip']
    PORT = params['port']

# Define the video stream
# Change 0 only if you have more than one webcams.

for i in range(10):
    cap = cv2.VideoCapture(i)
    if not(cap is None or not cap.isOpened()):
        break
        
PATH_TO_CKPT = 'data/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = 'data/label-map.pbtxt'

# Number of classes to detect
NUM_CLASSES = 2

THRESHOLD = 0.9
SLEEP_TIME = 0.5

# Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


# Loading label map
# Label maps map indices to category names, so that when our convolution network
# predicts `5`, we know that this corresponds to `airplane`.  Here we use
# internal utility functions, but anything that returns a dictionary mapping
# integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
    label_map,
    max_num_classes=NUM_CLASSES,
    use_display_name=True
)
category_index = label_map_util.create_category_index(categories)


# Helper code.
def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


# Detection.
with detection_graph.as_default():
    with tf.compat.v1.Session(graph=detection_graph) as sess:
        while True:
            # Read frame from camera.
            ret, image_np = cap.read()
            # Expand dimensions since the model expects images
            # to have shape: [1, None, None, 3].
            image_np_expanded = np.expand_dims(image_np, axis=0)
            # Extract image tensor.
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Extract detection boxes.
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            # Extract detection scores.
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            # Extract detection classes.
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            # Extract number of detections.
            num_detections = detection_graph.get_tensor_by_name(
                'num_detections:0'
            )
            # Actual detection.
            (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded}
            )
            # Visualization of the results of a detection.
            # vis_util.visualize_boxes_and_labels_on_image_array(
            #     image_np,
            #     np.squeeze(boxes),
            #     np.squeeze(classes).astype(np.int32),
            #     np.squeeze(scores),
            #     category_index,
            #     use_normalized_coordinates=True,
            #     line_thickness=8
            # )

            max_score = np.max(np.squeeze(scores))
            max_index = np.argmax(np.squeeze(scores))

            cls_id = np.squeeze(classes).astype(np.int32)[max_index]
            cls_name = category_index[cls_id]['name']

            if max_score > THRESHOLD:
                print(
                    f'Max score at element '
                    f'{max_index} = {max_score:.2f}, '
                    f'has a class {cls_name}'
                )

                payload = {
                    'entity': 'gesture',
                    'label': cls_name
                }
                try:
                    address = f'http://{IP}{":" + PORT if PORT else ""}/detect'
                    r = requests.get(address, params=payload)
                except requests.exceptions.ConnectionError:
                    print('Server is not available')

            # Display output.
            #cv2.imshow('object detection', cv2.resize(image_np, (800, 600)))
            #
            #if cv2.waitKey(25) & 0xFF == ord('q'):
            #    cv2.destroyAllWindows()
            #    break

            time.sleep(SLEEP_TIME)
