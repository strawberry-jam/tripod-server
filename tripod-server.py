from __future__ import print_function

import logging
import os
import subprocess
import sys
import uuid
import gphoto2 as gp
import base64

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/capture', methods=['POST'])
def capture():
	file_name = capture_image()
	encoded_string = ""
	with open(file_name, "rb") as image_file:
		encoded_string = str(base64.b64encode(image_file.read()))

	encoded_string = encoded_string.lstrip("b'").rstrip("'")

	response = {"name" : file_name ,
				"cameraModel" : "Canon E0S 60D",
				"base64Image" : encoded_string }

	return jsonify(response)


def capture_image():
	log()
	camera_context = gp.gp_context_new()
	camera = gp.check_result(gp.gp_camera_new())

	gp.check_result(gp.gp_camera_init(camera,camera_context))
	print('Capturing Image...')
	target = save_image(camera, camera_context)
	# open_image(target)
	exit_camera(camera, camera_context)
	return target

def open_image(target):
	subprocess.call(['xdg-open', target])

def exit_camera(camera, camera_context):
	gp.check_result(gp.gp_camera_exit(camera, camera_context))

def save_image(camera, camera_context):
	# save as a different file name
	# avoid overriding image
	file_name = "IMG_" + str(uuid.uuid4())[:6]
	file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE, camera_context))
	print('Camera file path: {0}/{1}'.format(file_path.folder, file_name))
	target = os.path.join('./captured', file_name)
	camera_file = gp.check_result(gp.gp_camera_file_get(
		camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL, camera_context))
	gp.check_result(gp.gp_file_save(camera_file, target))
	return target

def log():
	logging.basicConfig(
		format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
	gp.check_result(gp.use_python_logging())


if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug = True)