# Facial_Recognition_with_Opencv and Streamlit

This project is about facial recognition and identification on WEBCAM videos. More precisely, the aim of this project is to recognize automatically 
students of the Master SISE 2021/2022 of the University of Lyon 2 in which we are part of .

## Description of the application

We build an interactive application coded in Streamlit (Python) which is able to drive the WEBCAM from a computer. In real time, the application detects the people present on the video, and more importantly, those who are part of the class of SISE 2021/2022. The application is also able to indicate the emotion that animates them (joy, fear, sadness, surprise, etc.), indicate their gender and their age. For those who are not part of the sise promotion the name 'unknown' is displayed. The list of people appearing in the video is saved in a text file. 

In our application, you have the choose to identify the name of the people, their age, their gender... and each you change the fonctionnality detection, a video is recorded and all of these videos are saved in a dedicated folder.


## Installation to access to the app on your computer

First, you have to download all of the files which are in this github.
Then, you will have to create a new environnement on your Anaconda.

Let's open a prompt Anaconda and go to the directory path containing the .yml file. There is an example just below.

    cd /Users/gwladyskerhoas/Downloads/FaceRecognition

Execute the following command to create your new environment in which you will have all the necessary libraries to use our application.
The file you have to use is the environment.yml.

    conda env create -f environment.yml

Once this environment has been created in Anaconda, open a terminal in it like this :

<img width="699" alt="image" src="https://user-images.githubusercontent.com/73121667/157765205-7ebf6b80-09f2-4e17-a4ce-e7e13456a9ac.png">

Go to the root of the main file used to run the application, namely the file runAll.py

    cd /Users/gwladyskerhoas/Downloads/FaceRecognition

And finally, to execute the application, run it like this :

    streamlit run runAll.py
    
## Overview of our application

Here is some screenshot to overview the app.

![image](https://user-images.githubusercontent.com/73121667/157770743-bab5a36c-239c-4a0b-9ffd-137195c75a85.png)

![image](https://user-images.githubusercontent.com/73121667/157770836-a97ee5b1-59a7-4d12-9691-cdfc9759757e.png)
