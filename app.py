import os
from flask import Flask, request
import google.generativeai as genai
import requests

app = Flask(__name__)

# Gemini API සකස් කරගැනීම
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

# Green API විස්තර
GREEN_API_ID_INSTANCE = os.environ.get("GREEN_API_ID_INSTANCE")
GREEN_API_TOKEN = os.environ.get("GREEN_API_TOKEN")

@app.route("/", methods=["GET", "HEAD"])
def home():
    return "WhatsApp AI Bot is Running 24/7!"

@app.route("/", methods=["POST"])
def webhook():
    try:
        data = request.json
        
        # Green API එකෙන් එන මැසේජ් එක පරීක්ෂා කිරීම
        if data.get("typeWebhook") == "incomingMessageReceived":
            sender = data.get("senderData", {}).get("chatId", "")
            message_data = data.get("messageData", {})
            
            # ටෙක්ස්ට් මැසේජ් එකක් පමණක් ලබා ගැනීම
            message_text = ""
            if message_data.get("typeMessage") == "textMessage":
                message_text = message_data.get("textMessageData", {}).get("textMessage", "")
            elif message_data.get("typeMessage") == "extendedTextMessage":
                message_text = message_data.get("extendedTextMessageData", {}).get("text", "")

            # අංකය පරීක්ෂා කිරීම (අංකය අඩංගුදැයි බැලීම)
            user_phone = "966572686730"
            
            if user_phone in sender and message_text:
                
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

        return "OK", 200
    except Exception as e:
        print(f"Error: {e}")
        return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
