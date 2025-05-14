# ───────────────────── magic_mirror_app.py ─────────────────────
import os, pathlib, random, re
import streamlit as st
import pandas as pd

# 1) 페이지 설정
st.set_page_config(page_title="Magic Mirror", layout="centered")

# 2) 전역 테마
THEME = """
[theme]
base  = "light"
primaryColor             = "#6C63FF"
secondaryBackgroundColor = "#F9F5F0"
textColor                = "#333333"
font  = "serif"
"""
pathlib.Path(".streamlit").mkdir(exist_ok=True)
cfg = pathlib.Path(".streamlit/config.toml")
if not cfg.exists():
    cfg.write_text(THEME.strip())

# 3) CSS (bg.png 있으면 전체 배경으로 사용)
body_css = (
    "background:#F9F5F0;"
    if not os.path.exists("bg.png")
    else "background:url('bg.png') center/cover no-repeat fixed;"
)
st.markdown(f"""
<style>
body            {{{body_css} font-family:'Noto Sans KR',sans-serif; color:#333;}}
h1,h2,h3        {{color:#6C63FF; font-weight:600;}}
button[data-baseweb="button"] {{
    background:#6C63FF!important; color:#fff; border-radius:8px;
}}
button[data-baseweb="button"]:hover {{
    background:#DAD3FF!important; color:#333;
}}
</style>
""", unsafe_allow_html=True)

# 4) CSV 준비 (없으면 더미 생성)
persona_path, tags_path = "personas_40_full.csv", "tag_descriptions.csv"
if not os.path.exists(persona_path):
    pd.DataFrame({
        "id": range(1, 41),
        "name": [f"사람{i}" for i in range(1, 41)],
        "story": ["당신과 비슷한 이야기를 가진 사람입니다."]*40,
        "intro": ["짧은 소개"]*40,
        "tags": ["성찰, 유연함, 현실적, 자기통제"]*40,
        "gender": ["남성" if i % 2 else "여성" for i in range(40)],
    }).to_csv(persona_path, index=False)

if not os.path.exists(tags_path):
    pd.DataFrame({"tag": ["성찰","유연함","현실적","자기통제","균형감"]}
                 ).to_csv(tags_path, index=False)

df_persona = pd.read_csv(persona_path)
df_tags    = pd.read_csv(tags_path)
all_tags   = sorted(df_tags["tag"].unique().tolist())

# 5) 세션 상태
default_state = dict(
    page="landing",
    user_name="", user_gender="남성", preference="",
    reason_name="", reason_story="", selected_reason_tags=[],
    emotion=dict(x=5, y=5), final_tags=[], recommend_index=0,
    candidates=df_persona.sample(4).to_dict("records"),
)
for k, v in default_state.items():
    st.session_state.setdefault(k, v)

# 6) 공통 헤더
def header(sub):
    st.markdown("<h1 style='text-align:center;'>✨ Magic Mirror</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center;'>{sub}</h3>", unsafe_allow_html=True)
    st.markdown("---")

# 7) 유틸
def rec_tags(x, y):
    if x<=3 and y<=3: return ["신중함","감정 절제","분석적","객관적","침착함"]
    if x>=7 and y>=7: return ["외향적","공감","유쾌함","에너지","감성적"]
    if x<=3 and y>=7: return ["내성적","섬세함","조율자","감정이입","사려 깊음"]
    if x>=7 and y<=3: return ["직진형","열정","추진력","감정 표현","감정적"]
    return ["균형감","성찰","유연함","현실적","자기통제"]

# 8) 페이지
def page_landing():
    # ── 로고 + 텍스트만 ─────────────────────────────
    if os.path.exists("logo.png"):
        st.image("logo.png", width=180)
    else:
        st.markdown("<h2 style='text-align:center;'>🪞</h2>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center;'>Magic Mirror</h1>", unsafe_allow_html=True)

    if st.button("시작하기"):
        st.session_state.page = "name_input"
        st.experimental_rerun()

def page_name():
    header("너는 누구니?")
    st.markdown("우선, 네 이름을 알고 싶어.\n\n"
                "너는 이름이 뭐야? 별명도 좋고, 뭐든 좋아!")
    name   = st.text_input("이름", st.session_state.user_name)
    gender = st.radio("성별", ["남성","여성"],
                      index=("남성","여성").index(st.session_state.user_gender))
    if st.button("다음으로") and name.strip():
        st.session_state.user_name, st.session_state.user_gender = name.strip(), gender
        st.session_state.page = "why_here"; st.experimental_rerun()

def page_why():
    header(f"{st.session_state.user_name}, 나를 왜 찾았어?")
    for row in st.session_state.candidates:
        story = re.sub(r"사람\\d+", row["name"], row["story"])
        st.markdown(f"#### {row['name']}"); st.write(f"**{row['intro']}**"); st.write(story)
        if st.button(f"👉 이 사람이 가장 공감되요 ({row['name']})", key=row["name"]):
            st.session_state.update(
                reason_name=row["name"], reason_story=story,
                selected_reason_tags=random.sample(row["tags"].split(", "), 4),
                page="emotion_input")
            st.experimental_rerun()
    st.markdown("---")
    if st.button("🔁 다른 이야기 보기"):
        st.session_state.candidates = df_persona.sample(4).to_dict("records"); st.experimental_rerun()

def page_emotion():
    header("너의 감정을 좌표로 그려볼까?")
    x = st.slider("자기표현 정도 (1=내향 9=외향)", 1, 9, st.session_state.emotion["x"])
    y = st.slider("감정 방향성 (1=이성 9=감성)", 1, 9, st.session_state.emotion["y"])
    st.session_state.emotion.update(x=x, y=y)
    recommended = rec_tags(x, y)
    selected = st.multiselect("👇 너를 가장 잘 표현하는 태그를 골라줘",
                              all_tags, default=[t for t in recommended if t in all_tags])
    if selected: st.session_state.final_tags = selected
    if st.button("다음으로"):
        st.session_state.page = "orientation"; st.experimental_rerun()

def page_orient():
    header("어떤 만남을 원해?")
    pref = st.radio("👇 찾는 만남 유형", ["이성애","동성애","양성애"],
                    index=["이성애","동성애","양성애"]
                    .index(st.session_state.preference or "이성애"))
    if st.button("추천 계속하기"):
        st.session_state.preference = pref
        st.session_state.page = "recommendation"; st.experimental_rerun()

def page_reco():
    header("당신과 감정적으로 닮은 사람")
    df = df_persona.copy()
    user_tags = set(st.session_state.final_tags)
    gender = st.session_state.user_gender
    pref = st.session_state.preference
    if   pref == "이성애": df = df[df["gender"] != gender]
    elif pref == "동성애": df = df[df["gender"] == gender]
    df["score"] = df["tags"].apply(lambda t: len(user_tags & set(t.split(", "))))
    df = df
