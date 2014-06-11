import cv2
import os
import sys

from mousetrap.vision import Camera, HaarLoader, ImageConverter

# Initialize the camera and get the frame

camera = Camera(-1, 400, 300)

image = camera.read_image()

# Convert the image to grayscale

gray = ImageConverter.rgb_to_grayscale(image)

# Import the haar cascades

cascades = {
    "face": HaarLoader.from_name("face"),
    "nose": HaarLoader.from_name("nose")
}

# Detect faces using the cascade
# Use a 1.5 scale to ensure the head is always found
# Requiring 5 neighbors helps discard invalid faces

faces = cascades["face"].detectMultiScale(gray, 1.5, 5)

# Fail early if there were no faces

if not len(faces):
    sys.exit(1)

# Unpack the detected face into a more readable dictionary

face = {}
face["x"], face["y"], face["width"], face["height"] = faces[0]

# Get the smaller image for the detected face

face["image"] = gray[face["y"]:face["y"] + face["height"],
                     face["x"]:face["x"] + face["width"]]

# Detect noses using the cascade

noses = cascades["nose"].detectMultiScale(face["image"], 1.3, 5)

# Fail early is there are no noses

if not len(noses):
    sys.exit(1)

# Unpack the nose

nose = {}
nose["x"], nose["y"], nose["width"], nose["height"] = noses[0]

# Determine the central point of the nose
# This is done relative to the face
# It should probably be done relative to the entire picture

nose["center"] = {
    "x": (nose["x"] + nose["width"]) / 2,
    "y": (nose["y"] + nose["height"]) / 2,
}

print nose
