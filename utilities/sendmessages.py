import asyncio
import telegram
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set in environment variables or .env file.")

bot = telegram.Bot(token=TOKEN)

async def send_message(text):
    await bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True
    )


async def send_photo(photo_url):
    await bot.send_photo(
        chat_id=CHAT_ID,
        photo=photo_url
    )


async def send_pdf(pdf_url):
    await bot.send_document(
        chat_id=CHAT_ID,
        document=pdf_url
    )


async def send_documents(pdfs):
    await bot.send_media_group(
        chat_id=CHAT_ID,
        media=pdfs
    )

async def send_update(ann):
    text = ann.get("text", [])
    links = ann.get("links", [])
    images = ann.get("images", [])
    ytvideos = ann.get("ytvideos", [])

    for image in images:
        try:
            await send_photo(image)
        except Exception as e:
            logging.warning(f"Failed to send image {image}: {e}")

    for video in ytvideos:
        await send_message(video)

    pdf_links = [l for l in links if l.lower().endswith(".pdf")]
    #await send_documents([telegram.InputMediaDocument(link) for link in pdf_links])
    for pdf in pdf_links:
        try:
            await send_pdf(pdf)
        except Exception as e:
            logging.warning(f"Failed to send PDF {pdf}: {e}")

    if text:
        text[0] = f"<b>{text[0]}</b>"
        message = "\n".join(text)

        if links:
            message += "\n\n" + "\n".join(links)

        await send_message(message)