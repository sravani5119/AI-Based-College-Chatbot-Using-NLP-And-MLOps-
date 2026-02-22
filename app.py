from flask import Flask, render_template, request, jsonify
from pipeline.chatbot_engine import ChatbotEngine

app = Flask(__name__)

# Initialize chatbot engine
engine = ChatbotEngine()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    print("Received from frontend:", data)

    user_input = data.get("message", "")
    print("User input:", user_input)

    try:
        result = engine.get_response(user_input)
        print("Raw Engine Output:", result)

        # ✅ FIX: Extract only the text response
        if isinstance(result, dict):
            bot_response = result.get("response", "")
        else:
            bot_response = result

    except Exception as e:
        print("ERROR:", e)
        bot_response = "Internal server error."

    # ✅ Always send only plain text to frontend
    return jsonify({"response": bot_response})


if __name__ == "__main__":
    app.run(debug=True)