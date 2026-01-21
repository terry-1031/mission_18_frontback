import os
import requests
import streamlit as st
from datetime import date

st.set_page_config(page_title="Movie List", page_icon="🎬", layout="wide")

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")

def api_get(path: str):
    r = requests.get(f"{API_BASE}{path}", timeout=10)
    r.raise_for_status()
    return r.json()

def api_post(path: str, json: dict):
    r = requests.post(f"{API_BASE}{path}", json=json, timeout=10)
    r.raise_for_status()
    return r.json()

st.title("영화 목록")

with st.sidebar:
    st.header("영화 추가")
    title = st.text_input("제목", placeholder="예: 인터스텔라")
    release_date = st.date_input("개봉일", value=date(2014, 11, 7))
    director = st.text_input("감독", placeholder="예: 크리스토퍼 놀란")
    genre = st.text_input("장르", placeholder="예: SF")
    poster_url = st.text_input("포스터 URL", placeholder="https://...jpg")

    if st.button("등록", type="primary", use_container_width=True):
        if not (title and director and genre and poster_url):
            st.error("제목/감독/장르/포스터 URL은 필수입니다.")
        else:
            try:
                payload = {
                    "title": title,
                    "release_date": release_date.isoformat(),
                    "director": director,
                    "genre": genre,
                    "poster_url": poster_url,
                }
                api_post("/movies", payload)
                st.success("등록 완료!")
                st.rerun()
            except requests.HTTPError as e:
                st.error(f"등록 실패: {e.response.text}")
            except Exception as e:
                st.error(f"등록 실패: {e}")

# 목록 표시
try:
    movies = api_get("/movies")
except Exception as e:
    st.error(f"백엔드 연결 실패: {e}\n\nAPI_BASE_URL={API_BASE}")
    st.stop()

if not movies:
    st.info("등록된 영화가 없습니다. 왼쪽 사이드바에서 영화를 추가해보세요.")
    st.stop()

# 카드형 그리드
cols = st.columns(4)
for i, m in enumerate(movies):
    col = cols[i % 4]
    with col:
        st.image(m["poster_url"], use_column_width=True)
        st.subheader(m["title"])
        if m.get("avg_rating") is not None:
            st.caption(f"평균 평점: {m['avg_rating']:.1f}")
        st.caption(f"개봉일: {m['release_date']}")
        st.caption(f"감독: {m['director']}")
        st.caption(f"장르: {m['genre']}")
