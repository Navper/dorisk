import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = 'const API_URL = "http://localhost:8000";'
replacement = """// Cambia la URL de Render cuando lo despliegues
        const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
            ? 'http://localhost:8000' 
            : 'https://tu-backend-render.onrender.com';"""

if target in html:
    html = html.replace(target, replacement)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("API_URL updated.")
else:
    print("Target not found.")
