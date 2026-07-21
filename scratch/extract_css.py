import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
if style_match:
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(style_match.group(1).strip())
    
    html = html.replace(style_match.group(0), '<link rel="stylesheet" href="styles.css">')
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("CSS extracted successfully.")
else:
    print("No <style> tag found.")
