import cv2
import os
import sys
from mousetrap.vision import Camera, HaarLoader, ImageConverter


class TrackerSample(object):

    def __init__(self):
        self.camera = None
        self.cascades = None
        self.image_grayscale = None
        self.faces = None
        self.face = None
        self.noses = None
        self.nose = None
        self.initialize_camera()
        self.initialize_cascades()

    def initialize_camera(self):
        SEARCH_FOR_DEVICE = -1
        DEVICE_INDEX = SEARCH_FOR_DEVICE
        CAMERA_WIDTH = 400
        CAMERA_HEIGHT = 300
        self.camera = Camera(
                device_index=SEARCH_FOR_DEVICE,
                width=CAMERA_WIDTH,
                height=CAMERA_HEIGHT)

    def initialize_cascades(self):
        self.cascades = {
                "face": HaarLoader.from_name("face"),
                "nose": HaarLoader.from_name("nose")
                }

    def run(self):
        self.read_grayscale_image()
        self.detect_faces()
        self.exit_if_no_faces_detected()
        self.unpack_first_face()
        self.extract_face_image()
        self.detect_noses()
        self.exit_if_no_noses_detected()
        self.unpack_first_nose()
        self.calculate_center_of_nose()
        print self.nose

    def read_grayscale_image(self):
        image = self.camera.read_image()
        self.image_grayscale = ImageConverter.rgb_to_grayscale(image)

    def detect_faces(self):
        # Use a 1.5 scale to ensure the head is always found
        SCALE = 1.5
        # Requiring 5 neighbors helps discard invalid faces
        REQUIRED_NEIGHBORS = 5
        self.faces = self.cascades["face"].detectMultiScale(
                self.image_grayscale, SCALE, REQUIRED_NEIGHBORS)

    def exit_if_no_faces_detected(self):
        if len(self.faces) == 0:
            raise Exception('No faces detected')

    def unpack_first_face(self):
        self.face = dict(zip(['x', 'y', 'width', 'height'], self.faces[0]))

    def extract_face_image(self):
        f = self.face
        from_y = f['y']
        to_y = f['y'] + f['height']
        from_x = f['x']
        to_x = f['x'] + f['width']
        f["image"] = self.image_grayscale[from_y:to_y, from_x:to_x]

    def detect_noses(self):
        # Use a 1.5 scale to ensure the head is always found
        SCALE = 1.5
        # Requiring 5 neighbors helps discard invalid faces
        REQUIRED_NEIGHBORS = 5
        self.noses = self.cascades["nose"].detectMultiScale(
                self.face["image"], SCALE, REQUIRED_NEIGHBORS)

    def exit_if_no_noses_detected(self):
        if len(self.noses) == 0:
            raise Exception('No noses detected.')

    def unpack_first_nose(self):
        self.nose = dict(zip(['x', 'y', 'width', 'height'], self.noses[0]))

    def calculate_center_of_nose(self):
        # FIXME: This is done relative to the face; it should probably be done
        # relative to the entire picture
        self.nose["center"] = {
                "x": (self.nose["x"] + self.nose["width"]) / 2,
                "y": (self.nose["y"] + self.nose["height"]) / 2,
                }


TrackerSample().run()
