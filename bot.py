import time
import requests
from flask import Flask, request

app = Flask(__name__)
BOT_TOKEN = "8377621786:AAGXu6_8ZNwDpWaTTzvbLZYz4LFoYKQw2UA"

def send_tg(chat_id, text):
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={text}")

@app.route('/', methods=['POST'])
def telegram_bot():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        msg_text = data["message"].get("text", "")
        
        if "clickid=" in msg_text:
            # Extract ClickID
            import urllib.parse as urlparse
            parsed = urlparse.urlparse(msg_text)
            clickid = urlparse.parse_qs(parsed.query).get('clickid', [None])[0]

            if clickid:
                send_tg(chat_id, f"✅ Received! Waiting 4 minutes... then I will run all 3 steps instantly.")
                
                # --- ONLY ONE WAIT (4 MINUTES) ---
                time.sleep(240) 

                # --- STEP 1: ClickID Only (Instant) ---
                requests.post("http://akshit-bro.in/adcounty.php?i=2", data={'clickid': clickid, 'goal': ''})
                
                # --- STEP 2: Goal 1 (Instant) ---
                requests.post("http://akshit-bro.in/adcounty.php?i=2", data={'clickid': clickid, 'goal': 'ds_purchase_success_screen_load'})
                
                # --- STEP 3: Goal 2 (Instant) ---
                requests.post("http://akshit-bro.in/adcounty.php?i=2", data={'clickid': clickid, 'goal': 'dg_purchase_success_screen_load'})

                send_tg(chat_id, "🏁 All 3 steps completed instantly after the 4-minute wait!")

    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    
