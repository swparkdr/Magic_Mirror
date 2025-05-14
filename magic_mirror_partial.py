# ───────────────────── magic_mirror_app.py ─────────────────────
import random, re, os
import streamlit as st
import pandas as pd

# 1) 필수 설정
st.set_page_config(page_title="Magic Mirror")

# 2) CSV 로드 (없으면 더미 생성)
if not os.path.exists("personas_40_full.csv"):
    pd.DataFrame({
        "id": range(1, 41),
        "name": [f"사람{i}" for i in range(1, 41)],
        "story": ["당신과 비슷한 이야기를 가진 사람입니다."] * 40,
        "intro": ["짧은 소개"] * 40,
        "tags": ["성찰, 유연함, 현실적, 자기통제"] * 40,
        "gender": ["남성" if i % 2 else "여성" for i in range(40)],
    }).to_csv("personas_40_full.csv", index=False)

if not os.path.exists("tag_descriptions.csv"):
    pd.DataFrame({"tag": ["성찰", "유연함", "현실적", "자기통제", "균형감"]}).to_csv(
        "tag_descriptions.csv", index=False
    )

df_persona = pd.read_csv("personas_40_full.csv")
all_tags = sorted(pd.read_csv("tag_descriptions.csv")["tag"].unique().tolist())

# 3) 세션 초기화
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_gender" not in st.session_state:
    st.session_state.user_gender = "남성"
if "emotion" not in st.session_state:
    st.session_state.emotion = {"x": 5, "y": 5}
if "final_tags" not in st.session_state:
    st.session_state.final_tags = []
if "candidates" not in st.session_state:
    st.session_state.candidates = df_persona.sample(4).to_dict("records")
if "recommend_index" not in st.session_state:
    st.session_state.recommend_index = 0
if "reason_story" not in st.session_state:
    st.session_state.reason_story = ""

# 4) 간단 유틸
def rec_tags(x, y):
    if x <= 3 and y <= 3:
        return ["신중함", "감정 절제", "분석적", "객관적", "침착함"]
    if x >= 7 and y >= 7:
        return ["외향적", "공감", "유쾌함", "에너지", "감성적"]
    if x <= 3 and y >= 7:
        return ["내성적", "섬세함", "조율자", "감정이입", "사려 깊음"]
    if x >= 7 and y <= 3:
        return ["직진형", "열정", "추진력", "감정 표현", "감정적"]
    return ["균형감", "성찰", "유연함", "현실적", "자기통제"]


# 5) 페이지 정의
def landing():
    st.title("Magic Mirror")
    if st.button("시작하기"):
        st.session_state.page = "name"
        st.experimental_rerun()


def name_page():
    st.header("너는 누구니?")
    st.markdown("우선, 네 이름을 알고 싶어.\n\n너는 이름이 뭐야? 별명도 좋고, 뭐든 좋아!")
    name = st.text_input("이름", st.session_state.user_name)
    gender = st.radio("성별", ["남성", "여성"], index=0)
    if st.button("다음으로") and name.strip():
        st.session_state.user_name = name.strip()
        st.session_state.user_gender = gender
        st.session_state.page = "why"
        st.experimental_rerun()


def why_page():
    st.header(f"{st.session_state.user_name}, 나를 왜 찾았어?")
    for row in st.session_state.candidates:
        story = re.sub(r"사람\\d+", row["name"], row["story"])
        st.subheader(row["name"])
        st.write(row["intro"])
        st.write(story)
        if st.button(f"👉 이 사람이 가장 공감되요 ({row['name']})", key=row["name"]):
            st.session_state.reason_story = story
            st.session_state.page = "emotion"
            st.experimental_rerun()
    if st.button("다른 이야기 보기"):
        st.session_state.candidates = df_persona.sample(4).to_dict("records")
        st.experimental_rerun()


def emotion_page():
    st.header("너의 감정을 좌표로 그려볼까?")
    x = st.slider("자기표현 정도 (1=내향, 9=외향)", 1, 9, st.session_state.emotion["x"])
    y = st.slider("감정 방향성 (1=이성, 9=감성)", 1, 9, st.session_state.emotion["y"])
    st.session_state.emotion = {"x": x, "y": y}
    default_tags = rec_tags(x, y)
    selected = st.multiselect("너를 가장 잘 표현하는 태그를 골라줘", all_tags, default_tags)
    st.session_state.final_tags = selected
    if st.button("다음으로"):
        st.session_state.page = "recommend"
        st.experimental_rerun()


def recommend_page():
    st.header("당신과 감정적으로 닮은 사람")
    user_tags =_
