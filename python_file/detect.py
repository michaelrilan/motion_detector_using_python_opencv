import cv2
import pandas as pd
from datetime import datetime
import requests



class tolongges:
	def __init__(self):
		self.mlist = []
		self.check = None


obj_tolongges= tolongges()

cam = cv2.VideoCapture(0)

while cam.isOpened():
	#current date
	current_dateTime = datetime.now()
	#format the 12 hr format
	d = datetime.strptime(str(current_dateTime.hour)+":"+str(current_dateTime.minute), "%H:%M")
	formatted_time = d.strftime("%I:%M %p")

	#format the current date in words 
	formatted_date = datetime.now().strftime("%B %d, %Y")


	#this will be the string to be send via payload for date and time column
	date_and_time_express = str(formatted_date) +" at "+ str(formatted_time)	
	#this will be the name of the png file
	file_name =str(current_dateTime.hour)+str(current_dateTime.minute) + str(current_dateTime.second) + str(current_dateTime.microsecond)





	ret,frame1 = cam.read()
	ret,frame2 = cam.read()
	diff = cv2.absdiff(frame1,frame2)
	gray = cv2.cvtColor(diff,cv2.COLOR_RGB2GRAY)
	blur = cv2.GaussianBlur(gray, (5,5),0)
	_,thresh = cv2.threshold(blur,20,255, cv2.THRESH_BINARY)
	dilated = cv2.dilate(thresh,None, iterations=3)
	contours,_ = cv2.findContours(dilated,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#cv2.drawContours(frame1,contours, -1,(0,255,0),2)


	for c in contours:
		if cv2.contourArea(c)< 15000:
			continue
		x,y,w,h = cv2.boundingRect(c)
		cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)

		#save png file
		img_name = "opencv_frame_{}.png".format(file_name)
		cv2.imwrite(img_name, frame1)
		#para makuha yung path ng sinave na png file
		path_file = "/movement_detection/python_file/" + img_name
		obj_tolongges.mlist.append([date_and_time_express,path_file])

		payload_send = {
				"date_and_time":date_and_time_express,
				"image_path": path_file
		}
		obj_tolongges.check= requests.post('http://localhost:3100/tolongges',json=payload_send)
	if cv2.waitKey(10)==ord('q'):
		break


	cv2.imshow('Super_Senior_4th_Year',frame1)




cam.release()
cv2.destroyAllWindows
pdlist = []

for i in range(len(obj_tolongges.mlist)):
	pdlist.append(obj_tolongges.mlist[i][0])

df = pd.DataFrame({'Date_And_Time':pdlist})
print (df)
# 	df = obj_tolongges.df.append({"Date_And_Time": obj_tolongges.mlist[i][0],"Image_Path": obj_tolongges.mlist[i][1]}, ignore_index=True)
# print(df)
