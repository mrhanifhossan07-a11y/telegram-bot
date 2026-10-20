import logging
from telethon import TelegramClient, events
import requests

# আপনার স্ক্রিনশট থেকে নেওয়া আইডি ও হ্যাশ
API_ID = 23720271
API_HASH = '215a47830efec88902ebc0c6388da99a'

# n8n-এর Webhook URL (আপনার n8n থেকে পাওয়ার পর এখানে বসাবেন)
N8N_WEBHOOK_URL = 'https://sdsasw.app.n8n.cloud/webhook-test/1309dd97-0d78-4cba-ad85-aea9498818ab'

# যেসব চ্যানেল থেকে সিগন্যাল নিতে চান সেগুলোর Username বা লিঙ্ক আইডি
TARGET_CHANNELS = ['@binance_360', '@CryptoWorldUpdates'] 

logging.basicConfig(level=logging.INFO)
client = TelegramClient('siam_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=TARGET_CHANNELS))
async def my_event_handler(event):
    message_text = event.raw_text
    channel_username = event.chat.username or str(event.chat_id)
    
    if message_text:
        print(f"New signal from {channel_username}: {message_text}")
        
        payload = {
            "channel": channel_username,
            "message": message_text,
            "date": str(event.date)
        }
        
        try:
            response = requests.post(N8N_WEBHOOK_URL, json=payload)
            if response.status_code == 200:
                print("Successfully sent to n8n!")
            else:
                print(f"Failed to send to n8n. Status: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

def main():
    print("Siam's Signal Grabber is running...")
    client.start()
    client.run_until_disconnected()

if __name__ == '__main__':
    main()