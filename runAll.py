#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:48:55 2022

@author: gwladyskerhoas
"""

import streamApp
import utils
import streamlit as st
PAGES = {
    "Détection de visage par webcam": streamApp,
    "Détection de visage par image": utils
}
st.sidebar.title('Reconnaissance faciale')
selection = st.sidebar.radio("Choisir le type de reconnaissance :", list(PAGES.keys()))
page = PAGES[selection]
page.main()