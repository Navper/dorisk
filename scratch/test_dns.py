import socket

try:
    host = "vdgtskjbifgduzkspjqj.supabase.co"
    ip = socket.gethostbyname(host)
    print(f"OK: DNS resolved: {host} -> {ip}")
except Exception as e:
    print(f"ERROR: DNS resolution failed: {e}")
