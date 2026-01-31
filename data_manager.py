import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

# Supabase Config
# Using secrets if available, otherwise falling back (safer to use secrets)
try:
    SUPABASE_URL = st.secrets["supabase"]["url"]
    SUPABASE_KEY = st.secrets["supabase"]["key"]
except:
    # Fallback for local testing without valid secrets file loaded sometimes
    SUPABASE_URL = "https://aaazjpzmdzobqfmiczrb.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFhYXpqcHptZHpvYnFmbWljenJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDcyODQ1NiwiZXhwIjoyMDY2MzA0NDU2fQ.1TEEu33CYYv1dc_H22HZuNv-T_jDeEMeRHbcg0lV5mY"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def check_connection():
    """Checks if we can connect and if tables exist."""
    url = f"{SUPABASE_URL}/rest/v1/finance?select=id&limit=1"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return True
    return False

# --- Finance Functions ---
def add_transaction(date, type, category, amount, description):
    url = f"{SUPABASE_URL}/rest/v1/finance"
    data = {
        "date": str(date),
        "type": type,
        "category": category,
        "amount": amount,
        "description": description
    }
    requests.post(url, headers=HEADERS, json=data)

def get_transactions():
    url = f"{SUPABASE_URL}/rest/v1/finance?select=*&order=date.desc"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        if data:
            return pd.DataFrame(data)
    return pd.DataFrame(columns=['id', 'date', 'type', 'category', 'amount', 'description'])

def update_transaction(txn_id, date, type, category, amount, description):
    url = f"{SUPABASE_URL}/rest/v1/finance?id=eq.{txn_id}"
    data = {
        "date": str(date),
        "type": type,
        "category": category,
        "amount": amount,
        "description": description
    }
    # Prefer return=representation to see result, but minimal is fine
    requests.patch(url, headers=HEADERS, json=data)

def delete_transaction(txn_id):
    url = f"{SUPABASE_URL}/rest/v1/finance?id=eq.{txn_id}"
    requests.delete(url, headers=HEADERS)

def get_monthly_finance_summary(year, month):
    # Construct date range
    start_date = f"{year}-{month:02d}-01"
    if month == 12:
        next_month_year = year + 1
        next_month = 1
    else:
        next_month_year = year
        next_month = month + 1
    next_start_date = f"{next_month_year}-{next_month:02d}-01"
    
    # Supabase Filtering: date >= start_date AND date < next_start_date
    url = f"{SUPABASE_URL}/rest/v1/finance?select=*&date=gte.{start_date}&date=lt.{next_start_date}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            return pd.DataFrame(data)
    return pd.DataFrame(columns=['id', 'date', 'type', 'category', 'amount', 'description'])

# --- Member Functions ---
def add_member(name, birthdate):
    """멤버 추가"""
    url = f"{SUPABASE_URL}/rest/v1/members"
    data = {
        "name": name,
        "birthdate": str(birthdate)
    }
    requests.post(url, headers=HEADERS, json=data)

def get_members():
    url = f"{SUPABASE_URL}/rest/v1/members?select=id,name,birthdate&order=name.asc"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        if data:
            return pd.DataFrame(data)
    return pd.DataFrame(columns=['id', 'name', 'birthdate'])

def update_member(member_id, name, birthdate):
    """멤버 정보 수정"""
    url = f"{SUPABASE_URL}/rest/v1/members?id=eq.{member_id}"
    data = {
        "name": name,
        "birthdate": str(birthdate)
    }
    requests.patch(url, headers=HEADERS, json=data)

def delete_member(member_id):
    url = f"{SUPABASE_URL}/rest/v1/members?id=eq.{member_id}"
    requests.delete(url, headers=HEADERS)

# --- Score Functions ---
def add_score(game_date, member_id, member_name, grade):
    """스코어 등급 추가 (A/B/C)"""
    url = f"{SUPABASE_URL}/rest/v1/scores"
    data = {
        "game_date": str(game_date),
        "member_id": member_id,
        "member_name": member_name,
        "grade": grade  # 'A', 'B', or 'C'
    }
    response = requests.post(url, headers=HEADERS, json=data)
    return response.status_code == 201

def get_scores():
    """모든 스코어 조회 (최신순)"""
    url = f"{SUPABASE_URL}/rest/v1/scores?select=*&order=game_date.desc,grade.asc"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        if data:
            return pd.DataFrame(data)
    return pd.DataFrame(columns=['id', 'game_date', 'member_id', 'member_name', 'grade'])

def get_scores_by_date(game_date):
    """특정 날짜의 스코어 조회"""
    url = f"{SUPABASE_URL}/rest/v1/scores?select=*&game_date=eq.{game_date}&order=grade.asc"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        if data:
            return pd.DataFrame(data)
    return pd.DataFrame(columns=['id', 'game_date', 'member_id', 'member_name', 'grade'])

def delete_score(score_id):
    """스코어 삭제"""
    url = f"{SUPABASE_URL}/rest/v1/scores?id=eq.{score_id}"
    requests.delete(url, headers=HEADERS)

def delete_scores_by_date(game_date):
    """특정 날짜의 모든 스코어 삭제"""
    url = f"{SUPABASE_URL}/rest/v1/scores?game_date=eq.{game_date}"
    requests.delete(url, headers=HEADERS)

def get_latest_game_date():
    """가장 최근 게임 날짜 조회"""
    url = f"{SUPABASE_URL}/rest/v1/scores?select=game_date&order=game_date.desc&limit=1"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['game_date']
    return None

def get_unique_game_dates():
    """고유한 게임 날짜 목록 조회"""
    url = f"{SUPABASE_URL}/rest/v1/scores?select=game_date&order=game_date.desc"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        if data:
            # 중복 제거
            dates = list(set([d['game_date'] for d in data]))
            dates.sort(reverse=True)
            return dates
    return []

