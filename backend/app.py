from flask import Flask, request, jsonify
from main import process_content
from flask_cors import CORS
app = Flask(__name__)

@app.route('/')
def home():
    return "AI-Powered Content Remixing API"

@app.route('/process', methods=['POST'])
def process_content_route():
    data = request.get_json()  
    text = data.get("text")    

    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = process_content(text)
    print("this api has run")
    return jsonify(result)  

if __name__ == '__main__':
    app.run(debug=True)
    CORS(app)