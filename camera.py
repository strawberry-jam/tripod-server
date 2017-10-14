from __future__ import print_function

import logging
import os
import subprocess
import sys
import uuid
import gphoto2 as gp
import base64

from flask import Flask, jsonify

class Camera(object):
	"""docstring for Camera"""
	def __init__(self):
		self.context = gp.gp_context_new()
		self.camera = gp.check_result(gp.gp_camera_new())
		gp.check_result(gp.gp_camera_init(self.camera, self.context))
		log()

	def capture_image(self):
		print("Capturing image..")
		target = self.save_image()

	def save_image(self):
		file_name = "IMG_" + str(uuid.uuid4())[:6]
		gp.check_result(gp.gp_camera_capture(self.camera, gp.GP_CAPTURE_IMAGE, self.context))
		
		target = os.path.join('./captured', file_name)
		
		camera_file = gp.check_result(gp.gp_camera_file_get(
			self.camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL, self.context))
		gp.check_result(gp.gp_file_save(camera_file, target))
		return target

	def log():
		logging.basicConfig(
			format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
		gp.check_result(gp.use_python_logging())

if __name__ == "__main__":
    # app.run(debug = True)
    camera = Camera
    camera.capture_image()