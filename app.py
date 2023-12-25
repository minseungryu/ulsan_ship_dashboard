# -*- coding:utf-8 -*-

import streamlit as st
st.set_page_config(layout="wide")
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from pred2 import predict_ship_waiting_time 
from home import about_service
from eda import ulsan_eda
from data import show_data
import warnings
warnings.filterwarnings('ignore')

def main():
    with st.sidebar:
        selected_menu = option_menu('Welcome', ["About Service", 'EDA', "Prediction", "Data"],
                            icons = ['search', 'clipboard-data', 'magic', 'database'], menu_icon="Geo", default_index=0) #icon : https://icons.getbootstrap.com/

    if selected_menu == "About Service":
        about_service()

    if selected_menu == "Prediction":
        predict_ship_waiting_time()  

    if selected_menu == 'EDA':
        ulsan_eda()

    elif selected_menu == "Data":
        show_data()

if __name__ == "__main__":
    main()