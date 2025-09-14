import asyncio
import importlib
from datetime import datetime

from pyrogram import Client
from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from PyroUbot import *

# =======================================
# START COMMAND
# =======================================
@PY.BOT("start")
@PY.START
@PY.PRIVATE
async def start_handler(client, message):
    buttons = BTN.START(message)
    msg = MSG.START(message)
    await message.reply_video(
        "https://files.catbox.moe/axrb4w.mp4",
        caption=msg,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# =======================================
# CALLBACK "bahan"
# =======================================
@PY.CALLBACK("bahan")
async def bahan_handler(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        buttons = [
            [InlineKeyboardButton("⦪ ʀᴇꜱᴛᴀʀᴛ ⦫", callback_data="ress_ubot")],
            [InlineKeyboardButton("⦪ ᴋᴇᴍʙᴀʟɪ ⦫", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            "<b>Anda sudah membuat userbot. Tekan restart jika bermasalah.</b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        buttons = [[InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")]]
        return await callback_query.edit_message_text(
            f"<b>Maksimal userbot ({MAX_BOT}) telah tercapai!</b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    premium_users = await get_list_from_vars(client.me.id, "PREM_USERS")
    ultra_premium_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")
    if user_id not in premium_users and user_id not in ultra_premium_users:
        buttons = [
            [InlineKeyboardButton("⦪ ʟᴀɴᴊᴜᴛᴋᴀɴ ⦫", callback_data="bayar_dulu")],
            [InlineKeyboardButton("⦪ ᴋᴇᴍʙᴀʟɪ ⦫", callback_data=f"home {user_id}")]
        ]
        return await callback_query.edit_message_text(
            MSG.POLICY(),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        buttons = [[InlineKeyboardButton("⦪ ʟᴀɴᴊᴜᴛᴋᴀɴ ⦫", callback_data="add_ubot")]]
        return await callback_query.edit_message_text(
            "<b>Silahkan tekan lanjutkan untuk membuat userbot.</b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# =======================================
# CALLBACK "bayar_dulu"
# =======================================
@PY.CALLBACK("bayar_dulu")
async def bayar_dulu_handler(client, callback_query):
    user_id = callback_query.from_user.id
    buttons = BTN.PLUS_MINUS(1, user_id)
    return await callback_query.edit_message_text(
        MSG.TEXT_PAYMENT(30, 30, 1),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )

# =======================================
# CALLBACK "add_ubot"
# =======================================
@PY.CALLBACK("add_ubot")
async def add_ubot_handler(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.message.delete()

    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("📞Kontak Saya", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    msg = await bot.send_message(
        user_id,
        "<b>Klik tombol 📞 Kontak Saya untuk mengirim nomor Telegram Anda.</b>",
        reply_markup=keyboard
    )

    try:
        phone = await bot.listen(user_id, timeout=300)
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "<b>Pem-batalan otomatis. Gunakan /start untuk memulai ulang.</b>")

    if not phone.contact or not phone.contact.phone_number:
        return await bot.send_message(user_id, "<b>Harap kirim nomor dengan tombol kontak Telegram.</b>")

    phone_number = phone.contact.phone_number
    await msg.delete()

    new_client = Ubot(
        name=str(callback_query.id),
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=False
    )

    get_otp = await bot.send_message(user_id, "<b>Mengirim kode OTP...</b>")
    await new_client.connect()

    try:
        code = await new_client.send_code(phone_number.strip())
    except Exception as e:
        await get_otp.delete()
        return await bot.send_message(user_id, f"ERROR: {e}")

    await get_otp.delete()
    try:
        otp = await bot.ask(
            user_id,
            "<b>Kirim kode OTP dari akun resmi Telegram. Tambahkan spasi antar digit.</b>",
            timeout=300
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "<b>Pem-batalan otomatis. Gunakan /start untuk memulai ulang.</b>")

    if otp.text.startswith("/cancel"):
        return

    otp_code = otp.text
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code))
        )
    except SessionPasswordNeeded:
        two_step_code = await bot.ask(user_id, "<b>Masukkan password 2FA akun Anda.</b>", timeout=300)
        try:
            await new_client.check_password(two_step_code.text)
        except Exception as e:
            return await bot.send_message(user_id, f"ERROR: {e}")

    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False

    await add_ubot(
        user_id=int(new_client.me.id),
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string
    )

    for mod in loadModule():
        importlib.reload(importlib.import_module(f"PyroUbot.modules.{mod}"))

    buttons = [[InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")]]
    text_done = f"""
<b>Berhasil diaktifkan!</b>
• Nama: <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name}</a>
• ID: {new_client.me.id}
"""
    await bot.send_message(user_id, text_done, reply_markup=InlineKeyboardMarkup(buttons))

# =======================================
# CALLBACK "ress_ubot" (Restart)
# =======================================
@PY.CALLBACK("ress_ubot")
async def ress_ubot_handler(client, callback_query):
    if callback_query.from_user.id not in ubot._get_my_id:
        return await callback_query.answer("You don't have access", True)

    for X in ubot._ubot:
        if callback_query.from_user.id == X.me.id:
            for _ubot_ in await get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        ubot._ubot.remove(X)
                        ubot._get_my_id.remove(X.me.id)
                        UB = Ubot(**_ubot_)
                        await UB.start()
                        for mod in loadModule():
                            importlib.reload(importlib.import_module(f"PyroUbot.modules.{mod}"))
                        return await callback_query.edit_message_text(
                            f"⎆ Restart berhasil!\nNama: {UB.me.first_name} | {UB.me.id}"
                        )
                    except Exception as error:
                        return await callback_query.edit_message_text(f"{error}")

# =======================================
# CALLBACK "cek_masa_aktif"
# =======================================
@PY.CALLBACK("cek_masa_aktif")
async def cek_masa_aktif_handler(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    expired = await get_expired_date(user_id)
    try:
        remaining = (expired - datetime.now()).days
        return await callback_query.answer(f"Tinggal {remaining} hari lagi", True)
    except:
        return await callback_query.answer("Sudah tidak aktif", True)

# =======================================
# CALLBACK "del_ubot"
# =======================================
@PY.CALLBACK("del_ubot")
async def del_ubot_handler(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in await get_list_from_vars(client.me.id, "ADMIN_USERS"):
        return await callback_query.answer("Tidak punya akses", True)

    try:
        show = await bot.get_users(callback_query.data.split()[1])
        get_id = show.id
    except Exception:
        get_id = int(callback_query.data.split()[1])

    for X in ubot._ubot:
        if get_id == X.me.id:
            await remove_ubot(X.me.id)
            ubot._get_my_id.remove(X.me.id)
            ubot._ubot.remove(X)
            await X.log_out()
            await callback_query.answer(f"{get_id} berhasil dihapus", True)
            await callback_query.edit_message_text(await MSG.UBOT(0), reply_markup=InlineKeyboardMarkup(BTN.UBOT(ubot._ubot[0].me.id, 0)))
            await bot.send_message(X.me.id, MSG.EXP_MSG_UBOT(X), reply_markup=InlineKeyboardMarkup(BTN.EXP_UBOT()))

# =======================================
# CALLBACK Pagination ubot
# =======================================
@PY.CALLBACK("^(p_ub|n_ub)")
async def pagination_ubot(client, callback_query):
    query = callback_query.data.split()
    count = int(query[1])
    if query[0] == "n_ub":
        count = 0 if count == len(ubot._ubot) - 1 else count + 1
    elif query[0] == "p_ub":
        count = len(ubot._ubot) - 1 if count == 0 else count - 1

    await callback_query.edit_message_text(
        await MSG.UBOT(count),
        reply_markup=InlineKeyboardMarkup(BTN.UBOT(ubot._ubot[count].me.id, count))
    )
