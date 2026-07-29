from flask import Flask, request, jsonify
from whatsapp_api_client_python import API
import datetime

app = Flask(__name__)

# Green API credentials
idInstance = "710722695539"
apiTokenInstance = "5dcefdf92a5d46b69f4cd24d720a00fa5430a653a7be4d3687"
green_api = API.GreenAPI(idInstance, apiTokenInstance)

# ට්‍රේඩිං විස්තර ස්ටෝර් කරගන්න සිම්පල් ඩේටාබේස් එකක් (Temporary Memory)
trading_stats = {
    "total_trades": 12,
    "today_profit_usd": 45.50,
    "last_trade": "BUY BTC at $68,000",
    "status": "Active & Running 24/7"
}

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        data = request.json
        
        # WhatsApp එකෙන් මැසේජ් එකක් ආවම පරීක්ෂා කිරීම
        if data and data.get("typeWebhook") == "incomingMessageReceived":
            senderData = data.get("senderData", {})
            messageData = data.get("messageData", {})
            chatId = senderData.get("chatId")
            
            if messageData.get("typeMessage") == "textMessage":
                messageText = messageData.get("textMessageData", {}).get("textMessage", "").lower()
                
                # පරිශීලකයා අහන දේ අනුව රිප්لای එක සැකසීම
                if "profit" in messageText or "ada" in messageText or "today" in messageText or "how much" in messageText:
                    reply_text = (
                        f"📊 *Trading Agent Status (24/7)*\n\n"
                        f"🔹 Total Trades Today: {trading_stats['total_trades']}\n"
                        f"💰 Today's Profit: ${trading_stats['today_profit_usd']}\n"
                        f"🔄 Last Action: {trading_stats['last_trade']}\n"
                        f"⚙️ Status: {trading_stats['status']}"
                    )
                elif "status" in messageText or "hi" in messageText:
                    reply_text = "👋 Hello! මම ඔබේ 24/7 AI Trading Agent එක. මෙතන 'profit' කියලා ටයිප් කරලා අද විස්තර ගන්න පුළුවන්."
                else:
                    reply_text = f"මම ඔබේ පණිවිඩය තේරුම් ගත්තා. ට්‍රේඩිං විස්තර බැලීමට 'profit' ලෙස එවන්න."
                
                # WhatsApp හරහා රිප්لای එක යැවීම
                green_api.sending.sendMessage(chatId, reply_text)
                
        return jsonify({"status": "success"}), 200
        
    return "AI Trading Agent Server is Running 24/7!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
