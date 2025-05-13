import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(page_title="Magic Mirror", layout="centered")

# 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "name_input"
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_gender" not in st.session_state:
    st.session_state.user_gender = ""
if "preference" not in st.session_state:
    st.session_state.preference = ""
if "reason_name" not in st.session_state:
    st.session_state.reason_name = ""
if "reason_story" not in st.session_state:
    st.session_state.reason_story = ""
if "selected_reason_tags" not in st.session_state:
    st.session_state.selected_reason_tags = []
if "emotion" not in st.session_state:
    st.session_state.emotion = {"x": 5, "y": 5}
if "final_tags" not in st.session_state:
    st.session_state.final_tags = []
if "recommend_index" not in st.session_state:
    st.session_state.recommend_index = 0
if "candidates" not in st.session_state:
    df = pd.read_csv("personas_40_full.csv")
    st.session_state.candidates = df.sample(4).to_dict("records")

def get_tags_from_emotion(x, y):
    if x <= 3 and y <= 3:
        return ["신중함", "감정 절제", "분석적", "객관적", "침착함"]
    elif x >= 7 and y >= 7:
        return ["외향적", "공감", "유쾌함", "에너지", "감성적"]
    elif x <= 3 and y >= 7:
        return ["내성적", "섬세함", "조율자", "감정이입", "사려 깊음"]
    elif x >= 7 and y <= 3:
        return ["직진형", "열정", "추진력", "감정 표현", "감정적"]
    else:
        return ["균형감", "성찰", "유연함", "현실적", "자기통제"]

# 페이지 1
def page_name_input():
    st.markdown("### 안녕? 너는 이름이 뭐야?")
    name = st.text_input("이름", value=st.session_state.user_name)
    gender = st.radio("성별을 선택해줘", ["남성", "여성"], index=0)
    if name.strip():
        st.session_state.user_name = name.strip()
        st.session_state.user_gender = gender
    if st.button("다음으로"):
        st.session_state.page = "why_here"
        st.experimental_rerun()

# 페이지 2
def page_why_here():
    st.markdown(f"## {st.session_state.user_name}, 나를 왜 찾았어?")
    st.markdown("아래 사람들 중에서 가장 공감되는 이야기를 골라줄 수 있을까?")
    selected_name = None

    for row in st.session_state.candidates:
        story = re.sub(r"사람\\d+", row["name"], row["story"])
        st.markdown(f"### {row['name']}")
        st.markdown(f"**{row['intro']}**")
        st.markdown(story)
        if st.button(f"👉 이 사람이 가장 공감되요 ({row['name']})", key=row["name"]):
            st.session_state.reason_name = row["name"]
            st.session_state.reason_story = story
            st.session_state.selected_reason_tags = random.sample(row["tags"].split(", "), 4)
            st.session_state.page = "emotion_input"
            st.experimental_rerun()

    st.markdown("---")
    if st.button("🔁 다른 스토리 볼래요"):
        df = pd.read_csv("personas_40_full.csv")
        st.session_state.candidates = df.sample(4).to_dict("records")
        st.experimental_rerun()

# 페이지 3
def page_emotion_input():
    st.markdown("### 너에 대해 조금 더 알려줘!")

    # 감정 좌표 설명 추가
    st.markdown("#### 왜 감정 좌표를 묻는 걸까?")
    st.markdown("""
사람의 감정은 단순히 "기분"이나 "성격"으로 나뉘지 않아.  
우리는 감정을 어떻게 표현하고, 어떤 방향으로 흐르게 하느냐에 따라  
삶을 경험하고, 사람을 이해하게 되지.

이 좌표는 두 가지 축으로 구성돼 있어:

- **X축은 자기표현의 정도**야.  
  감정을 밖으로 얼마나 드러내는지, 사람들과 어떻게 연결되는지를 말해.

- **Y축은 감정의 방향성**이야.  
  너의 감정이 이성적으로 흐르는지, 감성적으로 반응하는지를 나타내지.

이 좌표는 너를 한 문장으로 규정하려는 게 아니야.  
오히려 지금 이 순간의 너,  
그리고 관계 속에서 너의 감정이 어떤 결을 가지고 있는지를  
함께 바라보는 시작점이야.

지금의 너는 어디쯤에 있을까?
""")

    # 좌표 입력
    x = st.slider("자기표현 정도 (X축)", 1, 9, st.session_state.emotion["x"])
    y = st.slider("감정 방향성 (Y축)", 1, 9, st.session_state.emotion["y"])
    st.session_state.emotion = {"x": x, "y": y}

    # 태그 추천 및 선택
    recommended = get_tags_from_emotion(x, y)
    tag_df = pd.read_csv("tag_descriptions.csv")
    all_tags = sorted(tag_df["tag"].unique().tolist())
    valid_defaults = [tag for tag in recommended if tag in all_tags]

    st.markdown("#### 추천된 감정 태그:")
    selected = st.multiselect("👇 너를 가장 잘 표현하는 태그를 골라줘", all_tags, default=valid_defaults)

    if selected:
        st.session_state.final_tags = selected

    if st.button("다음으로"):
        st.session_state.page = "orientation"
        st.experimental_rerun()

# 페이지 4
def page_orientation():
    st.markdown("### 그런데 먼저 물어보고 싶은 게 있어.")
    pref = st.radio("어떤 유형의 만남을 원해?", ["이성애", "동성애", "양성애"])
    if st.button("추천 계속하기"):
        st.session_state.preference = pref
        st.session_state.page = "recommendation"
        st.experimental_rerun()

# 페이지 5
def page_recommendation():
    df = pd.read_csv("personas_40_full.csv")
    user_tags = set(st.session_state.final_tags)
    gender = st.session_state.user_gender
    pref = st.session_state.preference

    if pref == "이성애":
        filtered = df[df["gender"] != gender]
    elif pref == "동성애":
        filtered = df[df["gender"] == gender]
    else:
        filtered = df

    def match_score(row):
        persona_tags = set(row["tags"].split(", "))
        return len(user_tags & persona_tags)

    filtered["score"] = filtered.apply(match_score, axis=1)
    top_matches = filtered.sort_values(by="score", ascending=False).reset_index(drop=True)

    idx = st.session_state.recommend_index
    if idx >= len(top_matches):
        st.warning("더 이상 추천할 사람이 없어요 😢")
        return

    match = top_matches.iloc[idx]

    st.markdown("## 💫 당신과 감정적으로 닮은 사람")
    st.markdown(f"### {match['name']}")
    st.markdown(f"**당신이 공감했던 이야기**: {st.session_state.reason_story}")
    st.markdown(f"**당신의 감정 키워드**: `{'`, `'.join(st.session_state.final_tags)}`")
    st.markdown(f"**감정 좌표**: ({st.session_state.emotion['x']}, {st.session_state.emotion['y']})")

    if st.button("이 사람이 더 궁금해요!"):
        st.success("이 사람과의 연결을 준비하고 있어요... (계속 개발 중!)")

    if st.button("이 사람은 나와 맞지 않는 것 같아요. 다른 사람은 없을까요?"):
        st.session_state.recommend_index += 1
        st.experimental_rerun()

# 라우팅
if st.session_state.page == "name_input":
    page_name_input()
elif st.session_state.page == "why_here":
    page_why_here()
elif st.session_state.page == "emotion_input":
    page_emotion_input()
elif st.session_state.page == "orientation":
    page_orientation()
elif st.session_state.page == "recommendation":
    page_recommendation()
