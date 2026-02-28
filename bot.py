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
    # --- Step 1: Mandatory 4-minute wait ---
    time.sleep(240) 
    
    target_url = "http://akshit-bro.in/adcounty.php?i=2"
    
    # Advanced Headers to bypass bot detection
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://akshit-bro.in',
        'Referer': 'http://akshit-bro.in/',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    goals = ['', 'ds_purchase_success_screen_load', 'dg_purchase_success_screen_load']
    
    try:
        session = requests.Session() # Using a session to keep cookies if any
        
        for i, goal in enumerate(goals):
            payload = {'clickid': clickid, 'goal': goal}
            response = session.post(target_url, data=payload, headers=headers, timeout=20)
            
            # Debugging: check if the server actually said "success"
            if "success" in response.text.lower():
                print(f"Goal {i} sent successfully")
            else:
                print(f"Goal {i} response: {response.text}")
                
            time.sleep(7) # 7-second gap between steps to ensure server processes each

        send_tg(chat_id, f"✅ Process Fully Executed!\nID: `{clickid}`\nCheck your task dashboard now.")
        
    except Exception as e:
        send_tg(chat_id, f"❌ Technical Error: {str(e)}")

@app.route('/', methods=['POST'])
def telegram_bot():
    data = request.get_json()
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        msg_text = data["message"].get("text", "")
        
        if "clickid=" in msg_text:
            parsed = urlparse.urlparse(msg_text)
            clickid = urlparse.parse_qs(parsed.query).get('clickid', [None])[0]

            if clickid:
                send_tg(chat_id, f"🔎 ClickID: `{clickid}`\n⏳ Bot is mimicking your phone... wait 4 minutes.")
                threading.Thread(target=background_task, args=(chat_id, clickid)).start()

    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    
