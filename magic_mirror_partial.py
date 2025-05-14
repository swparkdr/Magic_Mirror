# ───────────────────── magic_mirror_app.py ─────────────────────
import os, random, re
import streamlit as st
import pandas as pd

# 1) 기본 설정
st.set_page_config(page_title="Magic Mirror", layout="centered")

# 2) 매우 간단한 CSS
st.markdown("""
<style>
body            {background:#F9F5F0; font-family:'Noto Sans KR',sans-serif; color:#333;}
h1,h2,h3        {color:#6C63FF; font-weight:600;}
button[data-baseweb="button"] {background:#6C63FF!important; color:#fff; border-radius:8px;}
button[data-baseweb="button"]:hover {background:#DAD3FF!important; color:#333;}
</style>
""", unsafe_allow_html=True)

# 3) CSV 준비 (없으면 더미 생성)
if not os.path.exists("personas_40_full.csv"):
    pd.DataFrame({
        "id": range(1, 41),
        "name": [f"사람{i}" for i in range(1, 41)],
        "story": ["당신과 비슷한 이야기를 가진 사람입니다."]*40,
        "intro": ["짧은 소개"]*40,
        "tags": ["성찰, 유연함, 현실적, 자기통제"]*40,
        "gender": ["남성" if i % 2 else "여성" for i in range(40)],
    }).to_csv("personas_40_full.csv", index=False)

if not os.path.exists("tag_descriptions.csv"):
    pd.DataFrame({"tag": ["성찰","유연함","현실적","자기통제","균형감"]}
                 ).to_csv("tag_descriptions.csv", index=False)

df_persona = pd.read_csv("personas_40_full.csv")
all_tags = sorted(pd.read_csv("tag_descriptions.csv")["tag"].unique().tolist())

# 4) 세션 초기화
defaults = dict(
    page        ="landing",
    user_name   ="",       user_gender="남성",
    emotion     ={"x":5,"y":5},
    final_tags  =[],
    candidates  =df_persona.sample(4).to_dict("records"),
    recommend_index=0,
    reason_story=""
)
for k,v in defaults.items():
    st.session_state.setdefault(k,v)

# 5) 유틸
def rec_tags(x,y):
    if x<=3 and y<=3:   return ["신중함","감정 절제","분석적","객관적","침착함"]
    if x>=7 and y>=7:   return ["외향적","공감","유쾌함","에너지","감성적"]
    if x<=3 and y>=7:   return ["내성적","섬세함","조율자","감정이입","사려 깊음"]
    if x>=7 and y<=3:   return ["직진형","열정","추진력","감정 표현","감정적"]
    return ["균형감","성찰","유연함","현실적","자기통제"]

# 6) 페이지 정의
def landing():
    if os.path.exists("logo.png"):
        st.image("logo.png", width=180)
    else:
        st.markdown("<h2 style='text-align:center;'>🪞</h2>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;'>Magic Mirror</h1>", unsafe_allow_html=True)
    if st.button("시작하기"):
        st.session_state.page="name"

def page_name():
    st.header("너는 누구니?")
    st.markdown("우선, 네 이름을 알고 싶어.\n\n너는 이름이 뭐야? 별명도 좋고, 뭐든 좋아!")
    name   = st.text_input("이름",  st.session_state.user_name)
    gender = st.radio("성별", ["남성","여성"],
                      index=("남성","여성").index(st.session_state.user_gender))
    if st.button("다음으로") and name.strip():
        st.session_state.user_name   = name.strip()
        st.session_state.user_gender = gender
        st.session_state.page        = "encourage"
        st.experimental_rerun()

def page_encourage():
    st.header("작은 용기의 순간")
    uname = st.session_state.user_name or "친구"
    st.markdown(f"""
관계를 맺는 일은 언제나 작은 용기가 필요해요.  
당신이 이름을 적으며 내민 그 손길은 이미 충분히 소중합니다.  
우리는 모두 행복할 자격이 있고, 당신 역시 누군가에게 반짝이는 존재예요.  

우리 사실 모두 동화를 꿈꾼다. 현실이 동화같을 수만은 없겠지만,  
**당신에게도 그런 동화 같은 인연의 시작이 될 수 있기를 바라며.**

{uname}, 사람들과 관계를 맺을 준비가 됐어?  
아직 마음의 준비가 안 된 것 같다면,  
아직 나를 잘 모르겠다면,  
너무 급할 필요 없어!
""")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ 준비가 됐어. 시작해볼까"):
            st.session_state.page="why"
            st.experimental_rerun()
    with col2:
        if st.button("❓ 잘 모르겠어. 어떻게 하면 좋을까?"):
            st.session_state.page="explore"
            st.experimental_rerun()

def page_explore():
    st.header("스스로 탐구 (개발 중)")
    st.write("곧 당신이 자신의 감정을 더 깊이 살펴볼 수 있는 기능이 들어올 거예요.")
    if st.button("돌아가기"):
        st.session_state.page="encourage"
        st.experimental_rerun()

def page_why():
    st.header(f"{st.session_state.user_name}, 나를 왜 찾았어?")
    for row in st.session_state.candidates:
        story = re.sub(r"사람\\d+", row["name"], row["story"])
        st.subheader(row["name"])
        st.write(row["intro"]); st.write(story)
        if st.button(f"👉 이 사람이 가장 공감되요 ({row['name']})", key=row["name"]):
            st.session_state.reason_story = story
            st.session_state.page="emotion"
            st.experimental_rerun()
    if st.button("다른 이야기 보기"):
        st.session_state.candidates = df_persona.sample(4).to_dict("records")
        st.experimental_rerun()

def page_emotion():
    st.header("너의 감정을 좌표로 그려볼까?")
    x = st.slider("자기표현 정도 (1=내향, 9=외향)", 1, 9, st.session_state.emotion["x"])
    y = st.slider("감정 방향성 (1=이성, 9=감성)",   1, 9, st.session_state.emotion["y"])
    st.session_state.emotion = {"x":x,"y":y}
    st.session_state.final_tags = st.multiselect(
        "너를 가장 잘 표현하는 태그를 골라줘",
        all_tags, rec_tags(x,y))
    if st.button("다음으로"):
        st.session_state.page="recommend"

def page_recommend():
    st.header("당신과 감정적으로 닮은 사람")
    user_tags=set(st.session_state.final_tags)
    df=df_persona.copy()
    df["score"]=df["tags"].apply(lambda t: len(user_tags & set(t.split(", "))))
    df=df.sort_values("score",ascending=False).reset_index(drop=True)
    idx=st.session_state.recommend_index
    if idx>=len(df):
        st.warning("더 이상 추천할 사람이 없어요."); return
    row=df.iloc[idx]
    st.subheader(row["name"])
    st.write("공감했던 이야기:", st.session_state.reason_story or "—")
    st.write("너의 태그:", ", ".join(st.session_state.final_tags) or "—")
    st.write("감정 좌표:", st.session_state.emotion)
    if st.button("다른 사람 볼래"):
        st.session_state.recommend_index += 1
        st.experimental_rerun()

# 7) 라우팅
pages = {
    "landing":    landing,
    "name":       page_name,
    "encourage":  page_encourage,
    "explore":    page_explore,   # 🆕
    "why":        page_why,
    "emotion":    page_emotion,
    "recommend":  page_recommend,
}
pages[st.session_state.page]()
