from supabase import create_client, Client
import sys

url = "https://aaazjpzmdzobqfmiczrb.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFhYXpqcHptZHpvYnFmbWljenJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDcyODQ1NiwiZXhwIjoyMDY2MzA0NDU2fQ.1TEEu33CYYv1dc_H22HZuNv-T_jDeEMeRHbcg0lV5mY"

try:
    supabase: Client = create_client(url, key)
    # Try to fetch from a non-existent table to see the error message, 
    # or fetch from 'finance' to see if it exists.
    response = supabase.table("finance").select("*").limit(1).execute()
    print("Table 'finance' exists.")
except Exception as e:
    print(f"Error: {e}")
    # If error contains "relation \"finance\" does not exist", we confirm table is missing.
