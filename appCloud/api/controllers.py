from flask import Blueprint, g, render_template, request, jsonify, session, redirect, url_for, current_app as app
import json, os, time, sys, config



api = Blueprint("api", __name__, url_prefix="/api")

# url of cloud -> http://config.HOST_CLOUD:PORT_CLOUD/API//cloud/image_recognition
@api.route("/cloud/image_recognition", methods=["POST"]) 
def cloud_receive_img():
	"""
	This function receives an image from edge server 
	"""

	fileImg = request.files['media']
	if (fileImg):
		fileImg.save(os.path.join(config.SAVE_IMAGES_PATH_CLOUD , fileImg.filename))

	result = {"status": "ok"}
	if (result['status'] == 'ok'):
		return jsonify(result), 200

	else:
		return jsonify(result), 500