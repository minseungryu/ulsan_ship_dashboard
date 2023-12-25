import streamlit as st
import numpy as np
import pandas as pd

def show_data():
    df = pd.read_csv('./data/for_ship_model.csv')
    st.subheader('Filtering Options')
    st.markdown('울산항의 3년 데이터(2020~2022)를 확인해보세요.')
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.multiselect('Year (복수 선택 가능)', df['ETA_Year'].unique())
    with col2:
        month = st.multiselect('Month (복수 선택 가능)', df['ETA_Month'].unique())
    with col3:
        min_day = df['ETA_Day'].min()
        max_day = df['ETA_Day'].max()
        day = st.select_slider('Day', options= range(min_day, max_day +1), value=(min_day, max_day))

        min_hour = df['ETA_Hour'].min()
        max_hour = df['ETA_Hour'].max()
        hour = st.select_slider('Hour', options= range(min_hour, max_hour +1), value=(min_hour, max_hour))

    # filtered_df = df[(df['ETA_Year'] == year) & (df['ETA_Month'] == month) & (df['ETA_Day']== day)] 틀린코드

    if year:
        df = df[df['ETA_Year'].isin(year)]
    if month:
        df = df[df['ETA_Month'].isin(month)]
    df = df[(df['ETA_Day'] >= day[0]) & (df['ETA_Day'] <= day[1]) & (df['ETA_Hour'] >= hour[0]) & (df['ETA_Hour'] <= hour[1])]

    st.divider()
    # st.subheader(f'{", ".join(map(str, year))}년 {", ".join(map(str, month))}월 {day[0]}일부터 {day[1]}일까지')
    # st.write(df)
    
    if not year and not month and day[0] == min_day and day[1] == max_day:
        st.subheader('울산항의 3개년 데이터입니다.')
        st.write(df)
    elif not month and day[0] == min_day and day[1] == max_day:
        st.subheader(f'울산항의 {", ".join(map(str, year))}년 데이터입니다.')
        st.write(df)
    else:
        st.subheader(f'울산항의 {", ".join(map(str, year))}년 {", ".join(map(str, month))}월 {day[0]}일부터 {day[1]}일까지 데이터입니다.')
        st.write(df)


