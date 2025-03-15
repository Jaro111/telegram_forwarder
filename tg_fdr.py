import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
import asyncio
from telegram import Bot


load_dotenv()

api_id = os.getenv('TG_API_ID')
api_hash = os.getenv("TG_API_HASH")
phone = os.getenv("PHONE")
forward_bot_token=os.getenv("BOT_TOKEN")
listen_chanel_username=os.getenv("LISTEN_CHANNEL_USERNAME")

# Your bot credentials (for forwarding messages)
bot_token = forward_bot_token  # From BotFather
destination_chat_id = os.getenv("DESTINATION_ID")  # e.g., a user ID, group ID, or channel ID (like -100123456789)

# Initialize Telethon client (user account)
client = TelegramClient("/app/data/session_name", api_id, api_hash)

# Initialize your Telegram bot
bot = Bot(bot_token)

# Define the private bot's chat ID or username
private_bot_id = int(os.getenv("LISTEN_CHANNEL_ID"))  # Replace with the private bot's chat ID or username

@client.on(events.NewMessage(chats=listen_chanel_username))
async def handler(event):
    # Get the message content
    message_text = event.message.text
    print(f"Received from private bot: {message_text}")
    exact_time = event.message.date  # UTC datetime with seconds
    print(f"Received at {exact_time}")

    # Forward the message using your bot
    try:
        await bot.send_message(chat_id=destination_chat_id, text=message_text)
        print(f"Forwarded to {destination_chat_id}")
    except Exception as e:
        print(f"Error forwarding message: {e}")

async def main():
    await client.start(phone)
    print("Client started. Listening for messages...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())

    