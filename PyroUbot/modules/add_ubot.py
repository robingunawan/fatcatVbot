import asyncio
import importlib
from datetime import datetime
from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.raw.functions import functions
from PyroUbot import *

# ========== Helper ==========
async def safe_edit_message(obj, text, **kwargs):
    """Edit message aman, ignore MessageNotModified."""
    try:
        return await obj.edit_message_text(text, **kwargs)
    except pyrogram.errors.MessageNotModified:
        return

async def is_cancel(callback_query, text):
    if text.startswith("/cancel"):
        await bot.send_message(
            callback_query.from_user.id,
            "<blockquote>⎆ Pembatalan otomatis!\n⎆ Gunakan /start untuk memulai ulang</blockquote>"
        )
        return True
    return False

# ========== START ==========
@PY.BOT("start")
@PY.START
@PY.PRIVATE
async def _(client, message):
    buttons = BTN.START(message)
    msg = MSG.START(message)
    await message.reply_video(
        "https://files.catbox.moe/axrb4w.mp4",
        caption=msg,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ========== CALLBACK "bahan" ==========
@PY.CALLBACK("bahan")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        buttons = [
            [InlineKeyboardButton("⦪ Restart ⦫", callback_data="ress_ubot")],
            [InlineKeyboardButton("⦪ Kembali ⦫", callback_data=f"home {user_id}")]
        ]
        return await safe_edit_message(
            callback_query,
            "<blockquote><b>Anda sudah membuat userbot. Tekan restart jika bot tidak merespon.</b></blockquote>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        buttons = [[InlineKeyboardButton("Kembali", callback_data=f"home {user_id}")]]
        return await safe_edit_message(
            callback_query,
            f"<blockquote>☫ Maksimal userbot tercapai ({len(ubot._ubot)})</blockquote>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    premium_users, ultra_premium_users = await get_list_from_vars(client.me.id, "PREM_USERS"), await get_list_from_vars(client.me.id, "ULTRA_PREM")
    if user_id not in premium_users and user_id not in ultra_premium_users:
        buttons = [
            [InlineKeyboardButton("⦪ Lanjutkan ⦫", callback_data="bayar_dulu")],
            [InlineKeyboardButton("⦪ Kembali ⦫", callback_data=f"home {user_id}")]
        ]
        return await safe_edit_message(
            callback_query,
            MSG.POLICY(),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        buttons = [[InlineKeyboardButton("⦪ Lanjutkan ⦫", callback_data="add_ubot")]]
        return await safe_edit_message(
            callback_query,
            "<blockquote><b>Silahkan lanjutkan membuat userbot</b></blockquote>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# ========== CALLBACK "status" ==========
@PY.CALLBACK("status")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        buttons = [[InlineKeyboardButton("Kembali", callback_data=f"home {user_id}")]]
        exp = await get_expired_date(user_id)
        prefix = await get_pref(user_id)
        waktu = exp.strftime("%d-%m-%Y") if exp else "None"
        return await safe_edit_message(
            callback_query,
            f"<blockquote>⌬ Userbot Premium\n• Status: Premium\n• Prefix: {prefix[0]}\n• Expired: {waktu}</blockquote>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        buttons = [
            [InlineKeyboardButton("Beli Userbot", callback_data="bahan")],
            [InlineKeyboardButton("Kembali", callback_data=f"home {user_id}")]
        ]
        return await safe_edit_message(
            callback_query,
            "<blockquote>Anda belum membeli userbot, silakan beli terlebih dahulu.</blockquote>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# ========== CALLBACK "bayar_dulu" ==========
@PY.CALLBACK("bayar_dulu")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    buttons = BTN.PLUS_MINUS(1, user_id)
    return await safe_edit_message(
        callback_query,
        MSG.TEXT_PAYMENT(30, 30, 1),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ========== CALLBACK "add_ubot" ==========
@PY.CALLBACK("add_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.message.delete()

    # Tombol share contact
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("📞Kontak Saya", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    msg = await bot.send_message(
        user_id,
        "<blockquote>Silahkan klik tombol 📞 Kontak Saya untuk mengirimkan nomor Telegram Anda.</blockquote>",
        reply_markup=keyboard
    )

    try:
        phone = await bot.listen(user_id, timeout=300)
    except asyncio.TimeoutError:
        return await bot.send_message(
            user_id,
            "<blockquote>Pem-batalan otomatis!\nGunakan /start untuk memulai ulang</blockquote>"
        )

    if not phone.contact or not phone.contact.phone_number:
        return await bot.send_message(
            user_id,
            "<blockquote>Silahkan klik tombol 📞 Kontak Saya untuk mengirimkan nomor Telegram Anda.</blockquote>"
        )

    phone_number = phone.contact.phone_number
    await msg.delete()

    # Buat client baru
    new_client = Ubot(name=str(callback_query.id), api_id=API_ID, api_hash=API_HASH, in_memory=False)

    get_otp = await bot.send_message(user_id, "<b>⎆ Mengirim kode OTP...</b>")
    await new_client.connect()

    try:
        code = await new_client.send_code(phone_number.strip())
    except (ApiIdInvalid, PhoneNumberInvalid, PhoneNumberFlood, PhoneNumberBanned, PhoneNumberUnoccupied) as e:
        await get_otp.delete()
        return await bot.send_message(user_id, f"ERROR: {e}")
    except Exception as e:
        await get_otp.delete()
        return await bot.send_message(user_id, f"ERROR: {e}")

    await get_otp.delete()
    try:
        otp = await bot.ask(
            user_id,
            "<blockquote>Silakan periksa kode OTP dan kirim ke sini. Gunakan spasi untuk tiap digit.</blockquote>",
            timeout=300
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "<blockquote>Pem-batalan otomatis!</blockquote>")

    if await is_cancel(callback_query, otp.text):
        return

    otp_code = otp.text
    try:
        await new_client.sign_in(phone_number.strip(), code.phone_code_hash, phone_code=" ".join(str(otp_code)))
    except SessionPasswordNeeded:
        try:
            two_step_code = await bot.ask(
                user_id,
                "Akun Anda mengaktifkan verifikasi dua langkah. Kirim password Anda.\nGunakan /cancel untuk batal.",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await bot.send_message(user_id, "<blockquote>Pem-batalan otomatis!</blockquote>")

        if await is_cancel(callback_query, two_step_code.text):
            return

        try:
            await new_client.check_password(two_step_code.text)
        except Exception as e:
            return await bot.send_message(user_id, f"ERROR: {e}")

    # simpan session & start
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False
    await new_client.start()
    if user_id != new_client.me.id:
        ubot._ubot.remove(new_client)
        return await bot.send_message(user_id, "<b>Gunakan akun Telegram Anda sendiri.</b>")

    await add_ubot(user_id=int(new_client.me.id), api_id=API_ID, api_hash=API_HASH, session_string=session_string)
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"PyroUbot.modules.{mod}"))

    buttons = [[InlineKeyboardButton("Kembali", callback_data=f"home {user_id}")]]
    text_done = f"<b>Userbot berhasil diaktifkan\nNama: {new_client.me.first_name} {new_client.me.last_name or ''}\nID: {new_client.me.id}</b>"
    await bot.send_message(user_id, text_done, reply_markup=InlineKeyboardMarkup(buttons))

    # Log
    await bot.send_message(
        LOGS_MAKER_UBOT,
        f"<b>Userbot Diaktifkan</b>\nNama: {new_client.me.first_name} {new_client.me.last_name or ''}\nID: {new_client.me.id}",
        disable_web_page_preview=True
    )

# ========== CALLBACK CONTROL / RESTART / DEL ==========
@PY.BOT("control")
async def _(client, message):
    buttons = [[InlineKeyboardButton("Restart", callback_data=f"ress_ubot")]]
    await message.reply(
        "<b>Apakah anda ingin restart userbot?</b>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@PY.CALLBACK("ress_ubot")
async def _(client, callback_query):
    if callback_query.from_user.id not in ubot._get_my_id:
        return await callback_query.answer("Anda tidak punya akses", True)
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
                        return await safe_edit_message(
                            callback_query,
                            f"Restart berhasil!\nNama: {UB.me.first_name} | {UB.me.id}"
                        )
                    except Exception as error:
                        return await safe_edit_message(callback_query, f"{error}")

@PY.CALLBACK("del_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in await get_list_from_vars(client.me.id, "ADMIN_USERS"):
        return await callback_query.answer("Anda tidak punya akses tombol ini", True)
    try:
        show = await bot.get_users(callback_query.data.split()[1])
        get_id = show.id
        get_mention = f"{get_id}"
    except Exception:
        get_id = int(callback_query.data.split()[1])
        get_mention = f"{get_id}"
    for X in ubot._ubot:
        if get_id == X.me.id:
            await X.unblock_user(bot.me.username)
            await remove_ubot(X.me.id)
            ubot._get_my_id.remove(X.me.id)
            ubot._ubot.remove(X)
            await X.log_out()
            await callback_query.answer(f"{get_mention} berhasil dihapus", True)
            await safe_edit_message(
                callback_query,
                await MSG.UBOT(0),
                reply_markup=InlineKeyboardMarkup(BTN.UBOT(ubot._ubot[0].me.id, 0))
            )
            await bot.send_message(X.me.id, MSG.EXP_MSG_UBOT(X), reply_markup=InlineKeyboardMarkup(BTN.EXP_UBOT()))

# ========== CALLBACK PAGINATION ==========
@PY.CALLBACK("^(p_ub|n_ub)")
async def _(client, callback_query):
    query = callback_query.data.split()
    count = int(query[1])
    if query[0] == "n_ub":
        count = 0 if count == len(ubot._ubot) - 1 else count + 1
    elif query[0] == "p_ub":
        count = len(ubot._ubot) - 1 if count == 0 else count - 1
    await safe_edit_message(
        callback_query,
        await MSG.UBOT(count),
        reply_markup=InlineKeyboardMarkup(BTN.UBOT(ubot._ubot[count].me.id, count))
    )

# ========== CALLBACK CEK MASA AKTIF ==========
@PY.CALLBACK("cek_masa_aktif")
async def _(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    expired = await get_expired_date(user_id)
    try:
        days_left = (expired - datetime.now()).days
        await callback_query.answer(f"Tinggal {days_left} hari lagi", True)
    except:
        await callback_query.answer("Sudah tidak aktif", True)
