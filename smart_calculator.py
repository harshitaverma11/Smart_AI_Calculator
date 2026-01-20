import os

from flask import Flask, jsonify, render_template, request
from openai import OpenAI

app = Flask(__name__)

# You asked to pass the API key directly in code.
# Replace "YOUR_API_KEY_HERE" with your actual key string.
client = OpenAI(api_key="YOUR API KEY")

SYSTEM_PROMPT = (
    "You are a smart calculator. Solve the math problem correctly and give only the final answer."
)


@app.get("/")
def smart_calculator_page():
    return render_template("smart_calculator.html")


@app.post("/api/calc")
def api_calc():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()

    if not question:
        return jsonify({"error": "Missing 'question'."}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
        )
        answer = (response.choices[0].message.content or "").strip()
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Open in browser: http://127.0.0.1:5000
    app.run(host="127.0.0.1", port=5000, debug=True)