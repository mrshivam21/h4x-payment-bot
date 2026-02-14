from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import qrcode
import os
import asyncio

# --- CONFIGURATION ---
API_ID = 24391673 
API_HASH = "8677c3857e841852037989528628373b"
BOT_TOKEN = "7752119330:AAH8m6A_fD8N_rE9B565l59L57Y1m39pEoo"
UPI_ID = "shivam2171@axl"
# ---------------------

app = Client("payment_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        f"👋 Hello {message.from_user.mention}!\n\nWelcome to Payment Bot. Use /pay to generate a QR code.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Pay Now 💸", callback_data="generate_qr")]])
    )

@app.on_callback_query(filters.regex("generate_qr"))
async def qr_callback(client, callback_query):
    amount = "100"
    upi_url = f"upi://pay?pa={UPI_ID}&pn=Merchant&am={amount}&cu=INR"
    qr = qrcode.make(upi_url)
    qr_path = f"qr_{callback_query.from_user.id}.png"
    qr.save(qr_path)
    await callback_query.message.reply_photo(
        photo=qr_path,
        caption=f"✅ QR Code Generated!\n\nUPI ID: `{UPI_ID}`\nAmount: ₹{amount}\n\nScan this to pay."
    )
    os.remove(qr_path)

async def main():
    async with app:
        print("🚀 Bot is Live on Render!")
        await asyncio.Event().wait()

if __name__ == "__main__":
    # Render (Python 3.14) ke liye special loop fix
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
