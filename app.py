import os
from flask import Flask, request, jsonify
import requests
import google.generativeai as genai

app = Flask(__name__)

# Gemini API සෙටප් කිරීම
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

# Green API විස්තර
GREEN_API_ID_INSTANCE = os.environ.get("GREEN_API_ID_INSTANCE", "7105...") 
GREEN_API_TOKEN = os.environ.get("GREEN_API_TOKEN", "...") 

# Whitelisted Number එක
ALLOWED_NUMBER = os.environ.get("ALLOWED_NUMBER", "966572686730")

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp AI Bot is Running 24/7!"

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    try:
        if data.get("typeWebhook") == "incomingMessageReceived":
            senderData = data.get("senderData", {})
            messageData = data.get("messageData", {})
            
            sender = senderData.get("chatId", "") 
            message_text = ""
            
            if messageData.get("typeMessage") == "textMessage":
                message_text = messageData.get("textMessageData", {}).get("textMessage", "").strip()

            # Whitelisted අංකයෙන් එන මැසේජ් වලට පමණක් Gemini AI එක හරහා පිළිතුරු යැවීම
            if ALLOWED_NUMBER in sender and message_text:
                
                ai_reply = "සමාවෙන්න, මට දැන් AI එකට සම්බන්ධ වෙන්න බැහැ."
                if GEMINI_API_KEY:
                    try:
                        # Gemini AI එකට මැසේජ් එක යවා පිළිතුර ලබා ගැනීම
                        response = model.generate_content(message_text)
                        ai_reply = response.text
                    except Exception as e:
                        ai_reply = f"දෝෂයක් සිදු විය: {str(e)}"

                # WhatsApp වෙත Green API හරහා පිළිතුර යැවීම
                url = f"https://api.green-api.com/waInstance{GREEN_API_ID_INSTANCE}/sendMessage/{GREEN_API_TOKEN}"
                payload = {
                    "chatId": sender,
                    "message": ai_reply
                }
                headers = {'Content-Type': 'application/json'}
                requests.post(url, json=payload, headers=headers)

    except Exception as e:
        print(f"Error: {e}")

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
