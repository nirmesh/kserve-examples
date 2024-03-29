#!/usr/bin/env python3

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""A client that performs inferences on a ResNet model using the REST API.

The client downloads a test image of a cat, queries the server over the REST API
with the test image repeatedly and measures how long it takes to respond.

The client expects a TensorFlow Serving ModelServer running a ResNet SavedModel
from:

https://github.com/tensorflow/models/tree/master/official/vision/image_classification/resnet#pretrained-models

Typical usage example:

    resnet_client.py
"""

from __future__ import print_function

import base64
import io
import json

import numpy as np
from PIL import Image
import requests
import sys
import os

# The server URL specifies the endpoint of your server running the ResNet
# model with the name "resnet" and using the predict interface.
# SERVER_URL = 'http://localhost:8501/v1/models/model:predict'
SERVER_URL = 'http://image-serving:8501/v1/models/new_model:predict'

# The image URL is the location of the image we should send to the server
IMAGE_URL = 'https://tensorflow.org/images/blogs/serving/cat.jpg'
image_name = str(sys.argv[1])
pic_file_path = '/hotdog_image_classification_app/static/uploads/' + image_name + '.jpg'
#pic_file_path = '/home/jreyes/HotDog_App/hotdog_image_classification_app/static/uploads/' + image_name + '.jpg'

# Current Resnet model in TF Model Garden (as of 7/2021) does not accept JPEG
# as input
MODEL_ACCEPT_JPG = False

Labels = ['hot_dog', 'not_hot_dog']

def main():
  # Download the image
  dl_request = requests.get(IMAGE_URL, stream=True)
  dl_request.raise_for_status()

  if MODEL_ACCEPT_JPG:
    # Compose a JSON Predict request (send JPEG image in base64).
    jpeg_bytes = base64.b64encode(dl_request.content).decode('utf-8')
    predict_request = '{"instances" : [{"b64": "%s"}]}' % jpeg_bytes
  else:
    # Compose a JOSN Predict request (send the image tensor).
    #jpeg_rgb = Image.open(io.BytesIO(dl_request.content))
    # Normalize and batchify the image
    #jpeg_rgb = np.expand_dims(np.array(jpeg_rgb) / 255.0, 0).tolist()
    #predict_request = json.dumps({'instances': jpeg_rgb})
    jpeg_rgb = Image.open(pic_file_path)
    # Normalize and batchify the image
    jpeg_rgb = np.expand_dims(np.array(jpeg_rgb) / 255.0, 0).tolist()
    predict_request = json.dumps({'instances': jpeg_rgb})
    headers = {"content-type": "application/json"}
  # Send few requests to warm-up the model.
  #for _ in range(3):
  #  response = requests.post(SERVER_URL, data=predict_request)
  #  response.raise_for_status()

  # Send few actual requests and report average latency.
  total_time = 0
  #num_requests = 10
  #for _ in range(num_requests):
  response = requests.post(SERVER_URL, data=predict_request, headers=headers)
  response.raise_for_status()
  total_time += response.elapsed.total_seconds()
  prediction = response.json()['predictions'][0]

  print('Prediction class: {}, latency: {} ms'.format(
      Labels[np.argmax(prediction)], (total_time * 1000) ))

  if Labels[np.argmax(prediction)] == "hot_dog":
    pred = "Hot Dog"
  else:
    pred = "Not Hot Dog"
    
  print(pred)

if __name__ == '__main__':
  main()
