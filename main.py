from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from bs4 import BeautifulSoup
import aiohttp

# Function to check if the anime is available by scraping the site
async def is_anime_available(anime_name):
    search_url = f"https://www.blakiteanime.fun/search?q={anime_name.replace(' ', '+')}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as response:
                if response.status == 200:
                    page_content = await response.text()
                    soup = BeautifulSoup(page_content, 'html.parser')
                    results = soup.find_all('div', class_='hentry play c:hover-eee')
                    if results:
                        return True, search_url
                    else:
                        return False, search_url
                else:
                    return False, search_url
    except aiohttp.ClientError:
        return False, search_url

# Function to handle user messages and respond
async def search_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    bot_username = (await context.bot.get_me()).username

    # Check if the bot is explicitly mentioned
    if f"@{bot_username}" in message.text or message.text.strip().lower().startswith("bot"):
        # Extract the anime name after removing the bot mention
        anime_name = message.text.replace(f"@{bot_username}", "").replace("bot", "").strip()
        if anime_name:
            await message.reply_text("Please wait... Searching now...")
            available, search_url = await is_anime_available(anime_name)
            if available:
                reply_message = (
                    f"Here Is Your Link: [{anime_name}]({search_url})\n"
                    f"Let Me Know You Want More\n"
                    f"Stay Tuned\n"
                )
                await message.reply_text(reply_message, parse_mode='Markdown')
            else:
                reply_message = (
                    "Sorry, we couldn't find that anime.\n" 
                    "Please check the name or try again.\n"
                    "If anime is not available, go to Chat Group: t.me/blakitechats and comment there."
                )
                await message.reply_text(reply_message, parse_mode='Markdown')
        else:
            await message.reply_text(
                "Please mention an anime name after calling me!",
                parse_mode='Markdown'
            )
    else:
        # Ignore messages that do not call the bot
        return

# Main function to set up the bot
def main():
    application = Application.builder().token("7803638695:AAGY4G0A8qCImLZkGZnGGFBRzOwG9AqeAkc").build()
    # Add a message handler for user text input
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_anime))
    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
