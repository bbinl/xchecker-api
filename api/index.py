from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/check', methods=['GET'])
def check_card():
    card_number = request.args.get('card')

    if not card_number:
        return jsonify({"error": "Missing 'card' query parameter"}), 400

    try:
        response = requests.post(
            'https://web-production-8a397.up.railway.app/api/validate-card',
            json={"card_number": card_number},
            timeout=10
        )

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": "Something went wrong", "details": str(e)}), 500
