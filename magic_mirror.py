import streamlit as st

# 페이지 설정
st.set_page_config(page_title="결(結)", layout="centered")

# 안정적인 배경 이미지 + 투명도 적용
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(rgba(255,255,255,0.5), rgba(255,255,255,0.5)),
                url("https://raw.githubusercontent.com/swparkdr/Magic_Mirror/main/bg.png");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# 세션 상태로 페이지 전환 제어
if 'page' not in st.session_state:
    st.session_state.page = 1

# 1️⃣ 페이지 1: 텍스트 + 시작
if st.session_state.page == 1:
    st.markdown(
        '''
        <div style="text-align: center; margin-top: 30vh;">
            <div style="font-size: 16px; color: #555; font-family: 'Pretendard', sans-serif;">
                너의 결, 그리고 나의 결.
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Streamlit 방식 중앙 정렬 버튼
    st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
    if st.button("시작하기"):
        st.session_state.page = 2
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# 2️⃣ 페이지 2: 결 소개 + 선택
elif st.session_state.page == 2:
    st.markdown("### 결(結)이 전하고 싶은 이야기")
    st.markdown('''
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
    ''')

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

# 3️⃣ 페이지 3: 이름/별명 입력
elif st.session_state.page == 3:
    st.markdown("### 당신을 부를 수 있게 해주세요")
    st.markdown('''
    어린왕자 이야기를 아시나요?  
    여우는 말합니다. "너는 아직 내게 수많은 사람 중 하나일 뿐이야.  
    하지만 네가 나를 길들인다면, 나는 너에게 세상에 하나뿐인 존재가 될 거야."  
    
    누군가의 이름을 부르고, 기억하고, 마음에 담는 건 그런 의미예요.  
    이제, 당신을 부를 수 있게 해줄 이름이나 별명을 알려주세요.  
    그게 우리 여정의 첫 걸음이 될 거예요.
    ''')

    name = st.text_input("당신의 이름 또는 별명")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("다음 항목"):
            if name.strip():
                st.session_state.username = name
                st.session_state.page = 4
                st.experimental_rerun()
            else:
                st.warning("이름을 입력해 주세요!")
    with col2:
        if st.button("돌아가기"):
            st.session_state.page = 2
            st.experimental_rerun()
