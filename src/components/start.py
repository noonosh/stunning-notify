from telegram import Update
from telegram.ext import CallbackContext
from src.constants import ADMIN_IDS, BOT_ID
from src.db.connection import exec, add_group
import os
import html
import json

ROOT_DIR = os.path.dirname(os.path.abspath('bot.py'))
FILE = ROOT_DIR + '/' + 'groups.txt'


def start(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    if user_id not in ADMIN_IDS:
        return

    update.effective_message.reply_text(
        "😄 Send me a post to copy it for all available groups.")

    return "POST_AWATING"


def post(update: Update, context: CallbackContext):
    pass


def status_updates(update: Update, context: CallbackContext):
    if update.message.chat.title is not None:
        # Bot was added to the group while creating
        group_id = update.message.chat.id
        add_group(group_id, update.message.chat.title)
        context.bot.send_message(5340177802, "Bot added while creating group")

    if update.message.migrate_to_chat_id is not None:
        exec(
            f"UPDATE groups SET group_id = {update.message.migrate_to_chat_id} WHERE group_id = {update.message.chat.id}")
        context.bot.send_message(
            5340177802, "Chat migrated from simple group to supergroup")

    context.bot.send_message(5340177802, "New status in group " + str(update))


def manage_groups(update: Update, context: CallbackContext):
    m = update.message
    group_id = m.chat.id

    # if update.message.new_chat_members

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    text = f'<pre>{html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}</pre>'
    context.bot.send_message(5340177802, text, parse_mode='HTML')


def unsupported(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        "Unsupported type of media to send. Available formats:\n\n- Text\n- Photo\n- Video\n- Audio (mp3)\n- Voice messages\n\n<b>Beware!</b> All messages sent to bot will be copied EXACTLY THE SAME to all available groups",
        parse_mode='HTML')
    return start(update, context)
