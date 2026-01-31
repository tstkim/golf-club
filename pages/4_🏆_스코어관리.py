import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import sys
import os

# Add parent dir to path to import data_manager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import data_manager

st.set_page_config(page_title="스코어관리", page_icon="🏆", layout="wide")

st.title("🏆 스코어 관리")

# Load members
members_df = data_manager.get_members()

def get_next_sunday(from_date=None):
    """다음 일요일 날짜 반환"""
    if from_date is None:
        from_date = date.today()
    days_until_sunday = (6 - from_date.weekday()) % 7
    if days_until_sunday == 0 and from_date.weekday() != 6:
        days_until_sunday = 7
    return from_date + timedelta(days=days_until_sunday)

def get_last_sunday(from_date=None):
    """지난 일요일 날짜 반환"""
    if from_date is None:
        from_date = date.today()
    days_since_sunday = (from_date.weekday() + 1) % 7
    if days_since_sunday == 0:
        days_since_sunday = 7
    return from_date - timedelta(days=days_since_sunday)

def assign_grades(participants, rankings):
    """
    참가자 수에 따라 A/B/C 등급 배분
    rankings: 순위대로 정렬된 멤버 리스트 (1위부터)
    
    규칙:
    - 6명: A=2, B=2, C=2 → A+C 2팀, B+B 1팀 = 3방
    - 8명: A=3, B=2, C=3 → A+C 3팀, B+B 1팀 = 4방
    - B는 항상 2명 고정, A와 C는 나머지를 균등 분배
    """
    n = len(rankings)
    if n == 0:
        return {}
    
    if n <= 2:
        # 2명 이하: 모두 A
        grades = {member: 'A' for member in rankings}
        return grades
    elif n <= 4:
        # 3~4명: A=1, B=n-2, C=1
        a_count = 1
        c_count = 1
        b_count = n - 2
    else:
        # 5명 이상: B=2 고정, A와 C는 나머지 균등 분배
        b_count = 2
        remaining = n - b_count
        a_count = remaining // 2
        c_count = remaining - a_count
    
    grades = {}
    for i, member in enumerate(rankings):
        if i < a_count:
            grades[member] = 'A'
        elif i < a_count + b_count:
            grades[member] = 'B'
        else:
            grades[member] = 'C'
    
    return grades

# === 탭 구성 ===
tab1, tab2, tab3 = st.tabs(["📝 스코어 입력", "📊 기록 조회", "👥 다음주 팀 편성"])

with tab1:
    st.markdown("### 📝 2게임(개인전) 스코어 입력")
    st.info("💡 2게임 결과를 순위대로 입력하면 자동으로 A/B/C 등급이 배정됩니다.")
    
    # 날짜 선택
    col1, col2 = st.columns([1, 2])
    with col1:
        game_date = st.date_input("📅 게임 날짜", value=date.today())
    
    st.divider()
    
    if members_df.empty:
        st.warning("먼저 멤버를 등록해주세요! (멤버관리 메뉴)")
    else:
        # 참가자 선택
        st.markdown("#### 📍 참가자 선택 (순위 순서대로)")
        
        member_names = members_df['name'].tolist()
        
        # 세션 상태 초기화
        if 'score_rankings' not in st.session_state:
            st.session_state['score_rankings'] = []
        
        # 참가자 추가
        col1, col2 = st.columns([3, 1])
        with col1:
            available_members = [m for m in member_names if m not in st.session_state['score_rankings']]
            if available_members:
                selected_member = st.selectbox(
                    "멤버 선택 (1위부터 순서대로 추가)",
                    options=["선택하세요"] + available_members,
                    key="add_member_select"
                )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ 추가", use_container_width=True):
                if selected_member != "선택하세요":
                    st.session_state['score_rankings'].append(selected_member)
                    st.rerun()
        
        # 현재 순위 표시
        if st.session_state['score_rankings']:
            st.markdown("#### 🏅 현재 순위")
            
            # 등급 미리보기
            preview_grades = assign_grades(
                st.session_state['score_rankings'], 
                st.session_state['score_rankings']
            )
            
            grade_colors = {'A': '🥇', 'B': '🥈', 'C': '🥉'}
            
            cols = st.columns([1, 2, 1, 1])
            cols[0].markdown("**순위**")
            cols[1].markdown("**이름**")
            cols[2].markdown("**등급**")
            cols[3].markdown("**삭제**")
            
            for idx, member in enumerate(st.session_state['score_rankings']):
                grade = preview_grades.get(member, '-')
                cols = st.columns([1, 2, 1, 1])
                cols[0].markdown(f"**{idx + 1}위**")
                cols[1].markdown(member)
                cols[2].markdown(f"{grade_colors.get(grade, '')} {grade}")
                if cols[3].button("❌", key=f"remove_{idx}"):
                    st.session_state['score_rankings'].pop(idx)
                    st.rerun()
            
            st.divider()
            
            # 저장 버튼
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("💾 스코어 저장", type="primary", use_container_width=True):
                    # 기존 해당 날짜 스코어 삭제
                    data_manager.delete_scores_by_date(game_date.strftime("%Y-%m-%d"))
                    
                    # 새 스코어 저장
                    for member_name in st.session_state['score_rankings']:
                        grade = preview_grades[member_name]
                        member_id = members_df[members_df['name'] == member_name]['id'].values[0]
                        data_manager.add_score(
                            game_date.strftime("%Y-%m-%d"),
                            int(member_id),
                            member_name,
                            grade
                        )
                    
                    st.success(f"✅ {len(st.session_state['score_rankings'])}명의 스코어가 저장되었습니다!")
                    st.session_state['score_rankings'] = []
                    st.rerun()
            
            # 초기화 버튼
            if st.button("🔄 초기화", use_container_width=True):
                st.session_state['score_rankings'] = []
                st.rerun()

with tab2:
    st.markdown("### 📊 스코어 기록 조회")
    
    # 게임 날짜 목록 가져오기
    game_dates = data_manager.get_unique_game_dates()
    
    if not game_dates:
        st.info("아직 저장된 스코어가 없습니다.")
    else:
        # 날짜 선택
        selected_date = st.selectbox(
            "📅 조회할 날짜 선택",
            options=game_dates,
            format_func=lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%Y년 %m월 %d일 (일)")
        )
        
        if selected_date:
            scores_df = data_manager.get_scores_by_date(selected_date)
            
            if not scores_df.empty:
                st.markdown(f"#### 📋 {selected_date} 결과")
                
                # 등급별 그룹핑
                grade_groups = {'A': [], 'B': [], 'C': []}
                for _, row in scores_df.iterrows():
                    grade_groups[row['grade']].append(row['member_name'])
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("### 🥇 A등급")
                    for name in grade_groups['A']:
                        st.markdown(f"- {name}")
                    if not grade_groups['A']:
                        st.markdown("_없음_")
                
                with col2:
                    st.markdown("### 🥈 B등급")
                    for name in grade_groups['B']:
                        st.markdown(f"- {name}")
                    if not grade_groups['B']:
                        st.markdown("_없음_")
                
                with col3:
                    st.markdown("### 🥉 C등급")
                    for name in grade_groups['C']:
                        st.markdown(f"- {name}")
                    if not grade_groups['C']:
                        st.markdown("_없음_")
                
                st.divider()
                
                # 삭제 버튼
                if st.button("🗑️ 이 날짜 기록 삭제", type="secondary"):
                    data_manager.delete_scores_by_date(selected_date)
                    st.success("삭제되었습니다!")
                    st.rerun()

with tab3:
    st.markdown("### 👥 다음 주 1게임 팀 편성")
    
    # 상단: 간단 안내 + 룰 설명 버튼
    col_main, col_rule = st.columns([3, 1])
    
    with col_main:
        st.info("💡 지난주 2게임(개인전) 결과를 바탕으로 팀을 편성합니다.")
    
    with col_rule:
        pass  # expander를 위한 공간
    
    # 룰 설명 Expander
    with st.expander("📖 룰 설명 보기", expanded=False):
        st.markdown("""
        ## 🏌️ 골프존 스크린 골프 룰
        
        ---
        
        ### 🎮 게임 구성
        | 순서 | 게임 | 방식 | 비고 |
        |------|------|------|------|
        | 1게임 | **팀전 (방전)** | 챔피언+챌린저팀 vs 내돈내산팀 | 실력 밸런스 |
        | 2게임 | **개인전** | 각자 경쟁 | 등급 산정 후 다음주 첫게임에 팀전 반영 |
        
        ---
        
        ### 💰 게임 참가비 (1게임 기준)
        
        | 등급 | 별칭 | 참가비 |
        |:---:|:---:|:---:|
        | 🥇 **A등급** | **챔피언** 🏆 | **10,000원** |
        | 🥈 **B등급** | **내돈내산** 💵 | **14,000원** |
        | 🥉 **C등급** | **챌린저** 🔥 | **18,000원** |
        
        > 💡 잘하면 싸게, 못하면 더 내는 시스템! 실력 향상 동기부여!
        
        ---
        
        ### 🏆 등급 배분 규칙
        2게임(개인전) 결과 순위에 따라 등급이 배정됩니다.
        
        | 참가 인원 | 🥇 챔피언 | 🥈 내돈내산 | 🥉 챌린저 | 총 방 수 |
        |:---:|:---:|:---:|:---:|:---:|
        | **4명** | 1명 (1위) | 2명 (2~3위) | 1명 (4위) | 2방 |
        | **6명** | 2명 (1~2위) | 2명 (3~4위) | 2명 (5~6위) | 3방 |
        | **8명** | 3명 (1~3위) | 2명 (4~5위) | 3명 (6~8위) | 4방 |
        
        > **📌 공식**: 내돈내산은 항상 2명 고정, 챔피언과 챌린저는 나머지 균등 배분
        
        ---
        
        ### 👥 팀 편성 원리
        
        **목표**: 실력 밸런스를 맞춰 재미있는 경기!
        
        | 팀 구성 | 멤버 | 설명 |
        |:---:|:---:|:---:|
        | 🔵 **밸런스팀** | 챔피언 + 챌린저 | 상위권 + 하위권 |
        | 🟢 **균형팀** | 내돈내산 + 내돈내산 | 중위권끼리 |= 균형 팀 |
        
        **예시 (6명 참가 시)**:
        - 1방: 챔피언(1위) + 챌린저(5위)
        - 2방: 챔피언(2위) + 챌린저(6위)  
        - 3방: 내돈내산(3위) + 내돈내산(4위)
        
        ---
        
        ### 📅 진행 순서
        1. **일요일 1게임**: 지난주 등급 기준 팀 편성 → 팀전
        2. **일요일 2게임**: 개인전 진행
        3. **2게임 결과 기록**: 순위대로 등급 부여
        4. **다음 주 팀 편성**: 이번 주 등급 기준으로 자동 편성
        """)
    
    st.divider()
    
    # 최근 게임 날짜 가져오기
    latest_date = data_manager.get_latest_game_date()
    
    if not latest_date:
        st.warning("아직 저장된 스코어가 없습니다. 먼저 스코어를 입력해주세요!")
    else:
        st.markdown(f"**📅 기준 데이터**: {latest_date}")
        
        scores_df = data_manager.get_scores_by_date(latest_date)
        
        if not scores_df.empty:
            # 등급별 분류
            a_members = scores_df[scores_df['grade'] == 'A']['member_name'].tolist()
            b_members = scores_df[scores_df['grade'] == 'B']['member_name'].tolist()
            c_members = scores_df[scores_df['grade'] == 'C']['member_name'].tolist()
            
            st.divider()
            
            st.markdown("### 🏌️ 추천 팀 편성")
            
            # 팀 편성 로직: A와 C를 매칭
            teams = []
            
            # A-C 매칭
            min_ac = min(len(a_members), len(c_members))
            for i in range(min_ac):
                teams.append({
                    'team_num': len(teams) + 1,
                    'members': [a_members[i], c_members[i]],
                    'type': 'A+C'
                })
            
            # 남은 A 멤버
            remaining_a = a_members[min_ac:]
            # 남은 C 멤버
            remaining_c = c_members[min_ac:]
            
            # B끼리 매칭
            b_pairs = []
            for i in range(0, len(b_members), 2):
                if i + 1 < len(b_members):
                    teams.append({
                        'team_num': len(teams) + 1,
                        'members': [b_members[i], b_members[i+1]],
                        'type': 'B+B'
                    })
                else:
                    # 홀수인 경우 남은 B
                    remaining_b = [b_members[i]]
            
            # 팀 표시
            if teams:
                cols = st.columns(2)
                for idx, team in enumerate(teams):
                    col_idx = idx % 2
                    with cols[col_idx]:
                        team_type_emoji = "🔵" if team['type'] == 'A+C' else "🟢"
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                                    padding: 20px; border-radius: 15px; margin: 10px 0;
                                    border: 1px solid #0f3460;">
                            <h4 style="color: #e94560; margin-bottom: 10px;">
                                {team_type_emoji} {team['team_num']}팀 ({team['type']})
                            </h4>
                            <p style="color: white; font-size: 18px; margin: 0;">
                                👤 {team['members'][0]}<br>
                                👤 {team['members'][1]}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
            
            # 남은 인원 표시
            all_remaining = remaining_a + remaining_c + (remaining_b if 'remaining_b' in dir() else [])
            if all_remaining:
                st.divider()
                st.markdown("#### ⚠️ 미배정 인원")
                st.warning(f"팀 구성에서 남은 인원: {', '.join(all_remaining)}")
            
            st.divider()
            
            # 등급 현황
            st.markdown("#### 📊 등급 현황")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🥇 A등급", f"{len(a_members)}명")
                st.caption(", ".join(a_members) if a_members else "-")
            with col2:
                st.metric("🥈 B등급", f"{len(b_members)}명")
                st.caption(", ".join(b_members) if b_members else "-")
            with col3:
                st.metric("🥉 C등급", f"{len(c_members)}명")
                st.caption(", ".join(c_members) if c_members else "-")
