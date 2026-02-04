from supabase import create_client

url = "https://sonudgyyvxncdcganppl.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvbnVkZ3l5dnhuY2RjZ2FucHBsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDAzMDk0MywiZXhwIjoyMDc1NjA2OTQzfQ.6mmHZJ2QS3a4TywxZ-lswdcvwPCF5NCYLe6CuiO8-3A"

supabase = create_client(url, key)
response = supabase.table("tips").select("id, match_name, profit_percent").execute()

print(f"Összes találat: {len(response.data)}")
