from bot.src.start import Update, CallbackContext
from datetime import datetime
from pathlib import Path
import tempfile
from . import semaphore as tasks
from ..utils.misc import clean_text, update_dialog_messages
async def handle(chat, lang, update, context):
    from bot.src.utils.proxies import (
    ChatAction, ParseMode, config,
    interaction_cache, db
    )
    image = update.message.photo[-1]
    from PIL import Image
    import pytesseract
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            await update.effective_chat.send_action(ChatAction.TYPING)
            tmp_dir = Path(tmp_dir)
            img_path = tmp_dir / Path("ocrimagen.jpg")
            image_file = await context.bot.get_file(image.file_id)
            await image_file.download_to_drive(img_path)
            imagen = Image.open(str(img_path))
            doc = pytesseract.image_to_string(imagen, timeout=50, lang='spa+ara+eng+jpn+chi+deu+fra+rus+por+ita+nld', config='--psm 3')
            interaction_cache[chat.id] = ("visto", datetime.now())
            await db.set_chat_attribute(chat, "last_interaction", datetime.now())
            if len(doc) <= 1:
                text = f'{config.lang["errores"]["error"][lang]}: {config.lang["errores"]["ocr_no_extract"][lang]}'
            else:
                text = config.lang["mensajes"]["image_ocr_ask"][lang].format(ocresult=doc)
                doc, _, advertencia = await clean_text(doc, chat)
                if advertencia==True:
                    text = f'{config.lang["metagen"]["advertencia"][lang]}: {config.lang["errores"]["advertencia_tokens_excedidos"][lang]}\n\n{text}'
                new_dialog_message = {"user": f'{config.lang["metagen"]["transcripcion_imagen"][lang]}: "{doc}"', "date": datetime.now()}
                _ = await update_dialog_messages(chat, new_dialog_message)
    except RuntimeError:
        text = f'{config.lang["errores"]["error"][lang]}: {config.lang["errores"]["tiempoagotado"][lang]}'
    await update.message.reply_text(f'{text}', parse_mode=ParseMode.MARKDOWN)
    await tasks.releasemaphore(chat=chat)
async def wrapper(update: Update, context: CallbackContext):
    from bot.src.utils.proxies import (debe_continuar,obtener_contextos as oc, parametros, bb)
    if not update.effective_message.photo: return
    chat, lang = await oc(update)
    await parametros(chat, lang, update)
    if not await debe_continuar(chat, lang, update, context): return
    task = bb(handle(chat, lang, update, context))
    await tasks.handle(chat, lang, task, update)

