import streamlit as st
import joblib
import numpy as np
import pandas as pd
import joblib
import os
os.environ['DYLD_LIBRARY_PATH'] = '/angela/local/opt/libomp/lib'

def predict_ship_waiting_time():
    # 모델 불러오기
    model = joblib.load("./models/model.pkl")

    # 데이터 프레임 불러오기
    df = pd.read_csv('./data/for_ship_model.csv')

    # main text
    st.header('🔎  선박 대기시간 예측 서비스 - 상세') 
    st.markdown('아래의 입력 정보를 차례로 채우고 사이드바의 "예측하기" 버튼을 클릭하세요!')
    st.markdown('입항 예정 일시와 양적하 소요시간, 접안 예정 선석을 선택하신 후, 기상 상태와 선박 정보를 입력합니다.')
    st.markdown('---')

    container1 = st.container()
    with container1:
        st.subheader('⏰ 입항 일시')
        month_col, day_col, hour_col = st.columns(3)
        with month_col:
            month = st.selectbox('월(Month): ', df['ETA_Month'].unique())
        with day_col:
            day = st.selectbox('일(Day): ', df['ETA_Day'].unique())
        with hour_col:
            hour = st.selectbox('시간(Hour): ', df['ETA_Hour'].unique())
        date_data = [month, day, hour]

    st.divider()
    container2 = st.container()
    with container2:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('서비스(양적하) 소요 시간')
            avg_service_time = df['선박_연평균_서비스시간'].mean()
            service_time = st.number_input('필요한 서비스 시간(분)', value= avg_service_time)
        with col2:
            st.subheader('접안 예정 부두(계선장소)')
            place_name = pd.read_csv('./data/place_name_mapping.csv')
            selected_place = st.selectbox('계선장소 선택', place_name['계선장소명'])
            encoded_place = place_name[place_name['계선장소명'] == selected_place]['계선장소명_encoded'].values[0]

            place_avg_ton = df[df['계선장소명_encoded'] == encoded_place]['시설연평균_재화중량톤수'].values[0]
            st.markdown(f'▶︎ {selected_place} :green[**연평균 재화중량톤수**]는 **{round(place_avg_ton, 2)}톤** 이며,')

            place_avg_cnt = df[df['계선장소명_encoded'] == encoded_place]['연평균_총입항건수'].values[0]
            st.markdown(f'▶︎ 해당 선석의 :green[**연평균 총 입항 건 수**]는, **{int(place_avg_cnt)}건** 입니다.')

    st.divider()
    container3 = st.container()
    with container3:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('🌊 기상 상태')
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
                weather_data.append(round(weather_value, 2))
                st.write(weather_value)
        
        with col2:
            st.subheader('🚢 선박 정보')
            st.markdown('① 호출부호(선박 고유 ID)를 선택하세요')
            ## 호출부호 인코딩값 매핑데이터
            ship_name = pd.read_csv('./data/ship_name_mapping.csv')
            selected_ship = st.selectbox('', ship_name['호출부호'])
            encoded_ship = ship_name[ship_name['호출부호'] == selected_ship]['호출부호_encoded'].values[0]
            ship_service_time = df[df['호출부호_encoded'] == encoded_ship]['선박_연평균_서비스시간'].values[0]
            # st.write(f'{selected_ship} 선박의 연평균 서비스 시간은 {int(ship_service_time)}분 입니다.')
            st.markdown(f'👉 {selected_ship} 선박의 :blue[**연평균 서비스 시간**]은 **{int(ship_service_time)}분** 입니다.')
            st.markdown('---')


            ## 선박용도 인코딩값 매핑
            st.markdown('② 선박용도를 선택하세요')
            usage_name = pd.read_csv('./data/usage_name_mapping.csv')
            selected_usage = st.selectbox('', usage_name['선박용도'])
            encoded_usage = usage_name[usage_name['선박용도'] == selected_usage]['선박용도_encoded'].values[0]

            st.markdown('---')
            st.markdown('③ 선박제원정보를 입력하세요')
            ship_info_data = []
            ship_info_columns = ['총톤수', '재화중량톤수', '선박_총길이', '선박_너비', '선박_만재흘수', '선박_깊이', '선박_길이1']
            for col in ship_info_columns:
                average_value = df[col].mean()
                number = st.number_input(f'{col}', value = int(average_value))
                ship_info_data.append(number)

    st.divider()

    # 예측하기 버튼
    if st.sidebar.button('예측하기'):
        # 모델 입력 데이터 준비
        input_data = np.array(date_data + [service_time] + ship_info_data + weather_data + [place_avg_ton, place_avg_cnt, ship_service_time, encoded_ship, encoded_place, encoded_usage]).reshape(1, -1)

        # 모델 예측
        prediction = model.predict(input_data)

        # 예측 결과 출력
        st.sidebar.subheader(f'👉 선박 대기 :red[{int(prediction[0])}]분 예상')
