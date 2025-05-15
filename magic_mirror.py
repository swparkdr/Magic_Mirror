
import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import numpy as np

# 페이지 설정
st.set_page_config(page_title="결(結)", layout="centered")

# 커스텀 버튼 스타일 정의
st.markdown("""
<style>
.custom-btn {
    background-color: #b9aee0;
    color: white;
    font-size: 16px;
    font-family: 'Pretendard', sans-serif;
    border-radius: 12px;
    padding: 10px 24px;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin: 10px;
    display: inline-block;
}
.custom-btn:hover {
    background-color: #a493dc;
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

# 배경 이미지 설정
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

# 공통 로고 함수 (중앙 정렬된 헤더용)
def render_logo():
    st.markdown('''
    <div style="width: 100%; text-align: center; margin-top: 10px; margin-bottom: 5px;">
        <img src="https://raw.githubusercontent.com/swparkdr/Magic_Mirror/main/logo.png" width="120">
    </div>
    ''', unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 1
