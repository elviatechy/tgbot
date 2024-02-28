import os
import zipfile
import shutil
import logging
from xml.etree import ElementTree as ET
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import queue

# Define your bot's token here
TOKEN = "6329265648:AAGI0pDQr9ovBwB4onLBf7eZzuZpHtvfCng"

# Define the user IDs allowed to access the bot
ALLOWED_USER_IDS = {1063746236, 987654321, 555555555}  # Replace with your allowed user IDs

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Function to handle the /start command
def start(update, context):
    user_id = update.effective_user.id
    logging.debug("Received /start command from user ID: {}".format(user_id))
    if user_id in ALLOWED_USER_IDS:
        update.message.reply_text("Welcome to the APK Bot! Send me your mobile number and I'll personalize the app for you.")
    else:
        update.message.reply_text("Sorry, you are not authorized to use this bot.")

# Function to handle mobile numbers
def handle_mobile_number(update, context):
    user_id = update.effective_user.id
    logging.debug("Received mobile number from user ID: {}".format(user_id))
    if user_id in ALLOWED_USER_IDS:
        mobile_number = update.message.text.strip()
        apk_path = "base.apk"  # Replace with the path to your base APK file
        edited_apk_path = personalize_apk(apk_path, mobile_number)

        # Send the personalized APK back to the user
        context.bot.send_document(chat_id=update.effective_chat.id, document=open(edited_apk_path, "rb"))
    else:
        update.message.reply_text("Sorry, you are not authorized to use this bot.")

# Function to personalize the APK with the mobile number
def personalize_apk(apk_path, mobile_number):
    # Extract the APK
    with zipfile.ZipFile(apk_path, "r") as zip_ref:
        zip_ref.extractall("temp")

    # Edit the smali files to replace "VNM" with the mobile number
    for root, dirs, files in os.walk("temp"):
        for file in files:
            if file.endswith(".smali"):
                smali_path = os.path.join(root, file)
                replace_text_in_file(smali_path, "VNM", mobile_number)

    # Rebuild the APK
    edited_apk_path = "edited.apk"
    shutil.make_archive("temp", "zip", "temp")
    os.rename("temp.zip", edited_apk_path)

    return edited_apk_path

# Function to replace text in a file
def replace_text_in_file(file_path, old_text, new_text):
    with open(file_path, "r", encoding="utf-8") as file:
        file_data = file.read()

    file_data = file_data.replace(old_text, new_text)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(file_data)

  def main():
    # Create the Updater and pass in your bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Define the command handlers
    dp.add_handler(CommandHandler("start", start))

    # Define the message handler for mobile numbers
    dp.add_handler(MessageHandler(filters.Regex(r'^\d{10}$'), handle_mobile_number))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()      