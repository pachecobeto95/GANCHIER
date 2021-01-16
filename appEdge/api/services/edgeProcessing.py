from flask import jsonify, session, current_app as app
import cv2, os, pickle, requests, sys, config, time
import numpy as np, json

"""
Tasks:
* Insert a lookup search in the cache file that contains all storage features. 
* Adds LFU policy to this cache
* Adds zipf distribution to choice the image in the file endNode.py
* Do the time measurement 


"""

def imageRecognition(fileImg)-> dict:
	"""
	This function must receive an image, extract feature using ORB or SIFT, verify a possible match.
	Then, if positive, this returns reference picture or image name for the user. 
	Otherwise, it sends the raw data to the cloud server.  
	"""
	try:
		cloud_url = "%s/api/cloud/image_recognition"%(config.URL_CLOUD)
		imgPath = os.path.join(config.SAVE_IMAGES_PATH_EDGE, fileImg.filename)
		img = cv2.imread(imgPath)

		
		keypoint, descriptor = extractFeatureByOrb(img)

		match = matchImages_BF_Matcher(descriptor, descriptor)

		if (match):
			# HERE: we need something to return information to user. Return image name or something
			# The information provided to the user is extracted from cache image. 
			# THe matched cache image provide us some nformation to return to user or even the image
			pass 

		else:
			#This line is run, when any image matching is found. 
			result = sendImg(cloud_url, imgPath, fileImg.filename)

		
		#return result
		return {'status': 'ok'}
	except Exception as e:
		print(e.args)

		return {'status': 'error'}



def extractFeatureByOrb(img):
	"""
	This function receives an image and extract its features using Orb 
	Read about ORB technique : https://medium.com/data-breach/introduction-to-orb-oriented-fast-and-rotated-brief-4220e8ec40cf
	Input:
	img: (array) a matrix of pixels values
	
	Output:
	features: (array): extracted features by ORB
	"""

	orb = cv2.ORB_create(nfeatures=config.N_ORB_FEATURES)
	kp1, des1 = orb.detectAndCompute(img, None)

	return kp1, des1


def matchImages_BF_Matcher(des_request, des_cache):
	"""
	This function matches two descriptors and returns match or None, when there's no match and requires 
	cloud
	
	des_request :  current requested descriptor by user
	des_cache :    storaged descriptors in the cache
	"""

	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
	matches = bf.match(des1, des2)
	matches = sorted(matches, key = lambda x:x.distance)

	good = []
	for m,n in matches:
		if m.distance < config.GOOD_FEATURE_RATIO*n.distance:
			good.append([m])


	if len(good) > config.MIN_MATCHES:
		return True

	return False

def matchImages_FLANN(des_request, des_cache):
	"""
	This function matches two descriptors and returns match or None, when there's no match and requires 
	cloud
	
	des_request :  current requested descriptor by user
	des_cache :    storaged descriptors in the cache
	"""
	index_params = dict(algorithm=6, 
		table_number=6,
		key_size=12,
		multi_probe_level=2)


    search_params = {}
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

	good = [] #storage only good feature, that satisfies a threshold distance criteria
	for m,n in matches:
		if m.distance < config.GOOD_FEATURE_RATIO*n.distance:
			good.append([m])


	if len(good) > config.MIN_MATCHES:
		return True

	return False

def sendImg(url: str, imgFile, fileName: str) -> dict:
	"""
	This function sends raw image to the cloud. 
	"""
	try:
		files = {"media": open(imgFile, "rb")}

		r = requests.post(url, files=files)

		if (r.status_code != 201 and r.status_code != 200):
			raise Exception("Received an unsuccessful status code of %s"%(r.status_code))

		return {'status': 'ok'}


	except Exception as err:
		print(err.args)
		sys.exit()

	else:
		print("Upload Achieved")