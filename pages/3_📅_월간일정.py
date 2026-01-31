import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
import sys
import os

# Add parent dir to path to import data_manager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import data_manager

st.set_page_config(page_title="월간일정", page_icon="📅", layout="wide")

st.title("📅 월간 일정 및 현황")

# Select Year and Month
col1, col2 = st.columns([1, 1])
with col1:
    today = datetime.now()
    selected_year = st.selectbox("연도", range(today.year - 1, today.year + 3), index=1)
with col2:
    selected_month = st.selectbox("월", range(1, 13), index=today.month - 1)

st.divider()

# Get data
members_df = data_manager.get_members()
finance_df = data_manager.get_monthly_finance_summary(selected_year, selected_month)

# Prepare Calendar Data
cal = calendar.Calendar()
month_days = cal.monthdayscalendar(selected_year, selected_month)

# Weeks as simple grid
st.markdown(f"### {selected_year}년 {selected_month}월")

cols = st.columns(7)
weekdays = ["월", "화", "수", "목", "금", "토", "일"]
for idx, day_name in enumerate(weekdays):
    cols[idx].write(f"**{day_name}**")

for week in month_days:
    cols = st.columns(7)
    for idx, day in enumerate(week):
        with cols[idx]:
            if day == 0:
                st.write("")
                continue
            
            # Content bucket for the day
            day_content = []
            
            # 1. Check Birthdays
            # Filter members whose MM-DD matches selected_month-day
            if not members_df.empty:
                # Convert birthdate string to datetime to extract month/day easily
                # Assuming format YYYY-MM-DD
                for _, m in members_df.iterrows():
                    try:
                        m_date = pd.to_datetime(m['birthdate'])
                        if m_date.month == selected_month and m_date.day == day:
                            day_content.append(f"🎂 {m['name']}")
                    except:
                        pass
            
            # 2. Check Finances
            if not finance_df.empty:
                finance_df['date_dt'] = pd.to_datetime(finance_df['date'])
                day_fin = finance_df[finance_df['date_dt'].dt.day == day]
                if not day_fin.empty:
                    inc = day_fin[day_fin['type']=='입금']['amount'].sum()
                    exp = day_fin[day_fin['type']=='출금']['amount'].sum()
                    if inc > 0:
                        day_content.append(f"<span style='color:blue'>+{inc:,}</span>")
                    if exp > 0:
                        day_content.append(f"<span style='color:red'>-{exp:,}</span>")

            # Render Day Cell
            border_style = "1px solid #ddd"
            bg_style = "#fff"
            
            # Highlight Today
            if (selected_year == today.year and 
                selected_month == today.month and 
                day == today.day):
                bg_style = "#fff9c4" # Light yellow for today
                border_style = "2px solid #fbc02d"

            html_content = "".join([f"<div style='font-size:0.8em; margin-top:2px;'>{c}</div>" for c in day_content])

            st.markdown(
                f"""
                <div style="
                    height: 100px;
                    border: {border_style};
                    background-color: {bg_style};
                    padding: 5px;
                    border-radius: 5px;
                    margin-bottom: 5px;
                ">
                    <div style="font-weight:bold; color:#333;">{day}</div>
                    {html_content}
                </div>
                """,
                unsafe_allow_html=True
            )
