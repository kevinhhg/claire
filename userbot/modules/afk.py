# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module which contains afk-related commands """

import time
from datetime import datetime
from random import choice, randint

from telethon.events import StopPropagation

from userbot import (
    AFKREASON,
    COUNT_MSG,
    CMD_HELP,
    ISAFK,
    BOTLOG,
    BOTLOG_CHATID,
    USERS,
    PM_AUTO_BAN)  # pylint: disable=unused-imports

from userbot.events import register

# ========================= CONSTANTS ============================
AFKSTR = [
    "i'm busy right now. please talk in a bag and when i come back you can just give me the bag!",
    "i'm away right now. if you need anything, leave a message after the beep:\n`beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeep`!",
    "you missed me, next time aim better.",
    "i'll be back in a few minutes and if i'm not...,\nwait longer.",
    "i'm not here right now, so i'm probably somewhere else.",
    "roses are red,\nviolets are blue,\nleave me a message,\nand i'll get back to you.",
    "sometimes the best things in life are worth waiting for…\ni'll be right back.",
    "i'll be right back,\nbut if i'm not right back,\ni'll be back later.",
    "if you haven't figured it out already,\ni'm not here.",
    "hello, welcome to my away message, how may i ignore you today?",
    "i'm away over 7 seas and 7 countries,\n7 waters and 7 continents,\n7 mountains and 7 hills,\n7 plains and 7 mounds,\n7 pools and 7 lakes,\n7 springs and 7 meadows,\n7 cities and 7 neighborhoods,\n7 blocks and 7 houses...\n\nwhere not even your messages can reach me!",
    "i'm away from the keyboard at the moment, but if you'll scream loud enough at your screen, i might just hear you.",
    "i went that way\n---->",
    "i went this way\n<----",
    "please leave a message and make me feel even more important than i already am.",
    "i am not here so stop writing to me,\nor else you will find yourself with a screen full of your own messages.",
    "if i were here,\ni'd tell you where i am.\n\nbut i'm not,\nso ask me when i return...",
    "i am away!\ni don't know when i'll be back!\nhopefully a few minutes from now!",
    "i'm not available right now so please leave your name, number, and address and i will stalk you later.",
    "sorry, i'm not here right now.\nfeel free to talk to my userbot as long as you like.\ni'll get back to you later.",
    "i bet you were expecting an away message!",
    "life is so short, there are so many things to do...\ni'm away doing one of them..",
    "i am not here right now...\nbut if i was...\n\nwouldn't that be awesome?",
]

global USER_AFK  # pylint:disable=E0602
global afk_time  # pylint:disable=E0602
global afk_start
global afk_end
USER_AFK = {}
afk_time = None
afk_start = {}

# =================================================================


@register(outgoing=True, pattern="^.afk(?: |$)(.*)", disable_errors=True)
async def set_afk(afk_e):
    """ For .afk command, allows you to inform people that you are afk when they message you """
    afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFKREASON
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    global reason
    USER_AFK = {}
    afk_time = None
    afk_end = {}
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    if string:
        AFKREASON = string
        await afk_e.edit(
            f"going afk!\
        \nreason: `{string}`"
        )
    else:
        await afk_e.edit("going afk!")
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\nyou went afk!")
    ISAFK = True
    afk_time = datetime.now()  # pylint:disable=E0602
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ This sets your status as not afk automatically when you write something while being afk """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alive = datetime.now()
    afk_end = back_alive.replace(microsecond=0)
    if ISAFK:
        ISAFK = False
        msg = await notafk.respond("I'm no longer AFK.")
        time.sleep(3)
        await msg.delete()
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "you've recieved "
                + str(COUNT_MSG)
                + " messages from "
                + str(len(USERS))
                + " chats while you were away",
            )
            for i in USERS:
                if str(i).isnumeric():
                    name = await notafk.client.get_entity(i)
                    name0 = str(name.first_name)
                    await notafk.client.send_message(
                        BOTLOG_CHATID,
                        "[" + name0 + "](tg://user?id=" + str(i) + ")" +
                        " sent you " + "`" + str(USERS[i]) + " message(s)`",
                    )
                else:  # anon admin
                    await notafk.client.send_message(
                        BOTLOG_CHATID,
                        "anonymous admin in `" + i + "` sent you " + "`" +
                        str(USERS[i]) + " message(s)`",
                    )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = None


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ This function takes care of notifying the people who mention you that you are AFK."""
    global COUNT_MSG
    global USERS
    global ISAFK
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    afk_since = "a while ago"
    if ISAFK and mention.message.mentioned:
            now = datetime.now()
            datime_since_afk = now - afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "Yesterday"
            elif days > 1:
                if days > 6:
                    date = now + datetime.timedelta(
                        days=-days, hours=-hours, minutes=-minutes
                    )
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime("%A")
            elif hours > 1:
                afk_since = f"`{int(hours)}h{int(minutes)}m` ago"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m{int(seconds)}s` ago"
            else:
                afk_since = f"`{int(seconds)}s` ago"
            
            is_bot = False
            if (sender := await mention.get_sender()):
                is_bot = sender.bot
                if is_bot: return  # ignore bot

            chat_obj = await mention.client.get_entity(mention.chat_id)
            chat_title = chat_obj.title

            if mention.sender_id not in USERS or chat_title not in USERS:
                if AFKREASON:
                    await mention.reply(
                        f"i'm afk since {afk_since}.\
                        \nreason: `{AFKREASON}`"
                    )
                else:
                    await mention.reply(str(choice(AFKSTR)))
                if mention.sender_id is not None:
                    USERS.update({mention.sender_id: 1})
                else:
                    USERS.update({chat_title: 1})
            else:
                if USERS[mention.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await mention.reply(
                            f"i'm still afk since {afk_since}.\
                            \nreason: `{AFKREASON}`"
                        )
                    else:
                        await mention.reply(str(choice(AFKSTR)))
                    if mention.sender_id is not None:
                        USERS[mention.sender_id] += 1
                    else:
                        USERS[chat_title] += 1
                COUNT_MSG += 1


@register(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ Function which informs people that you are AFK in PM """
    global ISAFK
    global USERS
    global COUNT_MSG
    global COUNT_MSG
    global USERS
    global ISAFK
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    afk_since = "a while ago"
    if (
        sender.is_private
        and sender.sender_id != 777000
        and not (await sender.get_sender()).bot
    ):
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved

                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        if apprv and ISAFK:
            now = datetime.now()
            datime_since_afk = now - afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "yesterday"
            elif days > 1:
                if days > 6:
                    date = now + datetime.timedelta(
                        days=-days, hours=-hours, minutes=-minutes
                    )
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime("%A")
            elif hours > 1:
                afk_since = f"`{int(hours)}h{int(minutes)}m` ago"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m{int(seconds)}s` ago"
            else:
                afk_since = f"`{int(seconds)}s` ago"
            if sender.sender_id not in USERS:
                if AFKREASON:
                    await sender.reply(
                        f"i'm afk since {afk_since}.\
                        \nreason: `{AFKREASON}`"
                    )
                else:
                    await sender.reply(str(choice(AFKSTR)))
                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif apprv and sender.sender_id in USERS:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await sender.reply(
                            f"i'm still afk since {afk_since}.\
                            \nreason: `{AFKREASON}`"
                        )
                    else:
                        await sender.reply(str(choice(AFKSTR)))
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


CMD_HELP.update(
    {
        "afk": ".afk [Optional Reason]\
\nUsage: Sets you as afk.\nReplies to anyone who tags/PM's \
you telling them that you are AFK(reason).\n\nSwitches off AFK when you type back anything, anywhere.\
"
    }
)
