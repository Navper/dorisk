import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.db import admin_client

def check_and_confirm():
    user_id = "bbcfa206-4dc8-46f3-9618-911bc660c963"
    try:
        user = admin_client.auth.admin.get_user_by_id(user_id)
        u_data = user.user if hasattr(user, 'user') else user
        print("User details:")
        print("ID:", getattr(u_data, 'id', None))
        print("Email:", getattr(u_data, 'email', None))
        print("Email confirmed at:", getattr(u_data, 'email_confirmed_at', None))
        print("User metadata:", getattr(u_data, 'user_metadata', None))
        
        # Confirm email directly and set password
        admin_client.auth.admin.update_user_by_id(
            user_id,
            {
                "email_confirm": True,
                "password": "123456"
            }
        )
        print("User successfully updated and email confirmed!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    check_and_confirm()
