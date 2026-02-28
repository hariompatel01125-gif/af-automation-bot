import time
import requests
import threading
from flask import Flask, request

app = Flask(__name__)
BOT_TOKEN = "8377621786:AAGXu6_8ZNwDpWaTTzvbLZYz4LFoYKQw2UA"

def send_tg(chat_id, text):
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={text}")

def background_task(chat_id, clickid):
    # This part runs in the background
    time.sleep(240) # Wait 4 mins
    
    target = "http://akshit-bro.in/adcounty.php?i=2"
    
    try:
        # Step 1: Instant
        requests.post(target, data={'clickid': clickid, 'goal': ''}, timeout=10)
        # Step 2: Instant
        requests.post(target, data={'clickid': clickid, 'goal': 'ds_purchase_success_screen_load'}, timeout=10)
        # Step 3: Instant
        requests.post(target, data={'clickid': clickid, 'goal': 'dg_purchase_success_screen_load'}, timeout=10)
        
        send_tg(chat_id, f"🏁 Done! All steps executed for ID: {clickid}")
    except Exception as e:
        send_tg(chat_id, f"❌ Error executing task: {str(e)}")

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
                send_tg(chat_id, "⏳ 4-minute timer started. You can close Telegram now.")
                # Start the 4-minute wait in a separate thread so Render doesn't kill it
                thread = threading.Thread(target=background_task, args=(chat_id, clickid))
                thread.start()

    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    
