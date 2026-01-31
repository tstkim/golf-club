import streamlit as st

st.set_page_config(
    page_title="하나로 골프클럽",
    page_icon="⛳",
    layout="wide",
    initial_sidebar_state="expanded"
)

import base64
import os

# 이미지를 base64로 인코딩하는 함수
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# 이미지 로드 시도
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    header_bg_path = os.path.join(current_dir, "header_bg.png")
    header_bg_base64 = get_base64_image(header_bg_path)
    header_css = f"""
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('data:image/png;base64,{header_bg_base64}');
        background-size: cover;
        background-position: center;
    """
except:
    # 이미지 로드 실패 시 그라데이션 폴백
    header_css = """
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    """

# Custom CSS for aesthetics
st.markdown(f"""
<style>
    /* Global Fonts & Colors */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Noto Sans KR', sans-serif;
    }}
    
    .club-header {{
        text-align: center;
        padding: 2rem 0; /* 높이 50% 줄임 */
        {header_css}
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        position: relative;
        overflow: hidden;
    }}
    
    .club-title-kr {{
        font-size: 3.5rem; /* 폰트 키움 */
        font-weight: 800;
        color: #ffffff; /* 흰색으로 변경 */
        text-shadow: 0 4px 8px rgba(0,0,0,0.6);
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }}
    
    .club-title-en {{
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        color: #f0f0f0;
        letter-spacing: 4px;
        text-transform: uppercase;
        font-weight: 500;
        text-shadow: 0 2px 4px rgba(0,0,0,0.6);
        border-top: 1px solid rgba(255,255,255,0.3);
        border-bottom: 1px solid rgba(255,255,255,0.3);
        display: inline-block;
        padding: 5px 20px;
        margin-top: 10px;
        background-color: rgba(0,0,0,0.2); /* 텍스트 가독성 확보 */
        backdrop-filter: blur(2px);
    }}
    
    .metric-card {{
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }}
    
    div.stButton > button {{
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# 클럽 헤더
st.markdown("""
<div class="club-header">
    <div class="club-title-kr">하나로 골프클럽</div>
    <div class="club-title-en">ONE ELITE GOLF CLUB</div>
</div>
""", unsafe_allow_html=True)



st.divider()

# 멤버쉽 룰 설명
with st.expander("📖 하나로 골프클럽 멤버쉽 룰", expanded=True):
    st.markdown("""
    ## ⛳ 하나로 골프클럽 운영 규정
    
    ---
    
    ### 🗓️ 정기 모임
    - **일시**: 매주 주일
    - **장소**: 에프12골프존 스크린 (김포한강4로 341-13)
    - **게임**: 2게임 진행 (1게임 팀전 + 2게임 개인전)
    
    ---
    
    ### 🎮 게임 방식
    
    """, unsafe_allow_html=True)
    st.markdown("""
<style>
.styled-table {
    width: 100%;
    border-collapse: collapse;
    margin: 25px 0;
    font-size: 0.9em;
    font-family: sans-serif;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
}
.styled-table thead tr {
    background-color: #009879;
    color: #ffffff;
    text-align: center;
}
.styled-table th, .styled-table td {
    padding: 12px 15px;
    text-align: center;
    border-bottom: 1px solid #dddddd;
}
.styled-table tbody tr:last-of-type {
    border-bottom: 2px solid #009879;
}
.styled-table tbody tr.active-row {
    font-weight: bold;
    color: #009879;
}
.grade-a { color: #d4af37; font-weight: bold; }
.grade-b { color: #888; font-weight: bold; }
.grade-c { color: #cd7f32; font-weight: bold; }
</style>

<table class="styled-table">
<thead>
<tr>
<th style="width: 15%">순서</th>
<th style="width: 25%">게임</th>
<th style="width: 40%">방식</th>
<th style="width: 20%">목적</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>1게임</b></td>
<td>팀전 (방전)</td>
<td>챔피언+챌린저 vs 내돈내산</td>
<td>실력 밸런스 대결</td>
</tr>
<tr>
<td><b>2게임</b></td>
<td>개인전</td>
<td>각자 경쟁</td>
<td>등급 산정 후 반영</td>
</tr>
</tbody>
</table>
<br>

<h3>💰 게임 참가비 (1게임 기준)</h3>

<table class="styled-table">
<thead>
<tr>
<th style="width: 30%">등급</th>
<th style="width: 40%">별칭</th>
<th style="width: 30%">참가비</th>
</tr>
</thead>
<tbody>
<tr>
<td>🥇 <b>A등급</b></td>
<td class="grade-a">챔피언 🏆</td>
<td><b>10,000원</b></td>
</tr>
<tr>
<td>🥈 <b>B등급</b></td>
<td class="grade-b">내돈내산 💵</td>
<td><b>14,000원</b></td>
</tr>
<tr>
<td>🥉 <b>C등급</b></td>
<td class="grade-c">챌린저 🔥</td>
<td><b>18,000원</b></td>
</tr>
</tbody>
</table>

> 💡 **실력 향상 동기부여!** 잘하면 싸게, 못하면 더 내는 공정한 시스템

<br>
<h3>🏆 등급 배분 기준</h3>
<p>2게임(개인전) 결과 순위에 따라 등급이 결정되고 다음주 팀배정이 됩니다.</p>

<table class="styled-table">
<thead>
<tr>
<th style="width: 20%">참가 인원</th>
<th style="width: 20%">🏆 챔피언</th>
<th style="width: 20%">💵 내돈내산</th>
<th style="width: 20%">🔥 챌린저</th>
<th style="width: 20%">총 방 수</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>4명</b></td>
<td>1명 (1위)</td>
<td>2명 (2~3위)</td>
<td>1명 (4위)</td>
<td>2방</td>
</tr>
<tr>
<td><b>6명</b></td>
<td>2명 (1~2위)</td>
<td>2명 (3~4위)</td>
<td>2명 (5~6위)</td>
<td>3방</td>
</tr>
<tr>
<td><b>8명</b></td>
<td>3명 (1~3위)</td>
<td>2명 (4~5위)</td>
<td>3명 (6~8위)</td>
<td>4방</td>
</tr>
</tbody>
</table>

<br>
<h3>👥 팀 편성 원리</h3>
<p><b>목표</b>: 실력 밸런스를 맞춰 재미있는 경기!</p>

<table class="styled-table">
<thead>
<tr>
<th style="width: 30%">팀 구성</th>
<th style="width: 35%">멤버</th>
<th style="width: 35%">설명</th>
</tr>
</thead>
<tbody>
<tr>
<td style="color:#0066cc; font-weight:bold;">🔵 밸런스팀</td>
<td>챔피언 + 챌린저</td>
<td>상위권 + 하위권</td>
</tr>
<tr>
<td style="color:#009933; font-weight:bold;">🟢 균형팀</td>
<td>내돈내산 + 내돈내산</td>
<td>중위권끼리</td>
</tr>
</tbody>
</table>

**예시 (6명 참가 시)**:
```
🔵 1방: 챔피언(1위) + 챌린저(5위)
🔵 2방: 챔피언(2위) + 챌린저(6위)
🟢 3방: 내돈내산(3위) + 내돈내산(4위)
```
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("""
    ### 📅 주간 사이클
    
    1. **일요일 1게임**: 지난주 등급 기준 팀 편성 → 팀전 진행
    2. **일요일 2게임**: 개인전 진행
    3. **결과 기록**: 순위대로 챔피언/내돈내산/챌린저 등급 부여
    4. **다음 주**: 이번 주 등급 기준으로 새 팀 편성
    
    ---
    
    ### 🎂 생일 축하
    - 생일 달에 해당하는 멤버는 특별 축하!
    - 멤버관리에서 월별 생일자 확인 가능
    """)

# Initialize DB if needed
import data_manager
