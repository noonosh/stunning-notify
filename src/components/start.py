from telegram import Update
from telegram.error import Unauthorized, BadRequest
from telegram.ext import CallbackContext
from utils.groups_list import groups_list
from src.constants import ADMIN_IDS, BOT_ID
import os

ROOT_DIR = os.path.dirname(os.path.abspath('bot.py'))
FILE = ROOT_DIR + '/' + 'groups.txt'


def start(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    if user_id not in ADMIN_IDS:
        return

    update.effective_message.reply_text(
        "😄 Send me a post to copy it for all available groups.")

    return "POST_AWATING"


def activate(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if user_id not in ADMIN_IDS:
        return

    group_id = str(update.message.chat.id)
    if int(group_id) > 0:
        update.message.reply_text(
            "Activation works only in supergroups! Here, send me /start to begin broadcasting.")
        return

    if update.message.chat.type != 'supergroup':
        update.message.reply_text(
            "Please, make this group a supergroup, and give me full admin permissions.\n\nI promise to be a good boy ;)")
        return

    file = 'groups.txt'

    if group_id in groups_list():
        update.effective_message.reply_text("Group is already active!")
        return

    with open(file, 'a') as append_group:
        append_group.write(group_id + '\n')

    update.effective_message.reply_text(
        "Group activated! I will now be sending important notifications, stay tuned :)")

    group_info = f"<b>🔔 New group activated:</b>\n\nID: {group_id}\nTitle: {update.message.chat.title}"

    context.bot.send_message(user_id, group_info, parse_mode='HTML')
    return "IN_GROUP"


def post(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    post = update.effective_message

    groups = groups_list()

    m = update.effective_message.reply_text(
        f"I started sending. Progress 0/{len(groups)}")

    sent = 0
    for group in groups:
        try:
            p = post.copy(group)
            context.bot.pin_chat_message(group, p.message_id)
            sent += 1
            m.edit_text(f"I started sending. Progress {sent}/{len(groups)}")
        except (Unauthorized, BadRequest):
            continue

    update.effective_message.reply_text(
        f"Sent to all authorized groups: <b>{sent}/{len(groups)}</b>", parse_mode='HTML')

    return start(update, context)


def in_group(update: Update, context: CallbackContext):
    print("IN GROUP UPDATE UNHANDLED: " + str(update))


def unsupported(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        "Unsupported type of media to send. Available formats:\n\n- Text\n- Photo\n- Video\n- Audio (mp3)\n- Voice messages\n\n<b>Beware!</b> All messages sent to bot will be copied EXACTLY THE SAME to all available groups",
        parse_mode='HTML')
    return start(update, context)
