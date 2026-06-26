import streamlit as st
import unicodedata

st.set_page_config(
    page_title="자소분리 복원기",
    page_icon="🔧",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  /* 전체 배경 */
  [data-testid="stAppViewContainer"] {
    background: #f5f5f7;
  }
  [data-testid="stMain"] {
    background: #f5f5f7;
  }

  /* 카드 영역 */
  .card {
    background: white;
    border-radius: 16px;
    padding: 32px;
    max-width: 560px;
    margin: 48px auto 0;
    box-shadow: 0 2px 16px rgba(0,0,0,0.08);
  }
  .card h1 {
    font-size: 20px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 4px;
  }
  .subtitle {
    font-size: 13px;
    color: #888;
    margin-bottom: 24px;
  }
  .arrow {
    text-align: center;
    font-size: 22px;
    color: #bbb;
    margin: 8px 0;
  }
  .label {
    font-size: 13px;
    font-weight: 600;
    color: #555;
    margin-bottom: 6px;
  }

  /* 태그 */
  .tag-ok  { background:#e4e4ff; color:#5b5ef4; padding:3px 10px; border-radius:99px; font-size:12px; font-weight:700; }
  .tag-nfd { background:#ffe4e4; color:#c0392b; padding:3px 10px; border-radius:99px; font-size:12px; font-weight:700; }

  /* 상태 텍스트 */
  .status-ok  { font-size:12px; color:#5b5ef4; font-weight:600; text-align:right; margin-top:4px; }
  .status-nfd { font-size:12px; color:#c0392b; font-weight:600; text-align:right; margin-top:4px; }

  /* textarea 포커스 색상 */
  textarea:focus { border-color: #5b5ef4 !important; }

  /* 버튼 */
  [data-testid="stButton"] > button {
    border-radius: 10px;
    font-weight: 600;
    font-size: 14px;
    padding: 10px 0;
    width: 100%;
    border: none;
  }
  [data-testid="stButton"]:first-of-type > button {
    background: #f0f0f0;
    color: #555;
  }
  [data-testid="stButton"]:first-of-type > button:hover {
    background: #e4e4e4;
    color: #333;
  }

  /* st.code 복사 버튼이 잘 보이도록 */
  [data-testid="stCodeBlock"] {
    border-radius: 10px;
    border: 1.5px solid #5b5ef4;
    background: #f4f4ff;
  }

  /* footer 숨기기 */
  footer { visibility: hidden; }
  #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── 세션 상태 ──────────────────────────────────────────────────
if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# ── 카드 레이아웃 ───────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h1>🔧 자소분리 복원기</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">붙여넣기만 하면 자동 변환 — 결과 박스 우측 아이콘으로 복사하세요</p>', unsafe_allow_html=True)

st.markdown('<p class="label">깨진 파일명 붙여넣기 (Ctrl+V)</p>', unsafe_allow_html=True)
raw = st.text_area(
    label="input",
    label_visibility="collapsed",
    placeholder="여기에 붙여넣으세요 — 자동으로 변환됩니다",
    height=110,
    key=f"input_{st.session_state.input_key}",
)

st.markdown('<div class="arrow">↓</div>', unsafe_allow_html=True)

# ── 변환 결과 ───────────────────────────────────────────────────
if raw and raw.strip():
    normalized = unicodedata.normalize("NFC", raw)
    is_already_nfc = normalized == raw

    # 라벨 + 태그
    if is_already_nfc:
        st.markdown(
            '<p class="label">복원된 파일명 &nbsp; '
            '<span class="tag-ok">✓ 이미 정상 (NFC)</span></p>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<p class="label">복원된 파일명 &nbsp; '
            '<span class="tag-nfd">NFD → NFC 변환됨</span></p>',
            unsafe_allow_html=True,
        )

    # 결과 (우측 📋 아이콘으로 복사)
    st.code(normalized, language=None)

    # 상태
    if is_already_nfc:
        st.markdown('<p class="status-ok">자소분리 없음 — 그대로 사용하세요</p>', unsafe_allow_html=True)
    else:
        before, after = len(raw), len(normalized)
        st.markdown(
            f'<p class="status-nfd">글자 수: {before}자 → {after}자 ({before - after}자 결합)</p>',
            unsafe_allow_html=True,
        )
else:
    st.markdown('<p class="label">복원된 파일명</p>', unsafe_allow_html=True)
    st.markdown(
        '<div style="padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;'
        'min-height:80px;color:#aaa;font-size:14px;background:#fafafa;">'
        '변환 결과가 여기에 표시됩니다</div>',
        unsafe_allow_html=True,
    )

# ── 지우기 버튼 ─────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🗑 지우기"):
    st.session_state.input_key += 1
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
