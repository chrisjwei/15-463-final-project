from django.shortcuts import render
# import the necessary packages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.template import RequestContext, loader

import numpy as np
import urllib
import json
import cv2


def process(request):
  template = loader.get_template('face_swapper/process.html')

  data = {"success": False}
  if 'url' in request.GET:
      url = request.GET.get("url", None)
      if url is None:
        data["error"] = "No URL provided."
        return JsonResponse(data)
      image = _grab_image(url=url)
      results = process_face(image)
      if results["success"]:
        data["results"] = results["measurements"]
        data["success"] = True
      else:
        data["error"] = "Face processing failed."

  return return HttpResponse(template.render(data))

def process_face(image):
  pitch = 0
  yaw = 0
  rotation = 0
  x = 0
  y = 0
  width = 0
  height = 0

  measurements = {"pitch":pitch, "yaw":yaw, "rotation":rotation, "x":x, "y":y, "width":width, "height":height}
  return {"success": True, "measurements": measurements}

@csrf_exempt
def detect(request):
  # initialize the data dictionary to be returned by the request
  data = {"success": False}
 
  # check to see if this is a post request
  if request.method == "POST":
    # check to see if an image was uploaded
    if request.FILES.get("image", None) is not None:
      # grab the uploaded image
      image = _grab_image(stream=request.FILES["image"])
 
    # otherwise, assume that a URL was passed in
    else:
      # grab the URL from the request
      url = request.POST.get("url", None)
 
      # if the URL is None, then return an error
      if url is None:
        data["error"] = "No URL provided."
        return JsonResponse(data)
 
      # load the image and convert
      image = _grab_image(url=url)
 
    ### START WRAPPING OF COMPUTER VISION APP
    # Insert code here to process the image and update
    # the `data` dictionary with your results
    ### END WRAPPING OF COMPUTER VISION APP
 
    # update the data dictionary
    data["success"] = True
    
  # return a JSON response
  return JsonResponse(data)

def _grab_image(path=None, stream=None, url=None):
  # if the path is not None, then load the image from disk
  if path is not None:
    image = cv2.imread(path)
 
  # otherwise, the image does not reside on disk
  else: 
    # if the URL is not None, then download the image
    if url is not None:
      resp = urllib.urlopen(url)
      data = resp.read()
 
    # if the stream is not None, then the image has been uploaded
    elif stream is not None:
      data = stream.read()
 
    # convert the image to a NumPy array and then read it into
    # OpenCV format
    image = np.asarray(bytearray(data), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
  # return the image
  return image

# index page
def index(request):
  template = loader.get_template('face_swapper/index.html')
  context = RequestContext(request, {
      'foo': 'bar'
  })
  return HttpResponse(template.render(context))
