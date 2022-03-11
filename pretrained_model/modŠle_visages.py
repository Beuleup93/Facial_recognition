#!/usr/bin/env python
# coding: utf-8

# In[72]:


from imutils import paths
import face_recognition
import pickle
import cv2
import os

os.chdir(r'C:\Users\jacky\OneDrive\Bureau\Remise à niveau\Projet WebMining')
# Chemin vers le dossier contenant les photos des élèves
imagePaths = list(paths.list_images('jacky'))
knownEncodings = []
knownNames = []
# Itération dans le dossier pour récupérer les photos
for (i, imagePath) in enumerate(imagePaths):
    # On extrait le nom des personnes
    start = imagePath.find("jacky\\") + len("jacky\\")
    end = imagePath.find(".jpg")
    name = imagePath[start:end]
    
    # Conversion en RGB
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Utilisation d'un CNN de la librairie face_recognition pour détecter les visages
    boxes = face_recognition.face_locations(rgb,model='cnn')
    # Encodages des visages
    encodings = face_recognition.face_encodings(rgb, boxes)
    # Itération dans les encodages
    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)
# Exportation du modèle entraîné
data = {"encodings": knownEncodings, "names": knownNames}
# Avec pickle
f = open("face_enc", "wb")
f.write(pickle.dumps(data))
f.close()

