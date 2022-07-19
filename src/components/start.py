from email import message
from telegram import Update
from telegram.ext import CallbackContext
from telegram.error import Unauthorized, BadRequest
from utils.text import text
from utils.get_groups import get_groups
from src.constants import ADMIN_IDS
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


def post(update: Update, context: CallbackContext):
    message = update.effective_message
    group_ids = get_groups(FILE)

    if group_ids is 1:
        update.effective_message.reply_text("There are no groups to send.")
        return

    text = f"Wait... I started delivering your message to all groups. Progress: 0/{len(group_ids)}"
    m = update.effective_message.reply_text(text)

    not_sent = 0
    for i in group_ids:
        try:
            message.copy(i)
            m.edit_text(
                f"Wait... I started delivering your message to all groups. Progress: {group_ids.index(i) + 1}/{len(group_ids)}")
            time.sleep(3)
        except (Unauthorized, BadRequest) as e:
            not_sent += 1
            continue

    update.effective_message.reply_text(
        f"Post has been sent to all authorized groups: <b>{len(group_ids) - not_sent}/{len(group_ids)}</b>", parse_mode='HTML')
    return start(update, context)


def manage_groups(update: Update, context: CallbackContext):
    group_id = str(update.effective_chat.id)
    file = 'groups.txt'

    if not os.path.exists(FILE):
        with open(file, 'w') as new_file:
            new_file.write(group_id + '\n')
            return

    groups_list = []
    with open(file, 'r') as f:
        lines = f.readlines()
        for i in lines:
            groups_list.append(i.replace("\n", ""))

    if group_id not in groups_list:
        with open(file, 'a') as ap_file:
            ap_file.write(group_id + '\n')
            return

    with open(file, 'w') as fp:
        for line in lines:
            if line.strip("\n") != group_id:
                fp.write(line)


def unsupported(update: Update, context: CallbackContext):
    update.effective_message.reply_text("Unsupported type of media to send.")
