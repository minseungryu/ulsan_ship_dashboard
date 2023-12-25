import streamlit as st
import joblib
import numpy as np
import pandas as pd
import joblib
import os
os.environ['DYLD_LIBRARY_PATH'] = '/angela/local/opt/libomp/lib'

# 모델 불러오기
model = joblib.load("../models/model.pkl")

# 데이터 프레임 불러오기
df = pd.read_csv('../data/for_ship_model.csv')

# 예측 결과 출력 함수
def show_prediction(prediction):
    st.subheader('예측 결과')
    st.write(f'선박 대기시간 예측 결과: 약 {int(prediction)} 분')

# main text
st.subheader('🔎  선박 대기시간 예측 서비스 - 상세')
st.markdown('아래의 입력 정보를 차례로 채워주세요!')
st.markdown('그 후, 예측하기 버튼을 눌러주세요!')
st.markdown('---')

# 예측하기 버튼
if st.button('예측하기'):
    time_col, weather_col, ship_col = st.columns(3)

    with time_col:
        st.caption('입항 일시')
        ## 월, 일 시 input('ETA_Month', 'ETA_Day', 'ETA_Hour’)
        month = st.selectbox('입항 월: ', df['ETA_Month'].unique())
        day = st.selectbox('입항 일: ', df['ETA_Day'].unique())
        hour = st.selectbox('입항 시간: ', df['ETA_Hour'].unique())
        st.write(month, day, hour)

    with weather_col:
        st.caption('기상 정보')
        weather_columns = ['풍속', '풍향', 'GUST풍속', '현지기압', '습도', '기온', '수온', '최대파고', '유의파고', '평균파고', '파주기', '파향']
        for col in weather_columns:
            average_value = df[col].mean()
            min_val = min(df[col])
            max_val = max(df[col])
            st.slider(
                col,
                min_value=min_val, max_value=max_val, value=round(average_value, 2)
            )

    with ship_col:
        st.caption('서비스 시간')
        avg_service_time = df['선박_연평균_서비스시간'].mean()
        service_time = st.number_input('필요한 서비스 시간(분)', value=avg_service_time)

    st.markdown('---')

    st.caption('선박 정보')
    ship_info_columns = ['총톤수', '재화중량톤수', '선박_총길이', '선박_너비', '선박_만재흘수', '선박_깊이', '선박_길이1']
    for col in ship_info_columns:
        average_value = df[col].mean()
        number = st.number_input(f'{col} 정보를 입력하세요', value=int(average_value))
    
    st.markdown('---')

    ## 호출부호 인코딩값 매핑데이터
    ship_name = pd.read_csv('../data/ship_name_mapping.csv')
    selected_ship = st.selectbox('호출부호 선택', ship_name['호출부호'])
    # 선택한 호출부호에 대응하는 인코딩된 값을 출력
    encoded_ship = ship_name[ship_name['호출부호'] == selected_ship]['호출부호_encoded'].values[0]

    # 호출부호에 대응하는 선박_서비스시간_평균
    ship_service_time = df[df['호출부호_encoded'] == encoded_ship]['선박_연평균_서비스시간'].values[0]

    ## 선박용도 인코딩값 매핑
    usage_name = pd.read_csv('../data/usage_name_mapping.csv')
    selected_usage = st.selectbox('선박용도 선택', usage_name['선박용도'])
    encoded_usage = usage_name[usage_name['선박용도'] == selected_usage]['선박용도_encoded'].values[0]

    ## 계선장소 인코딩값 매핑(정박지 제외하지 않음)
    place_name = pd.read_csv('../data/place_name_mapping.csv')
    selected_place = st.selectbox('계선장소 선택', place_name['계선장소명'])
    encoded_place = place_name[place_name['계선장소명'] == selected_place]['계선장소명_encoded'].values[0]

    # 계선장소에 대응하는'시설연평균_재화중량톤수', '연평균_총입항건수'
    place_avg_ton = df[df['계선장소명_encoded'] == encoded_place]['시설연평균_재화중량톤수'].values[0]
    place_avg_cnt = df[df['계선장소명_encoded'] == encoded_place]['연평균_총입항건수'].values[0]

    date_data = [month, day, hour]

    ship_info_data = []
    for col in ship_info_columns:
        value = st.number_input(col)
        ship_info_data.append(value)

    weather_data = []
    for col in weather_columns:
        value = st.slider(col)
        weather_data.append(value)

    # 모델 입력 데이터 준비
    input_data = np.array(date_data + [service_time] + ship_info_data + weather_data + [place_avg_ton, place_avg_cnt, ship_service_time, encoded_ship, encoded_place, encoded_usage]).reshape(1, -1)

    # 모델 예측
    prediction = model.predict(input_data)

    # 예측 결과 출력
    show_prediction(prediction)
