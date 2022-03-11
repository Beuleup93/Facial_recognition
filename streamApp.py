#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 21:32:30 2022

@author: macbookair
"""
import cv2
import streamlit as st
from keras.models import model_from_json
import numpy as np
from keras.preprocessing.image import img_to_array
import face_recognition
import pickle
import datetime

# Modèles pré_entraînés pour détection des émotions

# Dictionnaire des émotions
emotion_dict = {0:'ronchonchon', 1 :'content(e)', 2: 'poker face', 3:'triste', 4: 'surpris(e)'}

# chargement du json et création du modèle
json_file = open('pretrained_model/emotion_model1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()

classifier = model_from_json(loaded_model_json)

# Chargement du modèle
classifier.load_weights("pretrained_model/emotion_model1.h5")

apparitions = list()

# XML pour la reconnaissance de visage
try:
    face_cascade = cv2.CascadeClassifier('reconnaissance/haarcascade_frontalface_default.xml')
except Exception:
    st.write("Error loading cascade classifiers")


# Modèle pré_entraîné pour détection du nom
data = pickle.loads(open('pretrained_model/face_enc', "rb").read())

# Modèle pré_entraîné pour détection de l'âge et la date
age_net = cv2.dnn.readNetFromCaffe('pretrained_model/deploy_age.prototxt','pretrained_model/age_net.caffemodel')
gender_net = cv2.dnn.readNetFromCaffe('pretrained_model/deploy_gender.prototxt', 'pretrained_model/gender_net.caffemodel')



    
def main():
    # Face Analysis Application #

    st.markdown("<h1 style='text-align: center; color: white; font-size: 40px;'>Application de reconnaissance faciale</h1>", unsafe_allow_html=True) 


    #st.title("Application de reconnaissance faciale")
    activiteis = ["Accueil", "Détection de visage par webcam", "A propos"]
    choice = st.sidebar.selectbox("Choisir votre onglet pour la détection par webcam", activiteis)
  
    
    if choice == "Accueil":
        html_temp_home1 = """<div style="background-color:#FA8072;padding:10px">
                                            <h4 style="color:white;text-align:center;">
                                            Identification automatique des étudiants du Master SISE 2021/2022</h4>
                                            </div>
                                            </br>"""
        st.markdown(html_temp_home1, unsafe_allow_html=True)
        st.write("""
                 Les fonctionnalités de l'application sont :

                 1. La détection et l'identification de visage

                 2. La détection des émotions (content, surprise, triste, etc) 
                 
                 3. La prédiction du sexe
                 
                 4. La prédiction de l'âge

                 """)
                 
    elif choice == "Détection de visage par webcam":
        # Flux video
        cam = cv2.VideoCapture(0)
        FRAME_WINDOW = st.image([])
        st.header("Webcam en temps réel")
        st.write("Cochez sur le checkbox pour utiliser la webcam")
        run = st.checkbox('Run')        
        
        #Ajout de checkbox
        options = st.sidebar.radio("Choisir les fonctionnalités de détection : ",("Détecter le visage","Afficher le nom",
                                                "Afficher les émotions",
                                                "Afficher l'âge et le genre",
                                               "Tout afficher",))
        ret, image = cam.read() 
        frame_width = int(cam.get(3))
        frame_height = int(cam.get(4))
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date = date.replace(" ", "_")
        date = date.replace(":", "_")
        filename = 'Videos/record_{0}.avi'.format(date)   
        size = (frame_width, frame_height)
        result = cv2.VideoWriter(filename, 
                                 cv2.VideoWriter_fourcc(*'MJPG'),
                                 24, size)
       
        if options == "Détecter le visage":
            
            while run:
                   # lecture des images
                   ret, image = cam.read()
                   
                   #convertir l'image en niveau de gri
                   image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                  
                   # detection des visages
                   faces = face_cascade.detectMultiScale(image=image, scaleFactor=1.3, minNeighbors=5)

                   #chaque visage est repéré par un rectangle
                   for (x, y, w, h) in faces:
                       cv2.rectangle(img=image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
                   
                   image2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                   result.write(image2)
                   FRAME_WINDOW.image(image)
                   
            else:
                #on libere les ressources
                cam.release()
                result.release()
                cv2.destroyAllWindows()
           
       
        elif options == "Afficher les émotions":
            
            while run:
                   # lecture des images
                   ret, image = cam.read()
                   
                   #convertir l'image en niveau de gris
                   image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                  
                   # detection des visages
                   faces = face_cascade.detectMultiScale(image=image, scaleFactor=1.3, minNeighbors=5)
                  
                   #image gray
                   img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                  
                   #chaque visage est repéré par un rectangle
                   for (x, y, w, h) in faces:
                       cv2.rectangle(img=image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
                       roi_gray = img_gray[y:y + h, x:x + w]
                       roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
                       if np.sum([roi_gray]) != 0:
                           roi = roi_gray.astype('float') / 255.0
                           roi = img_to_array(roi)
                           roi = np.expand_dims(roi, axis=0)
                           prediction = classifier.predict(roi)[0]
                           maxindex = int(np.argmax(prediction))
                           finalout = emotion_dict[maxindex]
                           output = str(finalout)
                       label_position = (x, y)
                       cv2.putText(image, output, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                   
                   image2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                   result.write(image2)
                   FRAME_WINDOW.image(image)
            else:
                #on libere les ressources
                cam.release()
                result.release()
                cv2.destroyAllWindows()
        
        elif options == "Afficher le nom":
            
            while run:
                # lecture des images
                ret, image = cam.read()
                
                # convertir l'image en niveau de gris
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5)
             
                # convertir l'image en couleur
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # Encodage de l'image de la webcam
                encodings = face_recognition.face_encodings(image)
                names = []
                
                # Itération dans les encodages
                
                for encoding in encodings:
                   # Comparaison de l'encodage des images vs les encodages du modèle pré-entraîné
                    matches = face_recognition.compare_faces(data["encodings"], encoding)
                    # Si pas de match => "non reconnue"
                    name = "Non reconnue"
                    # Vérification si existence de matches
                    if True in matches:
                        # On récupére la position des matches qu'on stocke dans une variable
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}
                        # Itération dans les index de matches
                        
                        for i in matchedIdxs:
                            # On récupère le nom des matches
                            name = data["names"][i]
                            # On incrémente le compte
                            counts[name] = counts.get(name, 0) + 1
                        # On récupère la valeur max
                        name = max(counts, key=counts.get)
                     
                    # Cette valeur max est ajoutée dans la liste des noms
                    names.append(name)
 
                    # Itération dans les faces reconnues
                    for ((x, y, w, h), name) in zip(faces, names):
                        # Définition du rectangle
                        # Afficher le nom de la prédiction
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(image, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                         0.75, (0, 255, 0), 2)
                        
                        apparitions.append(name)
                    
                    with open('record.txt', 'w') as f:
                         for apparition in np.unique(apparitions):
                             f.write(apparition)
                             f.write('\n')
                             
                image2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                result.write(image2)
                FRAME_WINDOW.image(image)
                
            else:
                cam.release()
                result.release()
                cv2.destroyAllWindows()
            
           
           
        elif options == "Afficher l'âge et le genre":
            
            MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
            age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
            gender_list = ['Homme', 'Femme']
            
            while run:
                
                ret, image = cam.read()
                
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                faces = face_cascade.detectMultiScale(image, scaleFactor = 1.05, minNeighbors = 5)
                for (x, y, w, h) in faces:
                    # On dessine le rectagle en fonction de la face détectée
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255,255,0), 2)
                    # Transforme le visage en matrice + copie
                    face_img = image[y:y + h, h:h + w].copy()
                    
                    # Transformation (normalisation) de la matrice avec les valeurs moyennes du modèle pré_entraîné
                    blob=cv2.dnn.blobFromImage(face_img,1,(244,244),MODEL_MEAN_VALUES,swapRB=True)
                    # Prédiction du genre
                    gender_net.setInput(blob)
                    gender_preds = gender_net.forward()
                    gender = gender_list[gender_preds[0].argmax()]
                    # Prédiction de l'âge
                    age_net.setInput(blob)
                    age_preds = age_net.forward()
                    age = age_list[age_preds[0].argmax()]
                    
                    # On rassemble les deux prédictions dans une variable
                    overlay_text = "%s %s" % (gender, age)
                    
                    # On l'affiche
                    cv2.putText(image, overlay_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                
                image2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                result.write(image2)
                FRAME_WINDOW.image(image)
            
            else:
                #on libere les ressources
                cam.release()
                result.release()
                cv2.destroyAllWindows()                
            
        elif options == "Tout afficher":
            MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
            age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
            gender_list = ['Homme', 'Femme']
            
            while run:
                ret, image = cam.read()
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5)
         
                # Conversion en RGB
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # Encodage de l'image de la webcam
                encodings = face_recognition.face_encodings(image)
                names = []
                  
                
                
                # Prédiction des noms

                for encoding in encodings:

                    matches = face_recognition.compare_faces(data["encodings"],encoding)
                    name = "Non reconnue"
                    if True in matches:
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}

                        for i in matchedIdxs:
                            name = data["names"][i]
                            counts[name] = counts.get(name, 0) + 1
                        name = max(counts, key=counts.get)
                    names.append(name)    
                
                
 
                for ((x, y, w, h), name) in zip(faces, names):
                    # Prédiction des émotions
                    cv2.rectangle(img=image, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=1)
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
                    face_img = image[y:y + h, h:h + w].copy()
                    if np.sum([roi_gray]) != 0:
                        roi = roi_gray.astype('float') / 255.0
                        roi = img_to_array(roi)
                        roi = np.expand_dims(roi, axis=0)
                        prediction = classifier.predict(roi)[0]
                        maxindex = int(np.argmax(prediction))
                        finalout = emotion_dict[maxindex]
                        output = str(finalout)
                    label_position = (x, y)
                    
                    blob=cv2.dnn.blobFromImage(face_img,1,(244,244),MODEL_MEAN_VALUES,swapRB=True)#**
                    # Prédiction du genre
                    gender_net.setInput(blob)
                    gender_preds = gender_net.forward()
                    gender = gender_list[gender_preds[0].argmax()]
                    # Prédiction de l'âge
                    age_net.setInput(blob)
                    age_preds = age_net.forward()
                    age = age_list[age_preds[0].argmax()]
                    overlay_text = "%s %s" % (gender, age)
                    
                    # affichage noms
                    cv2.putText(image, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                    # affichage âge et sexe
                    cv2.putText(image, overlay_text, (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (32, 32, 32), 2, cv2.LINE_AA)
                    
                    # affichage emotion
                    cv2.putText(image, output, (x, y-50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)    
                
                image2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                result.write(image2)
                FRAME_WINDOW.image(image)
            
            else:
                cam.release()
                result.release()
                cv2.destroyAllWindows()                
    
        
        
        
     
    elif choice == "A propos":
        st.subheader("A propos de l'application")
        html_temp_about1= """<div style="background-color:#FA8072;padding:10px">
                                    <h4 style="color:white;text-align:center;">
                                    Application de reconnaissance faciale et de prédiction des émotions, sexes, âges en temps réel utilisant OpenCV, les modèles pré entrainés et Streamlit.
                                    </h4>
                                    </div>
                                    </br>"""
        st.markdown(html_temp_about1, unsafe_allow_html=True)

        html_temp4 = """
                             		<div style="background-color:#FA8072;padding:10px">
                             		<h4 style="color:white;text-align:center;"> Cette application entre dans le cadre de notre formation en data science.</h4>
                             		<h4 style="color:white;text-align:center;">Merci pour la visite</h4>
                             		</div>
                             		<br></br>
                             		<br></br>"""

        st.markdown(html_temp4, unsafe_allow_html=True)
        
    st.sidebar.markdown(""" 
                        <br></br>
                        <br></br>
                        <div style="color:white;text-align:center;"> 
                        <i> Application développée par : Jacky, Hamza, Gwladys et Saliou<i></div>""", unsafe_allow_html=True)




if __name__ == "__main__":
    main()

    