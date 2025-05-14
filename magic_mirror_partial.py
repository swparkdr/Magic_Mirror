# ───────────────────── magic_mirror_app.py ─────────────────────
import os, random, re
import streamlit as st
import pandas as pd

# 1) 기본 설정
st.set_page_config(page_title="Magic Mirror", layout="centered")

# 2) 가벼운 CSS
st.markdown("""
<style>
body{background:#F9F5F0;font-family:'Noto Sans KR',sans-serif;color:#333;}
h1,h2,h3{color:#6C63FF;font-weight:600;}
button[data-baseweb="button"]{background:#6C63FF!important;color:#fff;border-radius:8px;}
button[data-baseweb="button"]:hover{background:#DAD3FF!important;color:#333;}
</style>
""", unsafe_allow_html=True)

# 3) CSV 준비 (없으면 더미)
if not os.path.exists("personas_40_full.csv"):
    pd.DataFrame({
        "id": range(1, 41),
        "name": [f"아린{i}" for i in range(1, 41)],
        "story": ["사람20은 새로운 도전을 앞두고 마음이 두근거려."]*40,
        "intro": ["짧은 소개"]*40,
        "tags": ["성찰, 유연함, 현실적, 자기통제"]*40,
        "gender": ["남성" if i % 2 else "여성" for i in range(40)],
    }).to_csv("personas_40_full.csv", index=False)

if not os.path.exists("tag_descriptions.csv"):
    pd.DataFrame({"tag": ["성찰","유연함","현실적","자기통제","균형감"]}
                 ).to_csv("tag_descriptions.csv", index=False)

df_persona = pd.read_csv("personas_40_full.csv")
all_tags   = sorted(pd.read_csv("tag_descriptions.csv")["tag"].unique().tolist())

# 4) 세션 초기화
init = dict(
    page="landing",
    user_name="", user_gender="남성",
    emotion={"x":5,"y":5},
    final_tags=[],
    candidates=df_persona.sample(4).to_dict("records"),
    recommend_index=0,
    reason_story=""
)
for k,v in init.items():
    st.session_state.setdefault(k,v)

# 5) 유틸
def rec_tags(x,y):
    if x<=3 and y<=3: return ["신중함","감정 절제","분석적","객관적","침착함"]
    if x>=7 and y>=7: return ["외향적","공감","유쾌함","에너지","감성적"]
    if x<=3 and y>=7: return ["내성적","섬세함","조율자","감정이입","사려 깊음"]
    if x>=7 and y<=3: return ["직진형","열정","추진력","감정 표현","감정적"]
    return ["균형감","성찰","유연함","현실적","자기통제"]

# 6) 페이지들
def landing():
    st.markdown("<h1 style='text-align:center;'>Magic Mirror</h1>", unsafe_allow_html=True)
    if st.button("시작하기"):
        st.session_state.page="name"

def page_name():
    st.header("네 이름 알려줘!")
    st.markdown("먼저 네 이름부터 적어줘. 편한 별명도 좋아 🙂")
    name   = st.text_input("이름 쓰기", st.session_state.user_name)
    gender = st.radio("성별 골라줘", ["남성","여성"],
                      index=("남성","여성").index(st.session_state.user_gender))
    if st.button("다음으로") and name.strip():
        st.session_state.user_name   = name.strip()
        st.session_state.user_gender = gender
        st.session_state.page        = "encourage"
        st.experimental_rerun()

def page_encourage():
    uname = st.session_state.user_name or "친구"
    st.header("작은 용기의 순간이야")
    st.markdown(f"""
누군가랑 이어지려면 항상 조금의 용기가 필요해.  
이름 적은 순간, 이미 한 걸음 내디딘 거야.  

**이번이 네 동화 같은 인연의 시작이 되길 바라!**

{uname}, 사람들과 연결될 준비 됐어?  
마음이 아직 안 열렸으면 천천히 해도 괜찮아 🙂
""")
    col1,col2 = st.columns(2)
    if col1.button("준비됐어, 시작하자!"):
        st.session_state.page="why"; st.experimental_rerun()
    if col2.button("잘 모르겠어…"):
        st.info("자기 탐구 기능은 만드는 중이야 🙂")
        if st.button("돌아가기"):
            st.session_state.page="encourage"; st.experimental_rerun()

def page_why():
    uname = st.session_state.user_name or "친구"
    st.header(f"{uname}, 왜 나를 찾았어?")
    st.markdown("""
네 얘기를 본격적으로 들어볼게!  
아래 사람들 중 **제일 공감 가는 이야기**를 골라줘.
""")
    for row in st.session_state.candidates:
        story = re.sub(r"(사람\\d+|Person\\d+)", row["name"], row["story"])
        st.subheader(row["name"]); st.write(row["intro"]); st.write(story)
        if st.button(f"👉 이 이야기 공감돼 ({row['name']})", key=row["name"]):
            st.session_state.reason_story = story
            st.session_state.page="emotion"; st.experimental_rerun()
    if st.button("다른 이야기 보여줘"):
        st.session_state.candidates = df_persona.sample(4).to_dict("records"); st.experimental_rerun()

def page_emotion():
    st.header("네 감정을 좌표로 그려볼까?")
    x = st.slider("자기표현 정도 (1=내향, 9=외향)", 1, 9, st.session_state.emotion["x"])
    y = st.slider("감정 방향성 (1=이성, 9=감성)", 1, 9, st.session_state.emotion["y"])  # ← 따옴표 닫힘 확인
    st.session_state.emotion = {"x":x,"y":y}

    default_tags = [t for t in rec_tags(x, y) if t in all_tags]

    st.session_state.final_tags = st.multiselect(
        "너를 잘 표현하는 태그 골라봐",
        all_tags,
        default=default_tags,
    )
    if st.button("다음으로"):
        st.session_state.page="recommend"

def page_recommend():
    st.header("너랑 감정적으로 닮은 사람이야")
    user_tags=set(st.session_state.final_tags)
    df=df_persona.copy()
    df["score"]=df["tags"].apply(lambda t: len(user_tags & set(t.split(", "))))
    df=df.sort_values("score",ascending=False).reset_index(drop=True)
    idx=st.session_state.recommend_index
    if idx>=len(df):
        st.warning("추천할 사람이 더 없어 😥"); return
    row=df.iloc[idx]
    st.subheader(row["name"])
    st.write("공감했던 이야기:", st.session_state.reason_story or "—")
    st.write("네 태그:", ", ".join(st.session_state.final_tags) or "—")
    st.write("감정 좌표:", st.session_state.emotion)
    if st.button("다른 사람도 볼래"):
        st.session_state.recommend_index += 1
        st.experimental_rerun()

# 7) 라우터
pages = {
    "landing":    landing,
    "name":       page_name,
    "encourage":  page_encourage,
    "why":        page_why,
    "emotion":    page_emotion,
    "recommend":  page_recommend,
}
pages[st.session_state.page]()
