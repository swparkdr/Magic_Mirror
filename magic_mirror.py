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

    # 버튼 중앙 정렬용 CSS + 컨테이너
    st.markdown("""
    <style>
    .center-button {
        display: flex;
        justify-content: center;
        margin-top: 80px;
    }
    .center-button button {
        background-color: #d5c7f7;
        color: white;
        border: none;
        border-radius: 30px;
        padding: 10px 30px;
        font-size: 16px;
        font-family: 'Pretendard', sans-serif;
    }
    </style>
    <div class="center-button">
        <form action="" method="post">
            <button type="submit" name="start">시작하기</button>
        </form>
    </div>
    """, unsafe_allow_html=True)

    # 버튼 상태 연결
    if st.session_state.get("start"):
        st.session_state.page = 2
        st.experimental_rerun()
