import os
import sys
import traceback
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "..", "backend", ".env")
load_dotenv(env_path)

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

try:
    from supabase import create_client
    client = create_client(supabase_url, supabase_key)
    print("Supabase client created.")
    
    print("Testing signup with dummy credentials...")
    try:
        res = client.auth.sign_up({
            "email": "dummy_test_user@example.com",
            "password": "somepassword123"
        })
        print(f"Signup result: {res}")
    except Exception as inner_e:
        print(f"Signup inner exception: {inner_e}")
        
except Exception as e:
    traceback.print_exc()
