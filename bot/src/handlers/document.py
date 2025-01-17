from bot.src.start import Update, CallbackContext

from . import semaphore as tasks
import tempfile
from pathlib import Path
from bot.src.utils.misc import clean_text, update_dialog_messages
from bot.src.utils.proxies import (ChatAction, ParseMode, datetime, config, interaction_cache, db)

async def handle(chat, lang, update, context):
    try:
        document = update.message.document
        file_size_mb = document.file_size / (1024 * 1024)
        if file_size_mb <= config.file_max_size:
            await update.effective_chat.send_action(ChatAction.TYPING)
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_dir = Path(tmp_dir)
                ext = document.file_name.split(".")[-1]
                doc_path = tmp_dir / Path(document.file_name)
                # download
                doc_file = await context.bot.get_file(document.file_id)
                await doc_file.download_to_drive(doc_path)
                doc = await process_document(update, doc_path, ext, chat, lang)
                text = f'{config.lang["mensajes"]["document_anotado_ask"][lang]}'
                if doc[2]==True:
                    text = f'{config.lang["metagen"]["advertencia"][lang]}: {config.lang["errores"]["advertencia_tokens_excedidos"][lang]}\n\n{text}'

                new_dialog_message = {"documento": f"{document.file_name} -> content: {doc[0]}", "placeholder": ".", "date": datetime.now()}
                _ = await update_dialog_messages(chat, new_dialog_message)

                interaction_cache[chat.id] = ("visto", datetime.now())
                await db.set_chat_attribute(chat, "last_interaction", datetime.now())
        else:
            text = config.lang["errores"]["document_size_limit"][lang].replace("{file_size_mb}", f"{file_size_mb:.2f}").replace("{file_max_size}", str(config.file_max_size))
    except Exception as e:
        text = f'{config.lang["errores"]["error"][lang]}: {e}'
    finally:
        await tasks.releasemaphore(chat=chat)
        await update.message.reply_text(text, parse_mode=ParseMode.HTML)

async def process_document(update, doc_path, ext, chat, lang):
    if "pdf" in ext:
        doc = await process_pdf(update, doc_path, lang)
    else:
        with open(doc_path, 'r') as f:
            doc = f.read()
    return await clean_text(doc, chat)

async def process_pdf(update, doc_path, lang):
    pdf_file = open(doc_path, 'rb')
    import PyPDF2
    read_pdf = PyPDF2.PdfReader(pdf_file)
    doc = ''
    lim = int(config.pdf_page_lim)
    paginas = int(len(read_pdf.pages))
    if int(paginas) > int(lim):
        await update.message.reply_text(f'{config.lang["errores"]["pdf_pages_limit"][lang].format(paginas=(paginas - lim), pdf_page_lim=int(lim))}', parse_mode=ParseMode.HTML)
        paginas = int(lim)
    for i in range(paginas):
        text = read_pdf.pages[i].extract_text()
        text = text.replace(".\n", "|n_parraf|")  
        paras = text.split("|n_parraf|")
        parafo_count = 1
        for para in paras:
            if len(para) > 3:
                doc += f'{config.lang["metagen"]["paginas"][lang]}{i+1}_{config.lang["metagen"]["parrafos"][lang]}{parafo_count}: {para}\n\n'      
                parafo_count += 1
    return doc

async def wrapper(update: Update, context: CallbackContext):
    from bot.src.utils.proxies import (debe_continuar,obtener_contextos as oc, parametros, bb)
    chat, lang = await oc(update)
    await parametros(chat, lang, update)
    if not await debe_continuar(chat, lang, update, context): return
    task = bb(handle(chat, lang, update, context))
    await tasks.handle(chat, lang, task, update)