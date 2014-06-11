import cv2
import os
import sys
from mousetrap.vision import Camera, HaarLoader, ImageConverter


class TrackerSample(object):

    def run(self):
        # Initialize the camera and get the frame

        SEARCH_FOR_DEVICE = -1
        DEVICE_INDEX = SEARCH_FOR_DEVICE
        CAMERA_WIDTH = 400
        CAMERA_HEIGHT = 300

        camera = Camera(
                device_index=SEARCH_FOR_DEVICE,
                width=CAMERA_WIDTH,
                height=CAMERA_HEIGHT)

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
        SCALE = 1.5

        # Requiring 5 neighbors helps discard invalid faces
        REQUIRED_NEIGHBORS = 5

        faces = cascades["face"].detectMultiScale(gray, SCALE, REQUIRED_NEIGHBORS)

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

TrackerSample().run()
