import requests
import sys

url = "https://aaazjpzmdzobqfmiczrb.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFhYXpqcHptZHpvYnFmbWljenJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDcyODQ1NiwiZXhwIjoyMDY2MzA0NDU2fQ.1TEEu33CYYv1dc_H22HZuNv-T_jDeEMeRHbcg0lV5mY"

def check():
    print("Checking 'finance' table via REST API...")
    api_url = f"{url}/rest/v1/finance?select=id&limit=1"
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            print("✅ SUCCESS: 'finance' table found and accessible!")
        else:
            print(f"❌ FAIL: Status {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    check()
