**Origin repo: <a href="https://github.com/karfly/chatgpt_telegram_bot" alt="Karfly">Karfly/chatgpt_telegram_bot</a>**

## Nueva actualización:
- Soporte de lectura de archivos de texto, PDF y de enlaces.
- Se reemplazó el modo "👩‍🎨 Artista básico" con el comando /img.
- <a href="https://github.com/karfly/chatgpt_telegram_bot/pull/112/commits/d54809aeb89a1921f6cfdffc00a4d1ee4744c8d2" alt="Dialog_ask">Preguntar si iniciar nueva conversación si lleva tiempo sin chatear</a> (TIMEOUT_ASK y DIALOG_TIMEOUT en docker-compose.yml)
- Si la api actual del usuario no soporta voz o imagen, se usará una api predefinida.
- <a href="https://github.com/karfly/chatgpt_telegram_bot/pull/188" alt="AutoDel">Borrar historiales antiguos al usar /new.</a>
- La transcripción de mensajes de voz ahora también funciona para archivos de audio.
- Añadidas variables a docker-compose para limitar el tamaño de los audios, documentos, paginas de PDF y urls.
- Apis de GPT4Free (necesita especificar las cookies en docker-compose para usar Bing y ChatGPT)

## Cambios anteriores en esta modificación:
- Traducción al español
- Base en Minideb.
- Se eliminó el seguimiento de tokens.
- Necesita base de datos mongo externa.
- Sólo hay mensajes en tiempo real, no hay envío de mensaje fijo
- **Añade la cantidad de APIs y modelos que quieras!**
- Un menú genérico para los tipos de opciones
- "Simplificación" de ciertas partes del código
- Se añadió un comando /reboot para reiniciar el sistema Docker (está roto), los permisos del usuario se declaran en docker-compose.yml en la variable sudo_users
- Cambio de API por usuario!
- El generador de imágenes envía las imágenes comprimidas y en formato sin comprimir (archivo) 

# Importante:
- Las API personalizadas deben seguir la misma estructura de OpenAI, es decir, el "https://dominio.dom/v1/..."

## Comandos
- /new - Iniciar nuevo diálogo.
- /img - Generar imagenes.
- /retry - Regenera la última respuesta del bot.
- /chat_mode - Seleccionar el modo de conversación.
- /model - Mostrar modelos IA.
- /api - Mostrar APIs.
- /help – Mostrar este mensaje de nuevo.

## Setup
1. Obtén tu clave de [OpenAI API](https://openai.com/api/)

2. Obtén tu token de bot de Telegram de [@BotFather](https://t.me/BotFather)

3. Edita `config/api.example.yml` para configurar tu OpenAI-API-KEY o añadir apis personalizadas

4. Añade tu token de telegram, base de datos Mongo, modifica otras variables en 'docker-compose.example.yml' y renombra `docker-compose.example.yml` a `docker-compose.yml`

5. 🔥 Y ahora **ejecuta**:
    ```bash
    docker-compose up --build
    ```