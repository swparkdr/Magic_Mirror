import streamlit as st
import pandas as pd
import math

# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "page_name"
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "nickname" not in st.session_state:
    st.session_state.nickname = ""
if "emotion_x" not in st.session_state:
    st.session_state.emotion_x = 5
if "emotion_y" not in st.session_state:
    st.session_state.emotion_y = 5
if "selected_story" not in st.session_state:
    st.session_state.selected_story = {}

# 페이지 1: 이름 입력
def page_name():
    st.title("✨ Magic Mirror에 오신 걸 환영해요!")
    st.write("당신의 이름을 알려주세요.")

    st.session_state.user_name = st.text_input("이름", value=st.session_state.user_name)

    if st.button("다음"):
        if st.session_state.user_name.strip() != "":
            st.session_state.page = "page_nickname"
        else:
            st.warning("이름을 입력해주세요!")

# 페이지 2: 애칭 설정
def page_nickname():
    st.title(f"반가워요, {st.session_state.user_name}님!")
    st.write("✨ 이제 제가 당신을 어떻게 부르면 좋을까요?")
    
    st.session_state.nickname = st.text_input("저는 당신을 이렇게 부를게요", value=st.session_state.nickname)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("이전"):
            st.session_state.page = "page_name"
    with col2:
        if st.button("다음"):
            if st.session_state.nickname.strip() != "":
                st.session_state.page = "page_emotion"
            else:
                st.warning("저에게 부를 이름을 입력해주세요!")

# 페이지 3: 감정 좌표 선택
def page_emotion():
    st.title(f"{st.session_state.nickname}님, 지금 당신의 감정은 어떤가요?")
    st.write("당신의 감정을 감정 좌표계로 표현해주세요.")

    st.session_state.emotion_x = st.slider("감정 방향성 (1 = 이성적, 9 = 감성적)", 1, 9, st.session_state.emotion_x)
    st.session_state.emotion_y = st.slider("감정 에너지 (1 = 차분함, 9 = 에너제틱함)", 1, 9, st.session_state.emotion_y)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("이전"):
            st.session_state.page = "page_nickname"
    with col2:
        if st.button("다음"):
            st.session_state.page = "page_story"

# 페이지 4: 감정 기반 스토리 추천
def page_story():
    st.title("💌 당신을 위한 이야기")

    try:
        df = pd.read_csv("story.csv")
        # 좌표 거리 기반으로 가장 가까운 스토리 추천
        def dist(row):
            return math.sqrt((row["emotion_x"] - st.session_state.emotion_x)**2 + (row["emotion_y"] - st.session_state.emotion_y)**2)

        df["distance"] = df.apply(dist, axis=1)
        best_story = df.sort_values(by="distance").iloc[0]

        st.session_state.selected_story = best_story

        st.subheader(best_story["story_title"])
        st.write(best_story["story_text"])

    except Exception as e:
        st.error("스토리를 불러올 수 없습니다. story.csv 파일을 확인해주세요.")
        st.exception(e)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("이전"):
            st.session_state.page = "page_emotion"
    with col2:
        if st.button("다음"):
            st.session_state.page = "page_match"

# 페이지 5: 감정 기반 페르소나 매칭 (샘플용 구성)
def page_match():
    st.title("🧭 당신과 어울리는 페르소나")
    st.write(f"감정 좌표 ({st.session_state.emotion_x}, {st.session_state.emotion_y})를 기반으로 매칭 중...")

    # TODO: personas.csv 로딩 + 거리 기반 추천 구성
    st.info("매칭 알고리즘은 아직 구성 중입니다. 곧 연결될 예정이에요.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("이전"):
            st.session_state.page = "page_story"
    with col2:
        if st.button("다음"):
            st.session_state.page = "page_result"

# 페이지 6: 최종 요약
def page_result():
    st.title("🌟 당신만의 감정 리포트")

    st.write(f"이름: {st.session_state.user_name}")
    st.write(f"호칭: {st.session_state.nickname}")
    st.write(f"감정 좌표: ({st.session_state.emotion_x}, {st.session_state.emotion_y})")

    if st.session_state.selected_story:
        st.write("당신에게 추천된 이야기:")
        st.subheader(st.session_state.selected_story["story_title"])
        st.write(st.session_state.selected_story["story_text"])

    if st.button("처음으로"):
        st.session_state.page = "page_name"

# 페이지 라우팅
pages = {
    "page_name": page_name,
    "page_nickname": page_nickname,
    "page_emotion": page_emotion,
    "page_story": page_story,
    "page_match": page_match,
    "page_result": page_result,
}

# 현재 페이지 실행
pages[st.session_state.page]()
