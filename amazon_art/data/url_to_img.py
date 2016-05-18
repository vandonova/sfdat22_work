import sys
sys.path += ['/usr/local/Cellar/opencv/2.4.12_2']
import numpy as np
import urllib
import cv2
#%matplotlib inline

def url_to_image(url):
	#download the image
	resp = urllib.urlopen(url)
	#convert to NumPy array
	image = np.asarray(bytearray(resp.read()), dtype ='uint8')
	#read it into OpenCV
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	
	return image
	
image = url_to_image('http://ecx.images-amazon.com/images/I/519lYUvAxDL._QL70_.jpg')
cv2.imshow('Image', image)
cv2.waitKey(0)


#urls = []

#for x in amazon_art
	