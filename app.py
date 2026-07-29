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
