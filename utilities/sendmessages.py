import asyncio
import telegram
import os

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

if not TOKEN or not chat_id:
    raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set in environment variables or .env file.")

bot = telegram.Bot(token=TOKEN)

async def send_message(text, chat_id):
    async with bot:
        await bot.send_message(text=text, chat_id=chat_id, parse_mode="HTML")

async def send_photo(photo, chat_id):
    async with bot:
        await bot.send_photo(photo=photo, chat_id=chat_id)

async def send_documents(documents, chat_id):
    async with bot:
        await bot.send_media_group(media=documents, chat_id=chat_id)

def send_update(div):
    text = div.get('text', [])
    links = div.get('links', [])
    images = div.get('images', [])
    ytvideos = div.get('ytvideos', [])

    if images:
        for image in images:
            asyncio.run(send_photo(image, chat_id))
    if ytvideos:
        for video in ytvideos:
            asyncio.run(send_message(video, chat_id))
    if text:
        text[0] = f"<b>{text[0]}</b>" 
        text_message = "\n".join(text)
        text_message += "\n\n" + "\n".join(links)
        asyncio.run(send_message(text_message, chat_id))
    if links:
        asyncio.run(send_documents([telegram.InputMediaDocument(link) for link in links if link.lower().endswith(".pdf")], chat_id))
