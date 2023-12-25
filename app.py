# -*- coding:utf-8 -*-

import streamlit as st
st.set_page_config(layout="wide")
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
from pred2 import predict_ship_waiting_time 
from home import about_service
from eda import ulsan_eda
from data import show_data

import warnings
warnings.filterwarnings('ignore')

# Streamlit 사이드바 메뉴
# st.sidebar.title("Welcome!")
# selected_menu = st.sidebar.radio("Choose Service", ["About Service", "Ship Waiting Time Prediction"])

with st.sidebar:
    selected_menu = option_menu('Welcome', ["About Service", 'EDA', "Prediction", "Data"],
                           icons = ['search', 'clipboard-data', 'magic', 'database'], menu_icon="Geo", default_index=0) #icon : https://icons.getbootstrap.com/

if selected_menu == "About Service":
    about_service()

if selected_menu == "Prediction":
    predict_ship_waiting_time()  # pred.py의 함수 호출

if selected_menu == 'EDA':
    ulsan_eda()

elif selected_menu == "Data":
    show_data()