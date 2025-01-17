from . import semaphore as tasks
from bot.src.utils.misc import clean_text, update_dialog_messages
async def extract_from_url(url: str) -> str:
    from bot.src.utils.proxies import config
    import httpx
    import html2text
    headers = {
        "User-Agent": "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/113.0 Firefox/113.0"
    }
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        response = await client.get(url)
    response.raise_for_status()
    content_length = int(response.headers.get('Content-Length', 0))
    if content_length > config.url_max_size * (1024 * 1024):
        raise ValueError("lenghtexceed")
    html_content = response.text
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_images = True
    text_maker.single_line_break = True
    doc = str(text_maker.handle(html_content))
    return doc
async def handle(chat, lang, update, urls):
    from bot.src.utils.proxies import config, datetime, ChatAction, ParseMode, interaction_cache, db
    textomensaje=""
    for url in urls:
        await update.effective_chat.send_action(ChatAction.TYPING)
        try:
            textomensaje = f'{config.lang["mensajes"]["url_anotado_ask"][lang]}'
            doc = await extract_from_url(url)
            doc, _, advertencia = await clean_text(doc, chat)
            if advertencia==True:
                textomensaje = f'{config.lang["metagen"]["advertencia"][lang]}: {config.lang["errores"]["advertencia_tokens_excedidos"][lang]}\n\n{textomensaje}'
            new_dialog_message = {"url": f"{url} -> content: {doc}", "placeholder": ".", "date": datetime.now()}
            _ = await update_dialog_messages(chat, new_dialog_message)
        except ValueError as e:
            if "lenghtexceed" in str(e):
                textomensaje = f'{config.lang["errores"]["url_size_limit"][lang]}: {e}'
            else: textomensaje = f'{config.lang["errores"]["error"][lang]}: {e}'
    interaction_cache[chat.id] = ("visto", datetime.now())
    await db.set_chat_attribute(chat, "last_interaction", datetime.now())
    return textomensaje
async def wrapper(raw_msg):
    urls = []
    for entity in raw_msg.entities:
        if entity.type == 'url':
            url_add = raw_msg.text[entity.offset:entity.offset+entity.length]
            if "http://" in url_add or "https://" in url_add:
                urls.append(raw_msg.text[entity.offset:entity.offset+entity.length])
    return urls
