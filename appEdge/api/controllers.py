from flask import Blueprint, g, render_template, request, jsonify, session, redirect, url_for, current_app as app
import json, os, time, sys, config
from .services import edgeProcessing

api = Blueprint("api", __name__, url_prefix="/api")


# Define url for the user send the image
@api.route('/edge/recognition_cache', methods=["POST"])
def edge_receive_img():
	"""
	This function receives an image from user or client with smartphone or even a insurance camera 
	into smart sity context
	"""
	fileImg = request.files['media']

	if (fileImg):
		fileImg.save(os.path.join(config.SAVE_IMAGES_PATH_EDGE, fileImg.filename))

	
	# this function returns a dict contais status about what happen inside the function
	
	result = edgeProcessing.imageRecognition(fileImg)  

	print(result)
	if (result["status"] ==  "ok"):
		return jsonify(result), 200

	else:
		return jsonify(result), 500

