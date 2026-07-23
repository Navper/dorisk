import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.db import admin_client

def reset_password():
    user_id = "bbcfa206-4dc8-46f3-9618-911bc660c963"
    try:
        admin_client.auth.admin.update_user_by_id(
            user_id,
            {"password": "123456"}
        )
        print("OK: Contrasena actualizada a 123456 para erikasolarico@outlook.com")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    reset_password()
