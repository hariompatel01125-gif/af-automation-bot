import time
import requests
import threading
from flask import Flask, request

app = Flask(__name__)
BOT_TOKEN = "8377621786:AAGXu6_8ZNwDpWaTTzvbLZYz4LFoYKQw2UA"

def send_tg(chat_id, text):
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={text}")

def background_task(chat_id, clickid):
    # --- STEP 1: Wait the full 4 minutes first ---
    time.sleep(240) 
    
    target = "http://akshit-bro.in/adcounty.php?i=2"
    headers = {'User-Agent': 'Mozilla/5.0'} # Adding a header to look more like a real user

    try:
        # Action 1: ClickID Only
        requests.post(target, data={'clickid': clickid, 'goal': ''}, headers=headers, timeout=15)
        time.sleep(2) # 2-second gap to prevent server from disconnecting you
        
        # Action 2: First Goal
        requests.post(target, data={'clickid': clickid, 'goal': 'ds_purchase_success_screen_load'}, headers=headers, timeout=15)
        time.sleep(2) # 2-second gap
        
        # Action 3: Second Goal
        requests.post(target, data={'clickid': clickid, 'goal': 'dg_purchase_success_screen_load'}, headers=headers, timeout=15)
        
        send_tg(chat_id, f"🏁 All steps finished successfully for ID: {clickid}")
    except Exception as e:
        send_tg(chat_id, f"❌ Target server refused connection. Error: {str(e)}\nHint: Try sending only one link at a time.")

@app.route('/', methods=['POST'])
def telegram_bot():
    data = request.get_json()
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        msg_text = data["message"].get("text", "")
        
        if "clickid=" in msg_text:
            import urllib.parse as urlparse
            parsed = urlparse.urlparse(msg_text)
            clickid = urlparse.parse_qs(parsed.query).get('clickid', [None])[0]

            if clickid:
                send_tg(chat_id, "⏳ Timer started! Wait 4 minutes for execution...")
                thread = threading.Thread(target=background_task, args=(chat_id, clickid))
                thread.start()

    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    
