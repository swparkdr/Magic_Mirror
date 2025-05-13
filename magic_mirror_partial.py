
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Magic Mirror", layout="centered")

# 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "name_input"
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "reason_name" not in st.session_state:
    st.session_state.reason_name = ""
if "reason_story" not in st.session_state:
    st.session_state.reason_story = ""
if "selected_reason_tags" not in st.session_state:
    st.session_state.selected_reason_tags = []
if "emotion" not in st.session_state:
    st.session_state.emotion = {"x": 5, "y": 5}

# 감정 태그 표시용 함수
def get_random_tags(tag_str, k=4):
    tags = tag_str.split(", ")
    return random.sample(tags, min(k, len(tags)))

# 페이지 1: 이름 입력
def page_name_input():
    st.markdown("""
    ### 환영해! 여기는 Magic Mirror.  
    지금의 너와 어울리는 감정과 사람을 찾아주는 거울이야.

    너의 이름을 알려주면,  
    그 순간부터 이 거울은 너만의 이야기를 시작할 거야.
    """)
    name = st.text_input("너의 이름은?", value=st.session_state.user_name)
    if name.strip():
        st.session_state.user_name = name.strip()

    if st.button("다음으로"):
      if st.session_state.user_name:
        st.session_state.page = "why_here"
        st.experimental_rerun()

# 페이지 2: 공감되는 이야기 고르기
def page_why_here():
    st.markdown(f"""
    ## 안녕, {st.session_state.user_name}!
    너는 왜 나를 찾았을까?

    너무 급하지 않게, 차분히 너의 이야기를 듣고 싶어.  
    아래 사람들 중에서, 가장 마음이 이입되는 사람을 골라줄 수 있을까?
    """)

    df = pd.read_csv("personas_40_full.csv")
    candidates = df.sample(4)

    for _, row in candidates.iterrows():
        cleaned_story = row['story'].replace("사람", row['name'])
        label = f"""**{row['name']}** : {row['intro']}  
        {cleaned_story}"""
        ""
        if st.button(label, key=row['name']):
            st.session_state.reason_name = row["name"]
            st.session_state.reason_story = row["story"].replace("사람", row["name"])
            st.session_state.selected_reason_tags = get_random_tags(row["tags"])
            st.session_state.page = "emotion_input"
            st.experimental_rerun()
            st.markdown("---")
        if st.button("🔁 다른 이야기 보기"):
            st.experimental_rerun()

    st.markdown("---")
    if st.button("다른 이야기 보기"):
        st.experimental_rerun()

# 페이지 3: 감정 좌표 슬라이더
def page_emotion_input():
    st.markdown(f"""
    ### {st.session_state.user_name}, 너는  
    **{st.session_state.reason_name}**의 이야기에 공감했구나.

    그 이야기 속에서 너에게 와닿은 감정은 이런 키워드들이야:  
    `{'`, `'.join(st.session_state.selected_reason_tags)}`

    이제 너에 대해 조금 더 알려줘!  
    지금 너에게 중요한 감정의 위치는 어디일까?
    """)

    st.markdown("#### 감정 좌표 안내")
    st.markdown("""
    - **X축**: 자기표현의 정도 (1 = 내향적, 9 = 외향적)  
    - **Y축**: 감정 방향성 (1 = 이성적, 9 = 감성적)
    """)

    x = st.slider("자기표현 정도 (X)", 1, 9, st.session_state.emotion["x"])
    y = st.slider("감정 방향성 (Y)", 1, 9, st.session_state.emotion["y"])
    st.session_state.emotion = {"x": x, "y": y}

    st.markdown(f"📍 너의 감정 좌표: ({x}, {y})")

# 페이지 라우팅
if st.session_state.page == "name_input":
    page_name_input()
elif st.session_state.page == "why_here":
    page_why_here()
elif st.session_state.page == "emotion_input":
    page_emotion_input()
