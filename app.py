from flask import Flask, request, send_from_directory
from collections import Counter
import re
import os

app = Flask(__name__)

FLAMES_MAP = {
    'F': 'Friendship',
    'L': 'Love',
    'A': 'Affection',
    'M': 'Marriage',
    'E': 'Enemy',
    'S': 'Siblings'
}

def clean_name(name: str) -> str:
    return ''.join(re.findall(r'[a-z]', name.lower()))

def remaining_count(name1: str, name2: str) -> int:
    c1 = Counter(clean_name(name1))
    c2 = Counter(clean_name(name2))
    common = sum((c1 & c2).values())
    return sum(c1.values()) + sum(c2.values()) - 2 * common

def flames_outcome(count: int) -> str:
    flames = ['F', 'L', 'A', 'M', 'E', 'S']
    idx = 0
    while len(flames) > 1:
        idx = (idx + count - 1) % len(flames)
        flames.pop(idx)
    return FLAMES_MAP[flames[0]]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        name1 = request.form.get("name1", "")
        name2 = request.form.get("name2", "")
        count = remaining_count(name1, name2)
        result = flames_outcome(count)

    # Load index.html
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Inject result dynamically
    if result:
        html = html.replace("{{ result }}", f"<div class='result fade-in'>Result: {result}</div>")
    else:
        html = html.replace("{{ result }}", "")

    return html

@app.route("/style.css")
def css():
    return send_from_directory(os.getcwd(), "style.css")

if __name__ == "__main__":
    app.run(debug=True)
