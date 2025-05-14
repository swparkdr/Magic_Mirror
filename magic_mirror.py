import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

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

if 'page' not in st.session_state:
    st.session_state.page = 1

# 1️⃣ 페이지 1: 텍스트 + 시작
if st.session_state.page == 1:
    st.markdown('''
        <div style="text-align: center; margin-top: 30vh;">
            <div style="font-size: 16px; color: #555; font-family: 'Pretendard', sans-serif;">
                너의 결, 그리고 나의 결.
            </div>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
    if st.button("시작하기"):
        st.session_state.page = 2
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
            else:
                st.warning("이름을 입력해 주세요!")
    with col2:
        if st.button("돌아가기"):
            st.session_state.page = 2

# 4️⃣ 페이지 4: 감정 슬라이더
elif st.session_state.page == 4:
    st.markdown(f"### {st.session_state.username}님, 지금의 감정을 잠깐만 들여다볼까요?")
    st.markdown("""
    우리가 지금 머물고 있는 감정의 좌표를 알려줘.  
    고요함과 격렬함 사이, 우울함과 희망 사이 어딘가에 당신이 있어.
    """)

    x = st.slider("감정의 강도 (고요 ↔ 격렬)", 1, 9, 5)
    y = st.slider("감정의 방향 (우울 ↔ 희망)", 1, 9, 5)

    @st.cache_data
    def load_tags():
        df = pd.read_csv("tags.csv")
        df["tags"] = df["tags"].apply(lambda t: [tag.strip() for tag in t.split(",")])
        return df

    tags_df = load_tags()
    match = tags_df[(tags_df["x"] == x) & (tags_df["y"] == y)]
    recommended_tags = match.iloc[0]["tags"] if not match.empty else []

    all_tags = sorted(set(tag for sublist in tags_df["tags"] for tag in sublist))
    selected_tags = st.multiselect("지금 당신을 표현하는 감정 단어를 골라주세요.", options=all_tags, default=recommended_tags)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("다음으로"):
            st.session_state.feeling_x = x
            st.session_state.feeling_y = y
            st.session_state.feeling_tags = selected_tags
            st.session_state.page = 5
    with col2:
        if st.button("이전으로"):
            st.session_state.page = 3

# 5️⃣ 페이지 5: 성향 슬라이더 (내향-외향 / 배려-표현)
elif st.session_state.page == 5:
    st.markdown(f"### {st.session_state.username}님에 대해 조금 더 알려주세요")
    st.markdown("""
    감정뿐 아니라, 관계 속에서의 당신의 **성향**도 함께 알고 싶어요.  
    조용히 바라보는 편인가요? 아니면 먼저 다가가는 편인가요?
    """)

    intro_extro = st.slider("나는 더 내향적인가요, 외향적인가요?", 1, 9, 5)
    care_express = st.slider("나는 배려 중심인가요, 자기표현 중심인가요?", 1, 9, 5)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("다음으로 넘어갈게요"):
            st.session_state.personality_introvert = intro_extro
            st.session_state.personality_expression = care_express
            st.session_state.page = 6
    with col2:
        if st.button("감정 선택으로 돌아갈래요"):
            st.session_state.page = 4

# 6️⃣ 페이지 6: 감정 페르소나 추천
elif st.session_state.page == 6:
    st.markdown(f"### {st.session_state.username}님과 비슷한 감정의 사람들을 찾아봤어요.")
    st.markdown("이 감정의 결을 닮은 사람들을 데려왔어. 누구와 지금 감정을 함께 나누고 싶어?")

    user_tags = st.session_state.feeling_tags
    user_x = st.session_state.feeling_x
    user_y = st.session_state.feeling_y

    @st.cache_data
    def load_personas():
        df = pd.read_csv("personas.csv")
        df["tags"] = df["tags"].apply(lambda t: [tag.strip() for tag in t.split(",")])
        return df

    personas = load_personas()

    def compute_similarity(user_tags, user_x, user_y):
        vectorizer = CountVectorizer(tokenizer=lambda x: x, lowercase=False)
        tag_matrix = vectorizer.fit_transform(personas["tags"])
        user_vec = vectorizer.transform([user_tags])

        tag_sim = cosine_similarity(tag_matrix, user_vec).flatten()
        coord_dist = ((personas["x"] - user_x) ** 2 + (personas["y"] - user_y) ** 2) ** 0.5
        coord_score = 1 - (coord_dist / coord_dist.max())

        final_score = 0.6 * tag_sim + 0.4 * coord_score
        personas["score"] = final_score
        return personas.sort_values(by="score", ascending=False).head(3)

    top_matches = compute_similarity(user_tags, user_x, user_y)

    for idx, row in top_matches.iterrows():
        st.markdown(f"#### {row['name']}")
        st.markdown(f"**감정 태그:** {', '.join(row['tags'])}")
        st.markdown(f"**요약:** {row.get('summary', '요약 정보 없음')}")
        if st.button(f"이 사람과 이어볼래요", key=f"select_{idx}"):
            st.session_state.selected_persona = row['name']
            st.session_state.page = 7

    if st.button("이전으로 돌아갈래요"):
        st.session_state.page = 5

# 7️⃣ 페이지 7: 감정 스토리
elif st.session_state.page == 7:
    name = st.session_state.get("selected_persona", None)
    username = st.session_state.get("username", "당신")

    if not name:
        st.error("선택된 페르소나가 없어요. 이전 단계로 돌아가주세요.")
        if st.button("돌아가기"):
            st.session_state.page = 6
    else:
        @st.cache_data
        def load_stories():
            df = pd.read_csv("story.csv")
            return df

        stories = load_stories()
        story_row = stories[stories["name"] == name]

        if not story_row.empty:
            story_text = story_row.iloc[0]["story"]
            st.markdown(f"### {username}님, 이 사람의 이야기를 들어볼래요?")
            st.markdown("#### ✧ 감정의 결을 따라온 이야기")
            st.markdown(f"""
            <div style='background-color: #f8f5ff; padding: 20px; border-radius: 12px; font-size: 16px; line-height: 1.7em;'>
            {story_text}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown(f"""**{username}**, 당신의 감정은 정말 소중해요.  
이 이야기가 조금이라도 위로가 되었다면, 그것만으로 충분해요.""")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("다시 해볼래"):
                    st.session_state.page = 1
            with col2:
                if st.button("내 결 저장하기"):
                    st.success("아직 구현 중이지만, 곧 당신의 감정 기록을 저장할 수 있게 될 거예요.")
        else:
            st.error("해당하는 스토리를 찾지 못했어요.")
