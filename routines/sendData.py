import requests, sys, os, json

def sendImg(url:str, imgFile, fileName:str):
	"""
	This function receives url of the edge device, the image name and then sends the image to the edge
	input:
	url: (str)
	imgFile: (object) the file that contains image
	filename: (str) 

	output: 
	None

	"""

	try:
		files = {"media": open(imgFile, "rb")}
		r = requests.post(url, files=files)

		if (r.status_code != 201 and r.status_code !=200):
			raise Exception("Received an unsuccessful status code of %s"%(r.status_code))

	except Exception as err:
		print(err.args)

	else:
		print("Upload Achieved of " + fileName)


def sendJson(url:str, jsonData:dict):
	try:
		r = requests.post(url, json=jsonData)
		if(r.status_code != 201 and r.status_code != 200):
			raise Exception('Received an unsuccessful status code of '%(r.status_code))

	except Exception as err:
		print(err.args)

	else:
		print("Upload Achieved")