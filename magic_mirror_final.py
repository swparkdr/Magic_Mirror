import pandas as pd
import random
import streamlit as st

st.set_page_config(page_title="Magic Mirror", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "name_input"
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "reason" not in st.session_state:
    st.session_state.reason = ""
if "emotion" not in st.session_state:
    st.session_state.emotion = {"x": 5, "y": 5}
if "selected_tags" not in st.session_state:
    st.session_state.selected_tags = []
if "tag_options" not in st.session_state:
    st.session_state.tag_options = []

def go_to(page):
    st.session_state.page = page

def go_back(current_page):
    back_map = {
        "why_here": "name_input",
        "emotion_input": "why_here",
        "emotion_report": "emotion_input",
        "recommendation": "emotion_report"
    }
    go_to(back_map.get(current_page, "name_input"))

emotion_tags_pool = [
    "감정적", "이성적", "공감", "표현력", "내면적", "외향적", "리더십", "사려 깊음", "차분함", "열정",
    "호기심", "논리적", "감정 절제", "직관적", "분석적", "신중함", "침착함", "주도성", "조율자", "중재자",
    "유쾌함", "성찰", "통찰력", "따뜻함", "냉정함", "직진형", "에너지", "섬세함", "감정이입", "객관적",
    "감성적", "계획적", "현실적", "유연함", "자기통제", "긍정적", "안정감", "부드러움", "자기표현"
]

def page_name_input():
    st.title("Magic Mirror")
    st.markdown("### 안녕? 너는 이름이 뭐야?")
    name = st.text_input("이름을 입력해줘", value=st.session_state.user_name)
    if name.strip():
        st.session_state.user_name = name.strip()
        if st.button("다음으로"):
            go_to("why_here")

def page_why_here():
    st.markdown(f"### 안녕, {st.session_state.user_name}. 나를 왜 찾아왔어?")
    options = ["그냥, 재미로", "요즘 일이 잘 안풀리네.", "그냥 말하고 싶어서", "외로워"]
    choice = st.radio("이유를 선택해줘", options, index=None)
    if choice:
        st.session_state.reason = choice
        if st.button("다음으로 갈게"):
            go_to("emotion_input")
    if st.button("← 이전으로 돌아가기"):
        go_back("why_here")

def page_emotion_input():
    st.markdown("### 나는 너가 어떤 사람인지, 더 알고 싶어.")
    st.markdown("#### 감정의 위치를 슬라이더로 표현해줘.")
    x = st.slider("자기표현 정도 (X축)", 1, 9, st.session_state.emotion["x"])
    y = st.slider("감정 방향성 (Y축)", 1, 9, st.session_state.emotion["y"])
    st.session_state.emotion = {"x": x, "y": y}
    st.markdown(f"📍 현재 감정 좌표: ({x}, {y})")
    if st.button("감정 리포트 보기"):
        go_to("emotion_report")
    if st.button("← 이전으로 돌아가기"):
        go_back("emotion_input")

def page_emotion_report():
    st.markdown("## 감정 리포트")
    x, y = st.session_state.emotion["x"], st.session_state.emotion["y"]
    st.write(f"너는 감정적으로 x={x}, y={y}인 위치에 있어.")
    st.write("아래 태그들 중에서 너를 가장 잘 설명하는 단어들을 선택해줘.")

    if not st.session_state.tag_options:
        st.session_state.tag_options = random.sample(emotion_tags_pool, 20)

    selected = st.multiselect(
        "👇 아래에서 여러 개 골라줘!",
        st.session_state.tag_options,
        default=st.session_state.selected_tags,
        placeholder="해당되는 단어를 클릭해 선택해줘!",
        key="tag_selector"
    )
    st.session_state.selected_tags = selected

    if st.button("추천 결과 보기"):
        go_to("recommendation")
    if st.button("← 이전으로 돌아가기"):
        go_back("emotion_report")

def page_recommendation():
    st.markdown("## 당신과 감정적으로 닮은 사람들")
    user_tags = set(st.session_state.selected_tags)
    df = pd.read_csv("personas_40_full.csv")
    recommendations = []
    for _, row in df.iterrows():
        persona_tags = set(str(row["tags"]).split(", "))
        matched_tags = user_tags & persona_tags
        score = len(matched_tags)
        if score > 0:
            recommendations.append({
                "name": row["name"],
                "score": score,
                "matched_tags": ", ".join(matched_tags),
                "style": row["style"],
                "tagline": row["tagline"]
            })
    sorted_results = sorted(recommendations, key=lambda x: x["score"], reverse=True)
    for rec in sorted_results[:5]:
        st.markdown(f"### {rec['name']} - {rec['tagline']}")
        st.write(f"**스타일:** {rec['style']}")
        st.write(f"**공통 태그:** {rec['matched_tags']}")
        st.markdown("---")
    if st.button("← 이전으로 돌아가기"):
        go_back("recommendation")

page = st.session_state.page
if page == "name_input":
    page_name_input()
elif page == "why_here":
    page_why_here()
elif page == "emotion_input":
    page_emotion_input()
elif page == "emotion_report":
    page_emotion_report()
elif page == "recommendation":
    page_recommendation()
