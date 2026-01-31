"""
멤버 초기 데이터 등록 스크립트
김택수왕자님이 제공하신 10명의 멤버 정보를 등록합니다.
"""
import requests

# Supabase Config
SUPABASE_URL = "https://aaazjpzmdzobqfmiczrb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFhYXpqcHptZHpvYnFmbWljenJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDcyODQ1NiwiZXhwIjoyMDY2MzA0NDU2fQ.1TEEu33CYYv1dc_H22HZuNv-T_jDeEMeRHbcg0lV5mY"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# 멤버 정보 (이름, 생년월일, 생파날짜)
# 정경원님은 실제 생일 6.09이지만 생파는 12.09 - 나중에 UI에서 특별 처리
MEMBERS = [
    ("왕준석", "1959-10-15", None),
    ("김택수", "1978-06-16", None),
    ("김효근", "1975-09-10", None),
    ("최창원", "1970-07-25", None),
    ("엄준경", "1980-02-06", None),
    ("정경원", "1980-12-09", None),  # 생파 날짜로 등록 (실제 생일 6.09)
    ("장호수", "1979-11-19", None),
    ("장재백", "1976-07-28", None),
    ("이세현", "1976-02-22", None),
    ("박수철", "1983-05-07", None),
]

def clear_all_members():
    """기존 멤버 모두 삭제 (중복 방지)"""
    url = f"{SUPABASE_URL}/rest/v1/members?id=gt.0"
    response = requests.delete(url, headers=HEADERS)
    print(f"기존 멤버 삭제: {response.status_code}")

def add_member(name, birthdate, party_date=None):
    """멤버 추가"""
    url = f"{SUPABASE_URL}/rest/v1/members"
    data = {
        "name": name,
        "birthdate": birthdate
    }
    if party_date:
        data["party_date"] = party_date
    
    response = requests.post(url, headers=HEADERS, json=data)
    status = "✅" if response.status_code in [200, 201, 204] else "❌"
    party_info = f" (생파: {party_date[5:]})" if party_date else ""
    print(f"{status} {name} - {birthdate}{party_info}")
    return response.status_code

def main():
    print("=" * 50)
    print("골프 모임 멤버 등록 스크립트")
    print("=" * 50)
    print()
    
    # 기존 멤버 삭제 (선택적)
    print("🗑️ 기존 멤버 데이터 정리 중...")
    clear_all_members()
    print()
    
    # 새 멤버 등록
    print("📝 새 멤버 등록 중...")
    print("-" * 50)
    
    success_count = 0
    for name, birthdate, party_date in MEMBERS:
        status = add_member(name, birthdate, party_date)
        if status in [200, 201, 204]:
            success_count += 1
    
    print("-" * 50)
    print(f"\n✅ 완료! {success_count}/{len(MEMBERS)}명 등록됨")
    print()

if __name__ == "__main__":
    main()
