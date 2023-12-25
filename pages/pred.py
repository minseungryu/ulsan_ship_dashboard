import streamlit as st
import joblib
import numpy as np
import pandas as pd
import joblib
import os
os.environ['DYLD_LIBRARY_PATH'] = '/angela/local/opt/libomp/lib'

def predict_ship_waiting_time():
    # 모델 불러오기
    model = joblib.load("../models/model.pkl")

    # 데이터 프레임 불러오기
    df = pd.read_csv('../data/for_ship_model.csv')

    # main text
    st.subheader('🔎  선박 대기시간 예측 서비스 - 상세') 
    st.markdown('아래의 입력 정보를 차례로 채우고 페이지 하단의 "예측하기" 버튼을 클릭하세요!')
    st.markdown('---')

    time_col, weather_col, ship_col = st.columns(3)

    with time_col:
        st.caption('입항 일시')
        ## 월, 일 시 input('ETA_Month', 'ETA_Day', 'ETA_Hour’)
        month = st.selectbox('입항 월: ', df['ETA_Month'].unique())
        day = st.selectbox('입항 일: ', df['ETA_Day'].unique())
        hour = st.selectbox('입항 시간: ', df['ETA_Hour'].unique())
        date_data = [month, day, hour]

        st.markdown('---')
        st.caption('서비스 시간')
        avg_service_time = df['선박_연평균_서비스시간'].mean()
        service_time = st.number_input('필요한 서비스 시간(분)', value= avg_service_time)

    with weather_col:
        st.caption('기상 정보')

        # # 풍속 >> 하나하나 지정하고 설명 추가하는 것 나중에
        # average_speed = df['풍속'].mean()
        # wind_sp = st.slider(
        #     '풍속',
        #     min_value=min(df['풍속']), max_value=max(df['풍속']), value= round(average_speed, 2))
        # #st.write('풍속:', wind_sp)

        # # 풍향
        # average_direction = df['풍향'].mean()
        # wind_dr = st.slider(
        #     '풍향',
        #     min_value=min(df['풍향']), max_value=max(df['풍향']), value= round(average_direction, 2))

        weather_data = []
        weather_columns = ['풍속', '풍향', 'GUST풍속', '현지기압', '습도', '기온', '수온', '최대파고', '유의파고', '평균파고', '파주기', '파향']
        for col in weather_columns:
            average_value = df[col].mean()
            min_val = min(df[col])
            max_val = max(df[col])
            weather_value = st.slider(
                col,
                min_value = min_val, max_value = max_val, value = round(average_value, 2)
            )
            weather_data.append(weather_value)
    

    with ship_col:
        st.caption('선박 정보')
        ship_info_data = []
        ship_info_columns = ['총톤수', '재화중량톤수', '선박_총길이', '선박_너비', '선박_만재흘수', '선박_깊이', '선박_길이1']
        for col in ship_info_columns:
            average_value = df[col].mean()
            number = st.number_input(f'{col}', value = int(average_value))
            ship_info_data.append(number)
        
        # for col in ship_info_columns:
        #     value = st.number_input(col)
        #     ship_info_data.append(value)
        st.markdown('---')

        ## 호출부호 인코딩값 매핑데이터
        ship_name = pd.read_csv('../data/ship_name_mapping.csv')
        selected_ship = st.selectbox('호출부호 선택', ship_name['호출부호'])
        # 선택한 호출부호에 대응하는 인코딩된 값을 출력
        encoded_ship = ship_name[ship_name['호출부호'] == selected_ship]['호출부호_encoded'].values[0]
        # st.write(f'선택한 호출부호: {selected_ship}')
        # st.write(f'호출부호_인코딩값: {encoded_ship}')

        # 호출부호에 대응하는 선박_서비스시간_평균
        ship_service_time = df[df['호출부호_encoded'] == encoded_ship]['선박_연평균_서비스시간'].values[0]
        st.write(f'{selected_ship} 선박의 연평균 서비스 시간: {int(ship_service_time)}분')

        ## 선박용도 인코딩값 매핑
        usage_name = pd.read_csv('../data/usage_name_mapping.csv')
        selected_usage = st.selectbox('선박용도 선택', usage_name['선박용도'])
        encoded_usage = usage_name[usage_name['선박용도'] == selected_usage]['선박용도_encoded'].values[0]
        # st.write(f'선택한 선박용도: ', selected_usage)
        # st.write(f'선박용도명의 인코딩값: ', encoded_usage)

        ## 계선장소 인코딩값 매핑(정박지 제외하지 않음)
        place_name = pd.read_csv('../data/place_name_mapping.csv')
        selected_place = st.selectbox('계선장소 선택', place_name['계선장소명'])
        encoded_place = place_name[place_name['계선장소명'] == selected_place]['계선장소명_encoded'].values[0]
        # st.write(f'선택한 계선장소: ', selected_place)
        # st.write(f'계선장소명의 인코딩값: ', encoded_place)

        # 계선장소에 대응하는'시설연평균_재화중량톤수', '연평균_총입항건수'
        place_avg_ton = df[df['계선장소명_encoded'] == encoded_place]['시설연평균_재화중량톤수'].values[0]
        st.write(f'{selected_place} 연평균 재화중량톤수: ', round(place_avg_ton, 2), '톤/연')

        place_avg_cnt = df[df['계선장소명_encoded'] == encoded_place]['연평균_총입항건수'].values[0]
        st.write('선석 연평균총입항건수: ', int(place_avg_cnt), '건/연')

    # date_data= [month, day, hour]
    # ship_info_data = []
    # for col in ship_info_columns:
    #     value = st.number_input(col)
    #     ship_info_data.append(value)

    # weather_data = []
    # for col in weather_columns:
    #     value = st.slider(col)
    #     weather_data.append(value)

    # if st.button('예측하기'):
    # # 모델 입력 데이터 준비
    #     input_data = np.array(date_data + [service_time] + ship_info_data + weather_data + [place_avg_ton, place_avg_cnt, ship_service_time, encoded_ship, encoded_place, encoded_usage]).reshape(1, -1)

    #     # 모델 예측
    #     prediction = model.predict(input_data)

    #     # 예측 결과 출력
    #     st.subheader('예측 결과')
    #     st.write(f'선박 대기시간 예측 결과: 약 {int(prediction[0])} 분')

    if st.button('예측하기'):
        # 모델 입력 데이터 준비
        input_data = np.array(date_data + [service_time] + ship_info_data + weather_data + [place_avg_ton, place_avg_cnt, ship_service_time, encoded_ship, encoded_place, encoded_usage]).reshape(1, -1)

        # 모델 예측
        prediction = model.predict(input_data)

        # 예측 결과 출력
        st.subheader('예측 결과')
        st.write(f'선박 대기시간 예측 결과: 약 {int(prediction[0])} 분')
