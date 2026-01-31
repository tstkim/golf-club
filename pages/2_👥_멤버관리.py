import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
import os

# Add parent dir to path to import data_manager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import data_manager

st.set_page_config(page_title="멤버관리", page_icon="👥", layout="wide")

st.title("👥 멤버 관리")

# Load members
members_df = data_manager.get_members()

def get_birthday_by_month():
    """월별 생일자 딕셔너리 반환"""
    birthday_dict = {i: [] for i in range(1, 13)}
    if not members_df.empty:
        for _, m in members_df.iterrows():
            try:
                m_date = pd.to_datetime(m['birthdate'])
                month = m_date.month
                day = m_date.day
                birthday_dict[month].append({
                    'name': m['name'],
                    'day': day,
                    'year': m_date.year
                })
            except:
                pass
    # 각 월별로 일자순 정렬
    for month in birthday_dict:
        birthday_dict[month] = sorted(birthday_dict[month], key=lambda x: x['day'])
    return birthday_dict

# === 멤버 등록 섹션 ===
with st.expander("➕ 새 멤버 등록하기", expanded=False):
    with st.form("add_member_form"):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("이름")
        with col2:
            new_birth = st.date_input("생년월일", min_value=pd.to_datetime("1950-01-01"))
        
        submit = st.form_submit_button("멤버 저장")
        if submit:
            if new_name:
                data_manager.add_member(new_name, new_birth.strftime("%Y-%m-%d"))
                st.success(f"{new_name}님 등록 완료!")
                st.rerun()
            else:
                st.error("이름은 필수입니다.")

st.divider()

# === 생일자 달별 분류 섹션 ===
st.markdown("### 🎂 월별 생일자")

birthday_dict = get_birthday_by_month()
current_month = datetime.now().month

# 월 이름과 이모지
month_emojis = {
    1: "❄️", 2: "💕", 3: "🌸", 4: "🌷", 5: "🌼", 6: "☀️",
    7: "🏖️", 8: "🌻", 9: "🍂", 10: "🎃", 11: "🍁", 12: "🎄"
}

# 4열씩 3행으로 12개월 표시
for row in range(3):
    cols = st.columns(4)
    for col_idx in range(4):
        month = row * 4 + col_idx + 1
        with cols[col_idx]:
            emoji = month_emojis[month]
            members_in_month = birthday_dict[month]
            
            # 현재 월 강조
            if month == current_month:
                st.markdown(f"##### {emoji} **{month}월** ⭐")
            else:
                st.markdown(f"##### {emoji} {month}월")
            
            if members_in_month:
                for member in members_in_month:
                    # 일자와 이름 표시
                    st.markdown(f"&nbsp;&nbsp;&nbsp;📌 **{member['day']}일** - {member['name']}")
            else:
                st.markdown("&nbsp;&nbsp;&nbsp;_없음_", help="이 달에는 생일자가 없습니다")
            
            st.markdown("")  # 간격

st.divider()

# === 전체 멤버 리스트 섹션 ===
st.markdown("### 📜 전체 멤버 리스트")

if not members_df.empty:
    # 생년월일 표시 형식 변환
    display_df = members_df.copy()
    display_df['birthdate'] = pd.to_datetime(display_df['birthdate']).dt.strftime('%Y.%m.%d')
    
    st.dataframe(
        display_df[['name', 'birthdate']],
        column_config={
            "name": "이름",
            "birthdate": "생년월일"
        },
        use_container_width=True,
        hide_index=True
    )
    
    # 멤버 삭제 기능
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        delete_member = st.selectbox(
            "삭제할 멤버 선택",
            options=["선택하세요"] + members_df['name'].tolist()
        )
    with col2:
        if st.button("🗑️ 삭제", type="secondary"):
            if delete_member != "선택하세요":
                member_id = members_df[members_df['name'] == delete_member]['id'].values[0]
                data_manager.delete_member(member_id)
                st.success(f"{delete_member}님이 삭제되었습니다.")
                st.rerun()
else:
    st.info("등록된 멤버가 없습니다.")
