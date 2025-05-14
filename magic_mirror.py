import streamlit as st

# 페이지 설정
st.set_page_config(page_title="결(結)", layout="centered")

# 배경 이미지 CSS
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://raw.githubusercontent.com/swparkdr/Magic_Mirror/main/bg.png");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# 세션 상태로 페이지 전환 제어
if 'page' not in st.session_state:
    st.session_state.page = 1

# 1️⃣ 페이지 1: 로고 + 시작
if st.session_state.page == 1:
    st.markdown(
        """
        <div style="text-align: center; margin-top: 10vh;">
            <img src="https://raw.githubusercontent.com/swparkdr/Magic_Mirror/main/logo.png" width="120">
            <div style="margin-top: 1rem; font-size: 14px; color: #555; font-family: 'Pretendard', sans-serif;">
                너의 결, 그리고 나의 결.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)

    if st.button("시작하기"):
        st.session_state.page = 2
        st.experimental_rerun()

# 2️⃣ 페이지 2: 결 소개 + 선택
elif st.session_state.page == 2:
    st.markdown("### 결(結)이 전하고 싶은 이야기")
    st.markdown("""
    결은 사람과 사람 사이의 감정, 흐름, 관계의 ‘결’을 소중히 여기는 공간이야.  
    우리는 알고 있어. 지금 세상은 너무 빠르고, 너무 가볍게 스쳐 지나가.  
    그 안에서 누군가를 믿고, 함께 시간을 쌓는다는 건 생각보다 큰 용기가 필요해.  
    그래서 결은 말하고 싶어.  
    당신이 지금 어떤 상태이든, 그 자체로 충분히 소중하다고.  
    그리고 누군가를 만날 준비가 되어 있다면,  
    우리는 당신의 감정을 존중하며 연결될 수 있는 사람들을 도와줄 수 있다고.

    ---

    **저는 아직 당신을 잘 모르지만, 많이 응원해주고 싶네요.**  
    소중한 당신, 새로운 사람들과의 관계를 맺을 준비가 됐나요?  
    준비가 됐다면, 이제부터 당신이 행복할 수 있게 최대한 도와줄게요.  
    아직은 아닌 것 같다면, 혹은 가벼운 마음에 그런 것 같다면,  
    스스로를 더 보듬어주고 다시 찾아와주세요.  
    우리는 이미, 가벼운 관계들로 너무 많이 병들어 왔잖아요.  
    저는 진심으로 당신이 행복했으면 하거든요.  
    자, 어떤 것 같아요? 편하게 말해주세요.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("준비가 된 것 같아요"):
            st.session_state.page = 3
            st.experimental_rerun()
    with col2:
        if st.button("잘 모르겠어요"):
            st.info("그럴 수도 있어요. 마음이 괜찮아질 때까지 충분히 기다려줄게요.")
    with col3:
        if st.button("나중에 다시 올게요"):
            st.warning("언제든 괜찮아요. 당신의 결이 빛날 그때 다시 만나요.")