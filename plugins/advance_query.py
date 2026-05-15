# +++ Made By Gojo [telegram username: @ryomen_0] +++

import random
from bot import Bot
from plugins.FORMATS import *
from config import OWNER_ID, PICS
from pyrogram.enums import ChatAction
from plugins.autoDelete import convert_time
from database.database import kingdb
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto, ReplyKeyboardMarkup, ReplyKeyboardRemove    

#File setting function for retriveing modes and state of file related setting
async def fileSettings(getfunc, setfunc=None, delfunc=False) :
    btn_mode, txt_mode, pic_mode = '❌', off_txt, off_pic
    del_btn_mode = 'ᴇɴᴀʙʟᴇ ✅'
    try:
        if not setfunc:
            if await getfunc():
                txt_mode = on_txt    
                btn_mode = '✅'
                del_btn_mode = 'ᴅɪsᴀʙʟᴇ ❌'
        
            return txt_mode, (del_btn_mode if delfunc else btn_mode)
            
        else:
            if await getfunc():
                await setfunc(False)
            else:
                await setfunc(True)
                pic_mode, txt_mode = on_pic, on_txt
                btn_mode = '✅'
                del_btn_mode = 'ᴅɪsᴀʙʟᴇ ❌'
                
            return pic_mode, txt_mode, (del_btn_mode if delfunc else btn_mode)
            
    except Exception as e:
        print(f"Error occured at [fileSettings(getfunc, setfunc=None, delfunc=False)] : {e}")

#Provide or Make Button by takiing required modes and data
def buttonStatus(pc_data: str, hc_data: str, cb_data: str) -> list:
    button = [
        [
            InlineKeyboardButton(f'• ᴘᴄ: {pc_data}', callback_data='pc'),
            InlineKeyboardButton(f'• ʜᴄ: {hc_data}', callback_data='hc')
        ],
        [
            InlineKeyboardButton(f'• ᴄʙ: {cb_data}', callback_data='cb'), 
            InlineKeyboardButton(f'• sʙ •', callback_data='setcb')
        ],
        [
            InlineKeyboardButton('• ʀᴇғʀᴇsʜ', callback_data='files_cmd'), 
            InlineKeyboardButton('ᴄʟᴏsᴇ •', callback_data='close')
        ],
    ]
    return button

#Verify user, if he/she is admin or owner before processing the query...
async def authoUser(query, id, owner_only=False):
    if not owner_only:
        if not any([id == OWNER_ID, await kingdb.admin_exist(id)]):
            await query.answer("ʙʀᴜʜ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ", show_alert=True)
            return False
        return True
    else:
        if id != OWNER_ID:
            await query.answer("ʙʀᴜʜ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ", show_alert=True)
            return False
        return True

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data        
    if data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
            
    elif data == "about":
        user = await client.get_users(OWNER_ID)
        user_link = f"https://t.me/{user.username}" if user.username else f"tg://openmessage?user_id={OWNER_ID}" 
        ownername = f"<a href={user_link}>{user.first_name}</a>" if user.first_name else f"<a href={user_link}>no name !</a>"
        await query.edit_message_media(
            InputMediaPhoto("https://envs.sh/y-w.jpg", 
                            ABOUT_TXT.format(
                                botname = client.name,
                                ownername = ownername, 
                            )
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('• ʙᴀᴄᴋ', callback_data='start'), InlineKeyboardButton('sᴛᴀᴛs •', callback_data='setting')]
            ]),
        )
        
    elif data == "setting":
        await query.edit_message_media(InputMediaPhoto(random.choice(PICS), "<b>›› ᴡᴀɪᴛ ᴀ sᴇᴄᴏɴᴅ...!!</b>"))
        try:
            total_fsub = len(await kingdb.get_all_channels())
            total_admin = len(await kingdb.get_all_admins())
            total_ban = len(await kingdb.get_ban_users())
            autodel_mode = 'ᴇɴᴀʙʟᴇᴅ' if await kingdb.get_auto_delete() else 'ᴅɪsᴀʙʟᴇᴅ'
            protect_content = 'ᴇɴᴀʙʟᴇᴅ' if await kingdb.get_protect_content() else 'ᴅɪsᴀʙʟᴇᴅ'
            hide_caption = 'ᴇɴᴀʙʟᴇᴅ' if await kingdb.get_hide_caption() else 'ᴅɪsᴀʙʟᴇᴅ'
            chnl_butn = 'ᴇɴᴀʙʟᴇᴅ' if await kingdb.get_channel_button() else 'ᴅɪsᴀʙʟᴇᴅ'
            reqfsub = 'ᴇɴᴀʙʟᴇᴅ' if await kingdb.get_request_forcesub() else 'ᴅɪsᴀʙʟᴇᴅ'
            
            await query.edit_message_media(
                InputMediaPhoto(random.choice(PICS),
                                SETTING_TXT.format(
                                    total_fsub = total_fsub,
                                    total_admin = total_admin,
                                    total_ban = total_ban,
                                    autodel_mode = autodel_mode,
                                    protect_content = protect_content,
                                    hide_caption = hide_caption,
                                    chnl_butn = chnl_butn,
                                    reqfsub = reqfsub
                                )
                ),
                reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('• ʙᴀᴄᴋ', callback_data='start'), InlineKeyboardButton('ᴄʟᴏsᴇ •', callback_data='close')]
                ]),
            )
        except Exception as e:
            print(f"! Error Occured on callback data = 'setting' : {e}")
        
    elif data == "start":
        await query.edit_message_media(
            InputMediaPhoto(random.choice(PICS), 
                            START_MSG.format(
                                first = query.from_user.first_name,
                                last = query.from_user.last_name,
                                username = None if not query.from_user.username else '@' + query.from_user.username,
                                mention = query.from_user.mention,
                                id = query.from_user.id
                            )
            ),
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("•  ғᴏʀ ᴍᴏʀᴇ  •", callback_data='about')],
                    [InlineKeyboardButton("• sᴇᴛᴛɪɴɢs", callback_data='setting'),
                     InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ •", url='https://t.me/DoraShin_hlo')]
            ]),
        )
        
    elif data == "files_cmd":
        if await authoUser(query, query.from_user.id) : 
            await query.answer("Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....!!") 
                
            try:
                protect_content, pcd = await fileSettings(kingdb.get_protect_content)
                hide_caption, hcd = await fileSettings(kingdb.get_hide_caption)
                channel_button, cbd = await fileSettings(kingdb.get_channel_button)
                name, link = await kingdb.get_channel_button_link()
                
                await query.edit_message_media(
                    InputMediaPhoto(files_cmd_pic,
                                    FILES_CMD_TXT.format(
                                        protect_content = protect_content,
                                        hide_caption = hide_caption,
                                        channel_button = channel_button,
                                        name = name,
                                        link = link
                                    )
                    ),
                    reply_markup = InlineKeyboardMarkup(buttonStatus(pcd, hcd, cbd)),
                )                   
            except Exception as e:
                print(f"! Error Occured on callback data = 'files_cmd' : {e}")
            
    elif data == "pc":
        if await authoUser(query, query.from_user.id) :
            await query.answer("Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....!!") 
                
            try:
                pic, protect_content, pcd = await fileSettings(kingdb.get_protect_content, kingdb.set_protect_content)
                hide_caption, hcd = await fileSettings(kingdb.get_hide_caption)   
                channel_button, cbd = await fileSettings(kingdb.get_channel_button) 
                name, link = await kingdb.get_channel_button_link()
                
                await query.edit_message_media(
                    InputMediaPhoto(pic,
                                    FILES_CMD_TXT.format(
                                        protect_content = protect_content,
                                        hide_caption = hide_caption,
                                        channel_button = channel_button,
                                        name = name,
                                        link = link
                                    )
                    ),
                    reply_markup = InlineKeyboardMarkup(buttonStatus(pcd, hcd, cbd))
                )                   
            except Exception as e:
                print(f"! Error Occured on callback data = 'pc' : {e}")
                
    elif data == "hc":
        if await authoUser(query, query.from_user.id) :
            await query.answer("Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....!!") 
                
            try:
                protect_content, pcd = await fileSettings(kingdb.get_protect_content)
                pic, hide_caption, hcd = await fileSettings(kingdb.get_hide_caption, kingdb.set_hide_caption)   
                channel_button, cbd = await fileSettings(kingdb.get_channel_button) 
                name, link = await kingdb.get_channel_button_link()
                
                await query.edit_message_media(
                    InputMediaPhoto(pic,
                                    FILES_CMD_TXT.format(
                                        protect_content = protect_content,
                                        hide_caption = hide_caption,
                                        channel_button = channel_button,
                                        name = name,
                                        link = link
                                    )
                    ),
                    reply_markup = InlineKeyboardMarkup(buttonStatus(pcd, hcd, cbd))
                )                   
            except Exception as e:
                print(f"! Error Occured on callback data = 'hc' : {e}")
            
    elif data == "cb":
        if await authoUser(query, query.from_user.id) :
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....") 
                
            try:
                protect_content, pcd = await fileSettings(kingdb.get_protect_content)
                hide_caption, hcd = await fileSettings(kingdb.get_hide_caption)   
                pic, channel_button, cbd = await fileSettings(kingdb.get_channel_button, kingdb.set_channel_button) 
                name, link = await kingdb.get_channel_button_link()
                
                await query.edit_message_media(
                    InputMediaPhoto(pic,
                                    FILES_CMD_TXT.format(
                                        protect_content = protect_content,
                                        hide_caption = hide_caption,
                                        channel_button = channel_button,
                                        name = name,
                                        link = link
                                    )
                    ),
                    reply_markup = InlineKeyboardMarkup(buttonStatus(pcd, hcd, cbd))
                )                   
            except Exception as e:
                print(f"! Error Occured on callback data = 'cb' : {e}")
            
    elif data == "setcb":
        id = query.from_user.id
        if await authoUser(query, id) :
            await query.answer("Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....!!") 
                
            try:
                button_name, button_link = await kingdb.get_channel_button_link()
            
                button_preview = [[InlineKeyboardButton(text=button_name, url=button_link)]]  
                set_msg = await client.ask(chat_id = id, text=f'<b>ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴ, ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ᴀʀɢᴜᴍᴇɴᴛs ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ.\nFᴏʀ ᴇxᴀᴍᴘʟᴇ:\n<blockquote><code>Join Channel - https://t.me/ʙᴜᴛᴛᴏɴ480p</code></blockquote>\n\n<i>ʙᴇʟᴏᴡ ɪs ʙᴜᴛᴛᴏɴ ᴘʀᴇᴠɪᴇᴡ ⬇️</i></b>', timeout=60, reply_markup=InlineKeyboardMarkup(button_preview), disable_web_page_preview = True)
                button = set_msg.text.split(' - ')
                
                if len(button) != 2:
                    markup = [[InlineKeyboardButton(f'• sᴇᴛ ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ •', callback_data='setcb')]]
                    return await set_msg.reply("<b>ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ᴀʀɢᴜᴍᴇɴᴛs.\nғᴏʀ ᴇxᴀᴍᴘʟᴇ:\n<blockquote><code>• ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ • - https://t.me/Adult_Flux</code></blockquote>\n\n<i>ᴛʀʏ ᴀɢᴀɪɴ ʙʏ ᴄʟɪᴄᴋɪɴɢ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ..</i></b>", reply_markup=InlineKeyboardMarkup(markup), disable_web_page_preview = True)
                
                button_name = button[0].strip(); button_link = button[1].strip()
                button_preview = [[InlineKeyboardButton(text=button_name, url=button_link)]]
                
                await set_msg.reply("<b><i>ᴀᴅᴅᴇᴅ sᴜᴄcᴇssғᴜʟʟʏ ✅</i>\n<blockquote>sᴇᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴀs Pʀᴇᴠɪᴇᴡ ⬇️</blockquote></b>", reply_markup=InlineKeyboardMarkup(button_preview))
                await kingdb.set_channel_button_link(button_name, button_link)
                return
            except Exception as e:
                try:
                    await set_msg.reply(f"<b>! ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ..\n<blockquote>ʀᴇᴀsᴏɴ:</b> {e}</blockquote>")
                    print(f"! Error Occured on callback data = 'setcb' : {e}")
                except:
                    await client.send_message(id, text=f"<b>! ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ..\n<blockquote><i>ʀᴇᴀsᴏɴ: 1 minute Time out ..</i></b></blockquote>", disable_notification=True)
                    print(f"! Error Occured on callback data = 'setcb' -> Rᴇᴀsᴏɴ: 1 minute Time out ..")

    elif data == 'autodel_cmd':
        if await authoUser(query, query.from_user.id, owner_only=True) :
            await query.answer("Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....!!") 
                
            try:
                timer = convert_time(await kingdb.get_del_timer())
                autodel_mode, mode = await fileSettings(kingdb.get_auto_delete, delfunc=True)
                
                await query.edit_message_media(
                    InputMediaPhoto(autodel_cmd_pic,
                                    AUTODEL_CMD_TXT.format(
                                        autodel_mode = autodel_mode,
                                        timer = timer
                                    )
                    ),
                    reply_markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton(mode, callback_data='chng_autodel'), InlineKeyboardButton('• sᴇᴛ ᴛɪᴍᴇʀ •', callback_data='set_timer')],
                        [InlineKeyboardButton('• ʀᴇғʀᴇsʜ', callback_data='autodel_cmd'), InlineKeyboardButton('ᴄʟᴏsᴇ •', callback_data='close')]
                    ])
                )
            except Exception as e:
                print(f"! Error Occured on callback data = 'autodel_cmd' : {e}")
            
    elif data == 'chng_autodel':
        if await authoUser(query, query.from_user.id, owner_only=True) :
            await query.answer("Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....!!")
                
            try:
                timer = convert_time(await kingdb.get_del_timer())
                pic, autodel_mode, mode = await fileSettings(kingdb.get_auto_delete, kingdb.set_auto_delete, delfunc=True)
            
                await query.edit_message_media(
                    InputMediaPhoto(pic,
                                    AUTODEL_CMD_TXT.format(
                                        autodel_mode = autodel_mode,
                                        timer = timer
                                    )
                    ),
                    reply_markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton(mode, callback_data='chng_autodel'), InlineKeyboardButton('• sᴇᴛ ᴛɪᴍᴇʀ •', callback_data='set_timer')],
                        [InlineKeyboardButton('• ʀᴇғʀᴇsʜ', callback_data='autodel_cmd'), InlineKeyboardButton('ᴄʟᴏsᴇ •', callback_data='close')]
                    ])
                )
            except Exception as e:
                print(f"! Error Occured on callback data = 'chng_autodel' : {e}")

    elif data == 'set_timer':
        id = query.from_user.id
        if await authoUser(query, id, owner_only=True) :
            try:
                
                timer = convert_time(await kingdb.get_del_timer())
                set_msg = await client.ask(chat_id=id, text=f'<b><blockquote>›› ᴄᴜʀʀᴇɴᴛ ᴛɪᴍᴇʀ: {timer}</blockquote>\n\nᴛᴏ ᴄʜᴀɴɢᴇ ᴛɪᴍᴇʀ, ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ ɪɴ sᴇᴄᴏɴᴅs ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ.\n<blockquote>ғᴏʀ ᴇxᴀᴍᴘʟᴇ: <code>300</code>, <code>600</code>, <code>900</code></b></blockquote>', timeout=60)
                del_timer = set_msg.text.split()
                
                if len(del_timer) == 1 and del_timer[0].isdigit():
                    DEL_TIMER = int(del_timer[0])
                    await kingdb.set_del_timer(DEL_TIMER)
                    timer = convert_time(DEL_TIMER)
                    await set_msg.reply(f"<b><i>ᴀᴅᴅᴇᴅ sᴜᴄcᴇssғᴜʟʟʏ ✅</i>\n<blockquote>›› ᴄᴜʀʀᴇɴᴛ ᴛɪᴍᴇʀ: {timer}</blockquote></b>")
                else:
                    markup = [[InlineKeyboardButton('• sᴇᴛ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ •', callback_data='set_timer')]]
                    return await set_msg.reply("<b>ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ ɪɴ sᴇᴄᴏɴᴅs.\n<blockquote>ғᴏʀ ᴇxᴀᴍᴘʟᴇ: <code>300</code>, <code>600</code>, <code>900</code></blockquote>\n\n<i>ᴛʀʏ ᴀɢᴀɪɴ ʙʏ ᴄʟɪᴄᴋɪɴɢ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ..</i></b>", reply_markup=InlineKeyboardMarkup(markup))
    
            except Exception as e:
                try:
                    await set_msg.reply(f"<b>! ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ..\n<blockquote>ʀᴇᴀsᴏɴ:</b> {e}</blockquote>")
                    print(f"! Error Occured on callback data = 'set_timer' : {e}")
                except:
                    await client.send_message(id, text=f"<b>! ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ..\n<blockquote><i>ʀᴇᴀsᴏɴ: 1 minute Time out ..</i></b></blockquote>", disable_notification=True)
                    print(f"! Error Occured on callback data = 'set_timer' -> ʀᴇᴀsᴏɴ: 1 minute Time out ..")

    elif data == 'chng_req':
        if await authoUser(query, query.from_user.id, owner_only=True) :
            await query.answer("Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....!!")
        
            try:
                on = off = ""
                if await kingdb.get_request_forcesub():
                    await kingdb.set_request_forcesub(False)
                    off = "🔴"
                    texting = off_txt
                else:
                    await kingdb.set_request_forcesub(True)
                    on = "🟢"
                    texting = on_txt
        
                button = [
                    [InlineKeyboardButton(f"{on} ᴏɴ", "chng_req"), InlineKeyboardButton(f"{off} ᴏғғ", "chng_req")],
                    [InlineKeyboardButton("• ᴍᴏʀᴇ sᴇᴛᴛɪɴɢs •", "more_settings")]
                ]
                await query.message.edit_text(text=RFSUB_CMD_TXT.format(req_mode=texting), reply_markup=InlineKeyboardMarkup(button)) #🎉)
        
            except Exception as e:
                print(f"! Error Occured on callback data = 'chng_req' : {e}")


    elif data == 'more_settings':
        if await authoUser(query, query.from_user.id, owner_only=True) :
            #await query.answer("Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....!!")
            try:
                await query.message.edit_text("<b>›› ᴡᴀɪᴛ ᴀ sᴇᴄᴏɴᴅ...!!</b>")
                LISTS = "ᴇᴍᴘᴛʏ ʀᴇǫᴜᴇsᴛ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟ ʟɪsᴛ !?"
                
                REQFSUB_CHNLS = await kingdb.get_reqChannel()
                if REQFSUB_CHNLS:
                    LISTS = ""
                    channel_name = "<i>ᴜɴᴀʙʟᴇ ᴛᴏ ʟᴏᴀᴅ ɴᴀᴍᴇ..</i>"
                    for CHNL in REQFSUB_CHNLS:
                        await query.message.reply_chat_action(ChatAction.TYPING)
                        try:
                            name = (await client.get_chat(CHNL)).title
                        except:
                            name = None
                        channel_name = name if name else channel_name
                        
                        user = await kingdb.get_reqSent_user(CHNL)
                        channel_users = len(user) if user else 0
                        
                        link = await kingdb.get_stored_reqLink(CHNL)
                        if link:
                            channel_name = f"<a href={link}>{channel_name}</a>"
    
                        LISTS += f"NAME: {channel_name}\n(ID: <code>{CHNL}</code>)\nUSERS: {channel_users}\n\n"
                        
                buttons = [
                    [InlineKeyboardButton("ᴄʟᴇᴀʀ ᴜsᴇʀs", "clear_users"), InlineKeyboardButton("cʟᴇᴀʀ cʜᴀɴɴᴇʟs", "clear_chnls")],
                    [InlineKeyboardButton("• ʀᴇғʀᴇsʜ sᴛᴀᴛᴜs •", "more_settings")],
                    [InlineKeyboardButton("• ʙᴀᴄᴋ", "req_fsub"), InlineKeyboardButton("ᴄʟᴏsᴇ •", "close")]
                ]
                await query.message.reply_chat_action(ChatAction.CANCEL)
                await query.message.edit_text(text=RFSUB_MS_TXT.format(reqfsub_list=LISTS.strip()), reply_markup=InlineKeyboardMarkup(buttons))
                        
            except Exception as e:
                print(f"! Error Occured on callback data = 'more_settings' : {e}")


    elif data == 'clear_users':
        #if await authoUser(query, query.from_user.id, owner_only=True) :
        #await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")    
        try:
            REQFSUB_CHNLS = await kingdb.get_reqChannel()
            if not REQFSUB_CHNLS:
                return await query.answer("ᴇᴍᴘᴛʏ ʀᴇǫᴜᴇsᴛ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟ !?", show_alert=True)

            await query.answer("Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....!!")
                
            REQFSUB_CHNLS = list(map(str, REQFSUB_CHNLS))    
            buttons = [REQFSUB_CHNLS[i:i+2] for i in range(0, len(REQFSUB_CHNLS), 2)]
            buttons.insert(0, ['CANCEL'])
            buttons.append(['DELETE ALL CHANNELS USER'])

            user_reply = await client.ask(query.from_user.id, text=CLEAR_USERS_TXT, reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))
            
            if user_reply.text == 'CANCEL':
                return await user_reply.reply("<b><i>🆑 ᴄᴀɴᴄᴇʟʟᴇᴅ...</i></b>", reply_markup=ReplyKeyboardRemove())
                
            elif user_reply.text in REQFSUB_CHNLS:
                try:
                    await kingdb.clear_reqSent_user(int(user_reply.text))
                    return await user_reply.reply(f"<b><blockquote>✅ ᴜsᴇʀ ᴅᴀᴛᴀ sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʟᴇᴀʀᴇᴅ ғʀᴏᴍ ᴄʜᴀɴɴᴇʟ ɪᴅ: <code>{user_reply.text}</code></blockquote></b>", reply_markup=ReplyKeyboardRemove())
                except Exception as e:
                    return await user_reply.reply(f"<b>! ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ...\n<blockquote>ʀᴇᴀsᴏɴ:</b> {e}</blockquote>", reply_markup=ReplyKeyboardRemove())
                    
            elif user_reply.text == 'DELETE ALL CHANNELS USER':
                try:
                    for CHNL in REQFSUB_CHNLS:
                        await kingdb.clear_reqSent_user(int(CHNL))
                    return await user_reply.reply(f"<b><blockquote>✅ ᴜsᴇʀ ᴅᴀᴛᴀ sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʟᴇᴀʀᴇᴅ ғʀᴏᴍ ᴀʟʟ ᴄʜᴀɴɴᴇʟ ɪᴅs</blockquote></b>", reply_markup=ReplyKeyboardRemove())
                except Exception as e:
                    return await user_reply.reply(f"<b>! ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ...\n<blockquote>ʀᴇᴀsᴏɴ:</b> {e}</blockquote>", reply_markup=ReplyKeyboardRemove())
                    
            else:
                return await user_reply.reply(f"<b><blockquote>ɪɴᴠᴀʟɪᴅ sᴇʟᴇᴄᴛɪᴏɴ</blockquote></b>", reply_markup=ReplyKeyboardRemove())
            
        except Exception as e:
            print(f"! Error Occured on callback data = 'clear_users' : {e}")


    elif data == 'clear_chnls':
        #if await authoUser(query, query.from_user.id, owner_only=True) 
            
        try:
            REQFSUB_CHNLS = await kingdb.get_reqChannel()
            if not REQFSUB_CHNLS:
                return await query.answer("ᴇᴍᴘᴛʏ ʀᴇǫᴜᴇsᴛ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟ !?", show_alert=True)
            
            await query.answer("Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....!!")
                
            REQFSUB_CHNLS = list(map(str, REQFSUB_CHNLS))    
            buttons = [REQFSUB_CHNLS[i:i+2] for i in range(0, len(REQFSUB_CHNLS), 2)]
            buttons.insert(0, ['CANCEL'])
            buttons.append(['DELETE ALL CHANNEL IDS'])

            user_reply = await client.ask(query.from_user.id, text=CLEAR_CHNLS_TXT, reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))
            
            if user_reply.text == 'CANCEL':
                return await user_reply.reply("<b><i>🆑 ᴄᴀɴᴄᴇʟʟᴇᴅ...</i></b>", reply_markup=ReplyKeyboardRemove())
                
            elif user_reply.text in REQFSUB_CHNLS:
                try:
                    chnl_id = int(user_reply.text)

                    await kingdb.del_reqChannel(chnl_id)

                    try: await client.revoke_chat_invite_link(chnl_id, await kingdb.get_stored_reqLink(chnl_id))
                    except: pass

                    await kingdb.del_stored_reqLink(chnl_id)

                    return await user_reply.reply(f"<b><blockquote><code>{user_reply.text}</code> ᴄʜᴀɴɴᴇʟ ɪᴅ ᴀʟᴏɴɢ ᴡɪᴛʜ ɪᴛs ᴅᴀᴛᴀ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ✅</blockquote></b>", reply_markup=ReplyKeyboardRemove())
                except Exception as e:
                    return await user_reply.reply(f"<b>! ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ...\n<blockquote>ʀᴇᴀsᴏɴ:</b> {e}</blockquote>", reply_markup=ReplyKeyboardRemove())
                    
            elif user_reply.text == 'DELETE ALL CHANNEL IDS':
                try:
                    for CHNL in REQFSUB_CHNLS:
                        chnl = int(CHNL)

                        await kingdb.del_reqChannel(chnl)

                        try: await client.revoke_chat_invite_link(chnl, await kingdb.get_stored_reqLink(chnl))
                        except: pass

                        await kingdb.del_stored_reqLink(chnl)

                    return await user_reply.reply(f"<b><blockquote>ᴀʟʟ ᴄʜᴀɴɴᴇʟ ɪᴅs ᴀʟᴏɴɢ ᴡɪᴛʜ ɪᴛs ᴅᴀᴛᴀ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ✅</blockquote></b>", reply_markup=ReplyKeyboardRemove())
                
                except Exception as e:
                    return await user_reply.reply(f"<b>! ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ...\n<blockquote>ʀᴇᴀsᴏɴ:</b> {e}</blockquote>", reply_markup=ReplyKeyboardRemove())
                    
            else:
                return await user_reply.reply(f"<b><blockquote>ɪɴᴠᴀʟɪᴅ sᴇʟᴇᴄᴛɪᴏɴs</blockquote></b>", reply_markup=ReplyKeyboardRemove())
        
        except Exception as e:
            print(f"! Error Occured on callback data = 'more_settings' : {e}")



    elif data == 'clear_links':
        #if await authoUser(query, query.from_user.id, owner_only=True) :
        #await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")
            
        try:
            REQFSUB_CHNLS = await kingdb.get_reqLink_channels()
            if not REQFSUB_CHNLS:
                return await query.answer("ɴᴏ sᴛᴏʀᴇᴅ ʀᴇǫᴜᴇsᴛ ʟɪɴᴋ ᴀᴠᴀɪʟᴀʙʟᴇ !?", show_alert=True)

            await query.answer("Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....!!")
                
            REQFSUB_CHNLS = list(map(str, REQFSUB_CHNLS))    
            buttons = [REQFSUB_CHNLS[i:i+2] for i in range(0, len(REQFSUB_CHNLS), 2)]
            buttons.insert(0, ['CANCEL'])
            buttons.append(['DELETE ALL REQUEST LINKS'])

            user_reply = await client.ask(query.from_user.id, text=CLEAR_LINKS_TXT, reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))
            
            if user_reply.text == 'CANCEL':
                return await user_reply.reply("<b><i>🆑 ᴄᴀɴᴄᴇʟʟᴇᴅ...</i></b>", reply_markup=ReplyKeyboardRemove())
                
            elif user_reply.text in REQFSUB_CHNLS:
                channel_id = int(user_reply.text)
                try:
                    try:
                        await client.revoke_chat_invite_link(channel_id, await kingdb.get_stored_reqLink(channel_id))
                    except:
                        text = """<b>❌ ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴠᴏᴋᴇ ʟɪɴᴋ !
<blockquote expandable>ɪᴅ: <code>{}</code></b>
<i>ᴇɪᴛʜᴇʀ ᴛʜᴇ ʙᴏᴛ ɪs ɴᴏᴛ ɪɴ ᴀʙᴏᴠᴇ ᴄʜᴀɴɴᴇʟ ᴏʀ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘʀᴏᴘᴇʀ ᴀᴅᴍɪɴ ᴘᴇʀᴍɪssɪᴏɴs</i></blockquote>"""
                        return await user_reply.reply(text=text.format(channel_id), reply_markup=ReplyKeyboardRemove())
                        
                    await kingdb.del_stored_reqLink(channel_id)
                    return await user_reply.reply(f"<b><blockquote><code>{channel_id}</code> ᴄʜᴀɴɴᴇʟs ʟɪɴᴋ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ✅</blockquote></b>", reply_markup=ReplyKeyboardRemove())
                
                except Exception as e:
                    return await user_reply.reply(f"<b>! ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ...\n<blockquote>ʀᴇᴀsᴏɴ:</b> {e}</blockquote>", reply_markup=ReplyKeyboardRemove())
                    
            elif user_reply.text == 'DELETE ALL REQUEST LINKS':
                try:
                    result = ""
                    for CHNL in REQFSUB_CHNLS:
                        channel_id = int(CHNL)
                        try:
                            await client.revoke_chat_invite_link(channel_id, await kingdb.get_stored_reqLink(channel_id))
                        except:
                            result += f"<blockquote expandable><b><code>{channel_id}</code> ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴠᴏᴋᴇ ❌</b>\n<i>ᴇɪᴛʜᴇʀ ᴛʜᴇ ʙᴏᴛ ɪs ɴᴏᴛ ɪɴ ᴀʙᴏᴠᴇ ᴄʜᴀɴɴᴇʟ ᴏʀ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘʀᴏᴘᴇʀ ᴀᴅᴍɪɴ ᴘᴇʀᴍɪssɪᴏɴs.</i></blockquote>\n"
                            continue
                        await kingdb.del_stored_reqLink(channel_id)
                        result += f"<blockquote><b><code>{channel_id}</code> IDs ʟɪɴᴋ ᴅᴇʟᴇᴛᴇᴅ ✅</b></blockquote>\n"
                        
                    return await user_reply.reply(f"<b>⁉️ ᴏᴘᴇʀᴀᴛɪᴏɴ ʀᴇsᴜʟᴛ:</b>\n{result.strip()}", reply_markup=ReplyKeyboardRemove())
 
                except Exception as e:
                    return await user_reply.reply(f"<b>! ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ...\n<blockquote>ʀᴇᴀsᴏɴ:</b> {e}</blockquote>", reply_markup=ReplyKeyboardRemove())
                    
            else:
                return await user_reply.reply(f"<b><blockquote>ɪɴᴠᴀʟɪᴅ sᴇʟᴇᴄᴛɪᴏɴs</blockquote></b>", reply_markup=ReplyKeyboardRemove())
            
        except Exception as e:
            print(f"! Error Occured on callback data = 'more_settings' : {e}")
            

    elif data == 'req_fsub':
        #if await authoUser(query, query.from_user.id, owner_only=True) :
        await query.answer("Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....!!")
    
        try:
            on = off = ""
            if await kingdb.get_request_forcesub():
                on = "🟢"
                texting = on_txt
            else:
                off = "🔴"
                texting = off_txt
    
            button = [
                [InlineKeyboardButton(f"{on} ᴏɴ", "chng_req"), InlineKeyboardButton(f"{off} ᴏғғ", "chng_req")],
                [InlineKeyboardButton("• ᴍᴏʀᴇ sᴇᴛᴛɪɴɢs •", "more_settings")]
            ]
            await query.message.edit_text(text=RFSUB_CMD_TXT.format(req_mode=texting), reply_markup=InlineKeyboardMarkup(button)) #🎉)
    
        except Exception as e:
            print(f"! Error Occured on callback data = 'chng_req' : {e}")
        
            
                
                    
                 
# +++ Made By Gojo [telegram username: @ryomen_0] +++
