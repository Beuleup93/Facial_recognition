# Facial_Recognition_with_Opencv

This project is about facial recognition and identification on WEBCAM videos. More precisely, the aim of this project is to recognize automatically 
students of the Master SISE 2021/2022 of the University of Lyon 2 in which we are part of.

## Description of the application

We build an application coded in Python which is able to 


## Installation to access to the app on your computer

First, you have to download all of the files which are in this github.
Then, you will have to create a new environnement on your Anaconda.

Let's open a prompt Anaconda and go to the directory path containing the .yml file. There is an example just below.

    cd /Users/gwladyskerhoas/Downloads/FaceRecognition

Execute the following command to create your new environment in which you will have all the necessary libraries to use our application.
The file you have to use is the environment.yml.

    conda env create -f environment.yml

Once this environment has been created in Anaconda, open a terminal in it like this :

Capture d’écran 2022-03-10 à 23.25.20<img width="699" alt="image" src="https://user-images.githubusercontent.com/73121667/157765205-7ebf6b80-09f2-4e17-a4ce-e7e13456a9ac.png">

Go to the root of the main file used to run the application, namely the file runAll.py

    cd /Users/gwladyskerhoas/Downloads/FaceRecognition

And finally, to execute the application, run it like this :

    streamlit run runAll.py
