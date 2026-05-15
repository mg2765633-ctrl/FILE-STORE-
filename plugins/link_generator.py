# +++ Made By Gojo [telegram username: @ryomen_0] +++

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from helper_func import encode, get_message_id, is_admin


@Bot.on_message(filters.command('batch') & filters.private & is_admin)
async def batch(client: Client, message: Message):
    channel = f"<a href={client.db_channel.invite_link}>ᴅʙ ᴄʜᴀɴɴᴇʟ</a>" 
    while True:
        try:
            first_message = await client.ask(text=f"<b>ғᴏʀᴡᴀʀᴅ ᴛʜᴇ ғɪʀsᴛ ᴍᴇssᴀɢᴇ ғʀᴏᴍ {channel} (ᴡɪᴛʜ ǫᴜᴏᴛᴇs)..\n<blockquote>ᴏʀ sᴇɴᴅ ᴛʜᴇ {channel} ᴘᴏsᴛ ʟɪɴᴋ</b>", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60, disable_web_page_preview=True)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply(f"<b>❌ ᴇʀʀᴏʀ..\nᴛʜɪs ғᴏʀᴡᴀʀᴅᴇᴅ ᴘᴏsᴛ ᴏʀ ᴍᴇssᴀɢᴇ ʟɪɴᴋ ɪs ɴᴏᴛ ғʀᴏᴍ ᴍʏ {channel}</b>", quote = True, disable_web_page_preview=True)
            continue

    while True:
        try:
            second_message = await client.ask(text =f"<b>ғᴏʀᴡᴀʀᴅ ᴛʜᴇ Lᴀsᴛ ᴍᴇssᴀɢᴇ ғʀᴏᴍ {channel} (ᴡɪᴛʜ ǫᴜᴏᴛᴇs)..\n<blockquote>ᴏʀ sᴇɴᴅ ᴛʜᴇ {channel} ᴘᴏsᴛ ʟɪɴᴋ</b>", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60, disable_web_page_preview=True)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply(f"<b>❌ ᴇʀʀᴏʀ..\nᴛʜɪs ғᴏʀᴡᴀʀᴅᴇᴅ ᴘᴏsᴛ ᴏʀ ᴍᴇssᴀɢᴇ ʟɪɴᴋ ɪs ɴᴏᴛ ғʀᴏᴍ ᴍʏ {channel}</b>", quote=True, reply_markup=reply_markup, disable_web_page_preview=True)
            continue


    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("📫 Sʜᴀʀᴇ URL", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>›› ʙᴇʟᴏᴡ ɪs ʏᴏᴜʀ ʟɪɴᴋ:</b>\n\n<blockquote>{link}</blockquote>", quote=True, reply_markup=reply_markup, disable_web_page_preview=True)


@Bot.on_message(filters.command('genlink') & filters.private & is_admin)
async def link_generator(client: Client, message: Message):
    channel = f"<a href={client.db_channel.invite_link}>ᴅʙ ᴄʜᴀɴɴᴇʟ</a>"
    while True:
        try:
            channel_message = await client.ask(text =f"<b><blockquote>ғᴏʀᴡᴀʀᴅ ᴛʜᴇ ᴍᴇssᴀɢᴇ ғʀᴏᴍ {channel} (ᴡɪᴛʜ ǫᴜᴏᴛᴇs)..</blockquote>\n<blockquote>ᴏʀ sᴇɴᴅ ᴛʜᴇ {channel} ᴘᴏsᴛ ʟɪɴᴋ</blockquote></b>", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60, disable_web_page_preview=True)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply(f"<b>❌ ᴇʀʀᴏʀ..\nᴛʜɪs ғᴏʀᴡᴀʀᴅᴇᴅ ᴘᴏsᴛ ᴏʀ ᴍᴇssᴀɢᴇ ʟɪɴᴋ ɪs ɴᴏᴛ ғʀᴏᴍ ᴍʏ {channel}</b>", quote=True, disable_web_page_preview=True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("📫 Sʜᴀʀᴇ URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>›› ʙᴇʟᴏᴡ ɪs ʏᴏᴜʀ ʟɪɴᴋ:</b>\n\n{link}", quote=True, reply_markup=reply_markup, disable_web_page_preview=True)
