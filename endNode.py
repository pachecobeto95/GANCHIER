import os, config
import requests, sys, json, os
import numpy as np
from routines.sendData import sendImg

"""
End Device Routine to test Edge device and cloud server
this file sends an image
"""
try:
	filePath = os.path.join("landmarks", "landmarks", "Query")
	file_list = os.listdir(filePath) 

	# choice an random file to send to the edge server
	fileName = file_list[np.random.choice(range(len(file_list)))]
	filePath = os.path.join(filePath, fileName)
	
	url = config.URL_EDGE + "/api/edge/recognition_cache"
	sendImg(url, filePath, fileName)


except Exception as e:
	print(e.args)