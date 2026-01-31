import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Add parent dir to path to import data_manager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import data_manager

st.set_page_config(page_title="재정관리", page_icon="💰", layout="wide")

st.title("💰 모임 재정 관리")

# === 1. Input Section ===
with st.container():
    st.subheader("📝 내역 입력")
    # Using a clearer layout for input
    col_input1, col_input2, col_input3, col_input4, col_input5, col_input6 = st.columns([2, 1, 2, 2, 3, 1])
    
    with col_input1:
        date = st.date_input("날짜", datetime.now(), label_visibility="collapsed")
    with col_input2:
        txn_type = st.selectbox("구분", ["입금", "출금"], label_visibility="collapsed")
    with col_input3:
        category = st.selectbox("항목", 
                                ["회비", "찬조금", "이월금", "기타"] if txn_type == "입금" 
                                else ["식대", "간식", "상품", "운영비", "기타"], label_visibility="collapsed")
    with col_input4:
        amount = st.number_input("금액", min_value=0, step=1000, value=0, label_visibility="collapsed", placeholder="금액")
    with col_input5:
        description = st.text_input("내용", placeholder="내용 입력", label_visibility="collapsed")
    with col_input6:
        if st.button("저장", type="primary", use_container_width=True):
            if amount > 0:
                data_manager.add_transaction(date, txn_type, category, amount, description)
                st.success("저장됨")
                st.rerun()
            else:
                st.toast("금액을 입력해주세요.")

st.divider()

# Get Data
df = data_manager.get_transactions()

# === 2. Summary & Stats ===
if not df.empty:
    total_income = df[df['type'] == '입금']['amount'].sum()
    total_expense = df[df['type'] == '출금']['amount'].sum()
    balance = total_income - total_expense
    
    col_m1, col_m2, col_m3, col_m4 = st.columns([1, 1, 1, 3])
    col_m1.metric("총 수입", f"+{total_income:,.0f}")
    col_m2.metric("총 지출", f"-{total_expense:,.0f}")
    col_m3.metric("남은 돈", f"{balance:,.0f}원")
    
    # Simple Chart below metrics if needed, or skip to keep it simple as requested.
    # User focused on "List visibility".

st.markdown("### 📋 전체 내역 (수정/삭제 가능)")

# === 3. Transaction List (Editable) ===
if not df.empty:
    # Create a copy for editing
    edit_df = df.copy()
    
    # FIX: Convert string date to datetime object for data_editor
    try:
        edit_df['date'] = pd.to_datetime(edit_df['date'])
    except:
        pass # Handle cases where data might be messy gracefully

    # Add a 'Delete' column (default False)
    edit_df["삭제"] = False
    
    # Configure columns
    edited_df = st.data_editor(
        edit_df,
        column_config={
            "id": None, # Hide ID
            "created_at": None, # Hide timestamp if present
            "date": st.column_config.DateColumn("날짜", format="YYYY-MM-DD", width="small"),
            "type": st.column_config.SelectboxColumn("구분", options=["입금", "출금"], width="small"),
            "category": st.column_config.SelectboxColumn("항목", options=["회비", "찬조금", "이월금", "식대", "간식", "상품", "운영비", "기타"], width="small"),
            "amount": st.column_config.NumberColumn("금액", format="%d원", width="medium"),
            "description": st.column_config.TextColumn("내용", width="large"),
            "삭제": st.column_config.CheckboxColumn("삭제", width="small")
        },
        hide_index=True,
        use_container_width=True,
        num_rows="fixed",
        key="finance_editor_main"
    )

    # Save Changes Button
    col_save_l, col_save_r = st.columns([5, 1])
    with col_save_r:
        if st.button("변경사항 적용", type="primary"):
            changes_count = 0
            for index, row in edited_df.iterrows():
                original_row = df[df['id'] == row['id']].iloc[0]
                
                # Check for Deletion
                if row['삭제']:
                    data_manager.delete_transaction(row['id'])
                    changes_count += 1
                    continue
                
                # Check for Updates
                # Convert date back to string for comparison/saving usually
                # But careful with types. formatting.
                row_date_str = row['date'].strftime("%Y-%m-%d") if isinstance(row['date'], datetime) or isinstance(row['date'], pd.Timestamp) else str(row['date'])[:10]
                orig_date_str = str(original_row['date'])[:10]

                if (row_date_str != orig_date_str or 
                    row['type'] != original_row['type'] or 
                    row['category'] != original_row['category'] or 
                    row['amount'] != original_row['amount'] or 
                    row['description'] != original_row['description']):
                    
                    data_manager.update_transaction(
                        row['id'], 
                        row_date_str, 
                        row['type'], 
                        row['category'], 
                        row['amount'], 
                        row['description']
                    )
                    changes_count += 1
            
            if changes_count > 0:
                st.success("✅ 저장 완료!")
                st.rerun()
            else:
                st.info("변경 사항 없음")
else:
    st.info("입금/출금 내역을 먼저 입력해주세요.")
