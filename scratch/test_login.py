import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.db import supabase_client

def test_login():
    try:
        res = supabase_client.auth.sign_in_with_password({
            "email": "erikasolarico@outlook.com",
            "password": "123456"
        })
        if res.user and res.session:
            print("LOGIN EXITO: Token generado correctamente para erikasolarico@outlook.com")
        else:
            print("LOGIN FALLO: No se genero sesion")
    except Exception as e:
        print("LOGIN ERROR:", e)

if __name__ == "__main__":
    test_login()
