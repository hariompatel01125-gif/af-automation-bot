import time
import requests
import threading
import urllib.parse as urlparse
from flask import Flask, request

app = Flask(__name__)
BOT_TOKEN = "8377621786:AAGXu6_8ZNwDpWaTTzvbLZYz4LFoYKQw2UA"

def send_tg(chat_id, text):
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={text}")

def background_task(chat_id, clickid):
    # --- STEP 1: The mandatory 4-minute wait ---
    time.sleep(240) 
    
    target_url = "http://akshit-bro.in/adcounty.php?i=2"
    # Headers make the bot look like the Chrome browser in your video
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        # Action 1: ClickID + Empty Goal (Initial Trigger)
        requests.post(target_url, data={'clickid': clickid, 'goal': ''}, headers=headers, timeout=15)
        time.sleep(5) # 5 second gap to mimic manual typing
        
        # Action 2: ClickID + Purchase Goal 1
        requests.post(target_url, data={'clickid': clickid, 'goal': 'ds_purchase_success_screen_load'}, headers=headers, timeout=15)
        time.sleep(5) # 5 second gap
        
        # Action 3: ClickID + Purchase Goal 2
        requests.post(target_url, data={'clickid': clickid, 'goal': 'dg_purchase_success_screen_load'}, headers=headers, timeout=15)
        
        send_tg(chat_id, f"✅ Process Complete!\nID: `{clickid}`\nAll 3 goals executed exactly like the manual script.")
    except Exception as e:
        send_tg(chat_id, f"❌ Execution Error: {str(e)}")

@app.route('/', methods=['POST'])
def telegram_bot():
    data = request.get_json()
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        msg_text = data["message"].get("text", "")
        
        # Auto-extract ClickID from Appsflyer link
        if "clickid=" in msg_text:
            parsed = urlparse.urlparse(msg_text)
            clickid = urlparse.parse_qs(parsed.query).get('clickid', [None])[0]

            if clickid:
                send_tg(chat_id, f"🔎 ClickID Detected: `{clickid}`\n⏳ Timer started. Running all steps in 4 minutes...")
                threading.Thread(target=background_task, args=(chat_id, clickid)).start()

    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    
