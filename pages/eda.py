import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from scipy.stats import ks_2samp
from itertools import combinations
from sklearn.cluster import KMeans
import plotly.figure_factory as ff

def ulsan_eda():
    df = pd.read_csv('./data/울산_전처리_ver7.csv')
    color_scale = px.colors.qualitative.Pastel

    st.header('울산항 3개년 입출항 현황을 확인해보세요')
    tab1, tab2, tab3 = st.tabs(["울산항 대기발생 비율", "선박용도 기준", "계선장소 기준"])
    with tab1:
        st.subheader('울산항 대기발생 비율과 선박용도별 현황')
        st.markdown('**▶︎ 울산항 전체 입항 건 중 20%의 대기 발생**')
        # '접안_대기시간_분' 열이 0인 데이터와 0이 아닌 데이터의 갯수 계산
        count_zero = (df['접안_대기시간_분'] == 0).sum()
        count_non_zero = (df['접안_대기시간_분'] != 0).sum()
        # 데이터 프레임 생성
        data = {'Category': ['대기발생 없음', '대기발생'], 'Count': [count_zero, count_non_zero]}
        df_plot = pd.DataFrame(data)

        # Plotly 그래프 그리기
        fig = px.bar(df_plot, x='Category', y='Count',
            color='Category',  title='접안 대기발생 유무',
            color_discrete_sequence=px.colors.qualitative.Pastel, 
        )
        fig.update_xaxes(title_text='접안 대기발생')
        st.plotly_chart(fig)

    with tab2:
        st.subheader('선박용도별 대기 발생 비율')
        st.markdown('**▶︎ 액체화물선의 대기 발생 비율과 시간이 높음** : 케미컬 운반선, 석유제품 운반선, LPG 운반선 등')
        filtered_df = df.groupby('선박용도').filter(lambda x : len(x) >= 100)
        usage_waiting_rate = filtered_df.groupby('선박용도')['접안_대기시간_분'].apply(lambda x : (x > 0).sum() / len(x)).reset_index()
        usage_waiting_rate.columns = ['선박용도', '접안대기시간_발생_비율']
        usage_waiting_rate = usage_waiting_rate.sort_values(by = '접안대기시간_발생_비율', ascending = True)

        fig = px.bar(usage_waiting_rate, x='접안대기시간_발생_비율', y='선박용도', orientation='h', 
                     title='선박용도별 접안대기시간 발생 비율 (입항횟수 100회 이상)',
                    color= usage_waiting_rate.index, color_continuous_scale=color_scale)

        fig.update_traces(texttemplate='%{x:.2%}', textposition='outside')
        fig.update_xaxes(title_text='접안대기시간 발생 비율')
        fig.update_yaxes(title_text='선박용도', categoryorder='total ascending')
        fig.update_coloraxes(showscale=False)
        fig.update_layout(width=800, height=600)
        st.plotly_chart(fig)

        st.divider()
        filtered_df = df.groupby('선박용도').filter(lambda x: len(x) >= 100)
        average_wait_time_by_purpose = filtered_df.groupby('선박용도')['접안_대기시간_분'].mean().reset_index()
        average_wait_time_by_purpose = average_wait_time_by_purpose.sort_values(by='접안_대기시간_분', ascending=False)
        fig = px.bar(
            average_wait_time_by_purpose,
            x='접안_대기시간_분',
            y='선박용도',
            orientation='h',
            title='선박용도별 접안 대기시간 평균(입항횟수 100회 이상)',
            color='선박용도', color_continuous_scale=color_scale,  
            text=average_wait_time_by_purpose['접안_대기시간_분'].apply(lambda x: f'{x:.2f}'),  # 텍스트 형식 지정
        )
        fig.update_xaxes(title_text='평균 접안대기시간')
        fig.update_yaxes(title_text='선박용도')
        fig.update_coloraxes(showscale=False)
        fig.update_layout(width=800, height=600)
        st.plotly_chart(fig)

        st.divider()
        average_waiting_rate_by_purpose = df.groupby('선박용도')['대기율'].agg(['mean', 'count']).reset_index()
        average_waiting_rate_by_purpose = average_waiting_rate_by_purpose[average_waiting_rate_by_purpose['count'] >= 100]
        average_waiting_rate_by_purpose = average_waiting_rate_by_purpose.sort_values(by='mean', ascending=False)
        fig = px.bar(average_waiting_rate_by_purpose, x = 'mean', y = '선박용도', orientation = 'h',
                    title = '선박용도별 대기율 평균 및 데이터 수(입항횟수 100회 이상)', color = '선박용도', color_continuous_scale = px.colors.qualitative.Pastel)
        fig.update_traces(texttemplate='%{x:.2f}', textposition = 'outside')
        fig.update_xaxes(title_text = '평균 대기율')
        fig.update_yaxes(title_text = '선박용도', categoryorder = 'total ascending')
        fig.update_coloraxes(showscale=False)
        fig.update_layout(width=800, height=600)
        st.plotly_chart(fig)

    with tab3:
        st.subheader('계선장소별 대기 발생 비율과 건 수')
        st.markdown('👇 스크롤을 내려 **대기 발생 비율이 높은 부두의 특성**을 확인하세요.')
        filtered_df = df[~df['계선장소명'].str.contains('정박')]
        waiting_rate_by_location = filtered_df.groupby('계선장소명')['대기율'].agg(['mean', 'count']).reset_index()
        waiting_rate_by_location = waiting_rate_by_location.sort_values(by='mean', ascending=False)
        top_10_locations = waiting_rate_by_location.head(10)
        fig = px.bar(top_10_locations, x = 'mean', y = '계선장소명', orientation = 'h', 
                    title = '상위 10개의 계선장소별 대기율 평균과 데이터 수', color = '계선장소명', color_continuous_scale=color_scale)
        fig.update_traces(text = top_10_locations['count'])
        fig.update_xaxes(title_text='대기율의 평균')
        fig.update_yaxes(title_text='계선장소명', categoryorder='total ascending')
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig)
        st.divider()
        st.markdown('▶︎ 상위 3개의 부두의 주요 취급 화물이 액체화물(연료, 화학물질 등)')
        st.image('../data/budu.png', width=500)
        
