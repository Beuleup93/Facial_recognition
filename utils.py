#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 07:58:59 2022

@author: macbookair
"""

import streamlit as st 
import time
import cv2
from PIL import Image,ImageEnhance
import numpy as np 

face_cascade = cv2.CascadeClassifier('reconnaissance/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('reconnaissance/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('reconnaissance/haarcascade_smile.xml')



def detect_faces(our_image):
	new_img = np.array(our_image.convert('RGB'))
	img = cv2.cvtColor(new_img,1)
	gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
	# Detect faces
	faces = face_cascade.detectMultiScale(gray, 1.1, 4)
	# Draw rectangle around the faces
	for (x, y, w, h) in faces:
				 cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
	return img,faces 


def detect_eyes(our_image):
	new_img = np.array(our_image.convert('RGB'))
	img = cv2.cvtColor(new_img,1)
	gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
	eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
	for (ex,ey,ew,eh) in eyes:
	        cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
	return img

def detect_smiles(our_image):
	new_img = np.array(our_image.convert('RGB'))
	img = cv2.cvtColor(new_img,1)
	gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
	# Detect Smiles
	smiles = smile_cascade.detectMultiScale(gray, 1.1, 4)
	# Draw rectangle around the Smiles
	for (x, y, w, h) in smiles:
	    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
	return img

def cartonize_image(our_image):
	new_img = np.array(our_image.convert('RGB'))
	img = cv2.cvtColor(new_img,1)
	gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
	# Edges
	gray = cv2.medianBlur(gray, 5)
	edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
	#Color
	color = cv2.bilateralFilter(img, 9, 300, 300)
	#Cartoon
	cartoon = cv2.bitwise_and(color, color, mask=edges)

	return cartoon

def record(cam):
        ret, frame = cam.read()
        if ret:
            record = "record-" + time.strftime("%d-%m-%Y-%H-%M-%S")
            fourcc = cv2.VideoWriter_fourcc(*'h263')
            op = cv2.VideoWriter(record + ".MP4", fourcc, 11.0, (640, 480))
            while 1:
                op.write(frame)
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                #    ret = False

def cannize_image(our_image):
	new_img = np.array(our_image.convert('RGB'))
	img = cv2.cvtColor(new_img,1)
	img = cv2.GaussianBlur(img, (11, 11), 0)
	canny = cv2.Canny(img, 100, 150)
	return canny

def main():
	"""Face Detection App"""

	st.title("Reconnaissance faciale")
	st.text("Construit avec Streamlit et OpenCV")

	activities = ["Détection de visage par image","A propos"]
	choice = st.sidebar.selectbox("Choisir votre onglet pour la détection par image",activities)

	if choice == 'Détection de visage par image':
        
		our_image = Image.open("known_faces/Zuckerberg.png")

		image_file = st.file_uploader("Télécharger une image",type=['jpg','png','jpeg'])
        
    
        
		if image_file is not None:
			our_image = Image.open(image_file)
			st.text("Original Image")
			st.write(type(our_image))
			st.image(our_image)

		enhance_type = st.sidebar.radio("Améliorer le type",["Original","Echelle de gris","Contraste","Luminosité","Floutage"])
		if enhance_type == 'Echelle de gris':
			new_img = np.array(our_image.convert('RGB'))
			img = cv2.cvtColor(new_img,1)
			gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			# st.write(new_img)
			st.image(gray)
		elif enhance_type == 'Contraste':
			c_rate = st.sidebar.slider("Contraste",0.5,3.5)
			enhancer = ImageEnhance.Contrast(our_image)
			img_output = enhancer.enhance(c_rate)
			st.image(img_output)

		elif enhance_type == 'Luminosité':
			c_rate = st.sidebar.slider("Luminosité",0.5,3.5)
			enhancer = ImageEnhance.Brightness(our_image)
			img_output = enhancer.enhance(c_rate)
			st.image(img_output)

		elif enhance_type == 'Floutage':
			new_img = np.array(our_image.convert('RGB'))
			blur_rate = st.sidebar.slider("Floutage",0.5,3.5)
			img = cv2.cvtColor(new_img,1)
			blur_img = cv2.GaussianBlur(img,(11,11),blur_rate)
			st.image(blur_img)
           
		elif enhance_type == 'Original':
			st.image(our_image,width=300)
		else:
			st.image(our_image,width=300)



		# Face Detection
		task = ["Visage","Sourire","Yeux","Contouré","Cartonné"]
		feature_choice = st.sidebar.selectbox("Choisir les caractéristiques",task)
		if st.button("Afficher"):

			if feature_choice == 'Visage':
				result_img,result_faces = detect_faces(our_image)
				st.image(result_img)

				st.success("Détecté {} visage".format(len(result_faces)))
			elif feature_choice == 'Sourire':
				result_img = detect_smiles(our_image)
				st.image(result_img)


			elif feature_choice == 'Yeux':
				result_img = detect_eyes(our_image)
				st.image(result_img)

			elif feature_choice == 'Cartonné':
				result_img = cartonize_image(our_image)
				st.image(result_img)

			elif feature_choice == 'Contouré':
				result_canny = cannize_image(our_image)
				st.image(result_canny)




	elif choice == 'A propos':
		st.subheader("A propos de l'application")
		st.markdown("Construit par Jacky, Hamza, Gwladys et Saliou")
		#st.text("Jesse E.Agbe(JCharis)")
		#st.success("Jesus Saves @JCharisTech")
        
    


if __name__ == '__main__':
		main()	