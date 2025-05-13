
import streamlit as st
import matplotlib.pyplot as plt

# --- 설정 ---
st.set_page_config(page_title="Magic Mirror", layout="centered")

# --- 페이지 전환 함수 ---
def go_to(page):
    st.session_state.page = page
    st.experimental_rerun()

# --- 세션 초기화 ---
if "page" not in st.session_state:
    st.session_state.page = "name_input"
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "reason" not in st.session_state:
    st.session_state.reason = ""
if "emotion" not in st.session_state:
    st.session_state.emotion = {"x": 5, "y": 5}
if "trajectory" not in st.session_state:
    st.session_state.trajectory = []

# --- 감정 태그 맵 (예시) ---
emotion_tags = {
    (3, 8): "조용한 공감가",
    (7, 8): "감정적인 리더",
    (3, 3): "내성적인 분석가",
    (7, 3): "외향적인 모험가",
    (5, 5): "균형 잡힌 사색가"
}

# --- 감정 시각화 함수 ---
def draw_emotion_map(x, y, trajectory):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0.5, 9.5)
    ax.set_ylim(0.5, 9.5)
    ax.set_xticks(range(1, 10))
    ax.set_yticks(range(1, 10))
    ax.grid(True)
    ax.set_title("감정 위치 지도")

    # 태그 표시
    for (tag_x, tag_y), label in emotion_tags.items():
        ax.text(tag_x, tag_y + 0.2, label, ha='center', fontsize=9, color='gray')

    # 궤적 표시
    if len(trajectory) > 1:
        xs, ys = zip(*trajectory)
        ax.plot(xs, ys, linestyle='--', marker='o', color='blue', alpha=0.6, label="감정 흐름")

    # 현재 위치
    ax.plot(x, y, 'ro', markersize=12, label='현재 감정')
    ax.legend()
    return fig

# --- 페이지 1: 이름 입력 ---
def page_name_input():
    st.markdown("### 안녕? 너는 이름이 뭐야?")
    name = st.text_input("이름을 입력해줘", value=st.session_state.user_name)

    if name.strip():
        st.session_state.user_name = name.strip()
        if st.button("다음으로"):
            go_to("why_here")

# --- 페이지 2: 이유 선택 ---
def page_why_here():
    name = st.session_state.user_name
    st.markdown(f"### 안녕, {name}. 나를 왜 찾아왔어?")
    options = ["그냥, 재미로", "요즘 일이 잘 안풀리네.", "그냥 말하고 싶어서", "외로워"]
    choice = st.radio("이유를 선택해줘", options, index=None)

    if choice:
        st.session_state.reason = choice
        if st.button("다음으로 갈게"):
            go_to("emotion_input")

# --- 페이지 3: 감정 입력 ---
def page_emotion_input():
    st.markdown("### 나는 너가 어떤 사람인지, 더 알고 싶어.")
    st.markdown("#### 감정의 위치를 슬라이더로 표현해줘.")

    col1, col2 = st.columns(2)
    with col1:
        x = st.slider("자기표현 정도 (X축)", 1, 9, st.session_state.emotion["x"])
    with col2:
        y = st.slider("감정 방향성 (Y축)", 1, 9, st.session_state.emotion["y"])

    # 현재 감정값 저장 및 궤적 업데이트
    st.session_state.emotion = {"x": x, "y": y}
    if not st.session_state.trajectory or st.session_state.trajectory[-1] != (x, y):
        st.session_state.trajectory.append((x, y))

    st.markdown(f"📍 현재 감정 좌표: ({x}, {y})")

    fig = draw_emotion_map(x, y, st.session_state.trajectory)
    st.pyplot(fig)

    if st.button("✨ 계속하기"):
        go_to("result")

# --- 페이지 4: 결과 ---
def page_result():
    st.markdown("### 🎯 매칭 결과 준비 중")
    st.write("이름:", st.session_state.user_name)
    st.write("이유:", st.session_state.reason)
    st.write("감정 좌표:", st.session_state.emotion)
    st.write("이전에 지나온 감정 흐름:", st.session_state.trajectory)

    if st.button("🪞 내 감정을 다시 돌아보기"):
        go_to("emotion_input")

    if st.button("➡ 다음"):
        go_to("reflection")

# --- 페이지 5: 자기이해 마무리 ---
def page_reflection():
    st.markdown("## ☕ 자, 네가 나한테 보여준 너는 이런 사람이야.")
    st.write("""
사람은 변하니까, 언제든 와서 바꿀 수 있어!  
하지만, 스스로에게 솔직한 너의 모습이  
제일 너를 행복하게 한다는 것만 기억해줘. 😊
    """)

    st.markdown(" ")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🙌 잘 이해했어"):
            st.success("고마워! 네 감정에 진심이었어.")

    with col2:
        if st.button("💌 자, 이제 다른 사람들을 만나러 가볼까?"):
            st.info("곧 추천 시스템 페이지로 넘어갈 거야!")
            go_to("recommend")

# --- 라우팅 ---
if st.session_state.page == "name_input":
    page_name_input()
elif st.session_state.page == "why_here":
    page_why_here()
elif st.session_state.page == "emotion_input":
    page_emotion_input()
elif st.session_state.page == "result":
    page_result()
elif st.session_state.page == "reflection":
    page_reflection()
