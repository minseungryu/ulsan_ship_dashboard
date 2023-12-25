# -*- coding:utf-8 -*-

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def about_service():
    # 홈 화면
    st.header('⛴️' + ' 울산항 선박 대기시간 예측 서비스')
    st.markdown('본 서비스는 **PORT-MIS**를 기반으로 **울산항 선박 대기시간**에 영향을 미치는 다양한 지표를 분석하여\n**분 단위 대기시간 예측**을 제공합니다.')
    # 이미지
    st.image("./data/ulsan.jpeg", width = 800) #use_column_width=True
    # st.markdown('여기에 소개쓰기, 두개 컬럼')

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('선박 대기시간, 왜 중요할까요?')
        st.text_area('① 항만 경쟁력 증대의 핵심 지표', '항구 운영 효율성 향상 및 선박 회전율 증가에 따른 물류 비용 절감 및 경쟁력 증대', height = 10)
        # st.markdown('(1) 항구 운영 효율성 향상 및 선박 회전율 증가에 따른  :blue[**물류 비용 절감 및 경쟁력 증대**]')
        st.text_area('② 선박 대기 비용 절감', '광양항 항만자동화 테스트베드 구축(KDI, 2022)의 예비 타당성 조사에서 선박 대기 관련 편익이 전체의 83%차지(약 214억)', height = 10)
        # st.markdown('(2) :blue[**선박 대기 중 발생하는 비용**] 절감  👉 선박 대기 관련 편익이 항만 전체의 83%차지(약 214억)')
        st.text_area('③ 대기 오염 배출 절감', '일반적으로 정박 시 발생하는 연료 소비량은 운항 시 발생하는 소비량의 20%로 산정 👉 선박 대기시간 감축 시, 선박 대기 간 발생하는 오염물질 절감 가능', height = 10)

    with col2:
        st.subheader('선박 입출항 프로세스')
        st.image("../data/process.png",use_column_width=True)