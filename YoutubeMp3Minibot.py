import http.client
import re
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your RapidAPI key and host
RAPIDAPI_KEY = #add your rapidapi
RAPIDAPI_HOST = #add rapid host endpoint

# Function to fetch MP3 link
def fetch_mp3_link(video_id: str) -> dict:
    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    conn.request("GET", f"/dl?id={video_id}", headers=headers)
    res = conn.getresponse()
    data = res.read()

    # Parse the JSON response
    return json.loads(data.decode("utf-8"))

# Function to extract the video ID after "v="
def extract_video_id(link: str) -> str:
    # Regex to extract the video ID after "v="
    regex = r"v=([a-zA-Z0-9_-]{11})"
    match = re.search(regex, link)
    if match:
        return match.group(1)
    return None

# Format the API response into a user-friendly message
def format_response(response: dict) -> str:
    if response.get("status") != "ok":
        return "Sorry, I couldn't fetch the MP3 link. Please try again later."

    title = response.get("title", "Unknown Title")
    mp3_link = response.get("link", "")
    filesize_mb = round(response.get("filesize", 0) / (1024 * 1024), 2)  # Convert to MB
    duration_sec = round(response.get("duration", 0), 2)

    message = (
        f"🎵 *Title*: {title}\n"
        f"📥 *Download Link*: [Click Here]({mp3_link})\n"
        f"📦 *File Size*: {filesize_mb} MB\n"
        f"⏱️ *Duration*: {duration_sec} seconds\n"
    )
    return message

# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "🌟 *Welcome to the YouTube MP3 Downloader Bot!* 🌟\n\n"
        "🎧 I can help you download MP3 files from YouTube videos.\n\n"
        "📋 *How to use me:*\n"
        "1. Copy the YouTube video link (e.g., `https://www.youtube.com/watch?v=jHjUJG9SHfo`).\n"
        "2. Paste the link here, and I'll give you the MP3 download link.\n\n"
        "🚀 *Let's get started!* Paste your YouTube link below 👇"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

# Handle YouTube links
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    # Extract the video ID after "v="
    video_id = extract_video_id(user_input)
    if not video_id:
        await update.message.reply_text("❌ Invalid YouTube link. Please send a valid link.")
        return

    # Fetch MP3 link
    try:
        response = fetch_mp3_link(video_id)
        formatted_message = format_response(response)
        await update.message.reply_text(formatted_message, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("❌ Sorry, something went wrong. Please try again later.")
        print(f"Error: {e}")

# Main function to start the bot
def main():
    # Replace with your Telegram bot token
    TELEGRAM_TOKEN = #add yout bot token

    # Create the bot application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
