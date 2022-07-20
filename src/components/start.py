from telegram import Update
from telegram.ext import CallbackContext
from telegram.error import Unauthorized, BadRequest
from src.constants import ADMIN_IDS, BOT_ID
import os
import time

ROOT_DIR = os.path.dirname(os.path.abspath('bot.py'))
FILE = ROOT_DIR + '/' + 'groups.txt'


def start(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    if user_id not in ADMIN_IDS:
        return

    update.effective_message.reply_text(
        "😄 Send me a post to copy it for all available groups.")

    return "POST_AWATING"


def unsupported(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        "Unsupported type of media to send. Available formats:\n\n- Text\n- Photo\n- Video\n- Audio (mp3)\n- Voice messages\n\n<b>Beware!</b> All messages sent to bot will be copied EXACTLY THE SAME to all available groups",
        parse_mode='HTML')
    return start(update, context)
