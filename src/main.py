import os
import logging
import json
import pathlib
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

# Configuración de Logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Cargar variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

# Funciones de procesamiento de texto con IA
def process_text_with_ai(transcription_text):
    """
    Toma texto desordenado y usa GPT-4o-mini para extraer tareas estructuradas en JSON.
    """
    
    # Prompt para el modelo
    system_prompt = """
    Eres un asistente personal experto en productividad (GTD).
    Tu trabajo es analizar la transcripción de una nota de voz.
    
    Debes extraer:
    1. Un resumen muy breve de la nota.
    2. Una lista de tareas accionables.
    
    IMPORTANTE: Debes responder EXCLUSIVAMENTE en formato JSON con esta estructura:
    {
        "summary": "Resumen del audio aquí...",
        "tasks": [
            {
                "title": "Título de la tarea (verbo + acción)",
                "priority": "Alta/Media/Baja",
                "type": "Personal/Trabajo/Idea"
            }
        ]
    }
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini", # Modelo
        response_format={"type": "json_object"}, # Forzamos que devuelva JSON válido
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcription_text}
        ]
    )

    # Convertimos la respuesta de texto a un diccionario de Python real
    return json.loads(response.choices[0].message.content)


# Handlers de Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="¡Hola! Envíame un audio con tareas y las organizaré por ti."
    )

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    status_msg = await context.bot.send_message(chat_id=chat_id, text="Descargando audio...")

    try:
        # Descargar audio
        new_file = await context.bot.get_file(update.message.voice.file_id)
        file_path = pathlib.Path(f"voice_{user_id}.ogg")
        await new_file.download_to_drive(custom_path=file_path)
        
        # Transcribir audio
        await context.bot.edit_message_text(chat_id=chat_id, message_id=status_msg.message_id, text="Escuchando...")
        
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        text_transcribed = transcript.text
        
        # Procesar texto con IA
        await context.bot.edit_message_text(chat_id=chat_id, message_id=status_msg.message_id, text="Procesando y analizando tareas...")
        
        structured_data = process_text_with_ai(text_transcribed)
        
        # Formatear respuesta para Telegram
        summary = structured_data.get("summary", "Sin resumen")
        tasks = structured_data.get("tasks", [])
        
        response_text = f"**Resumen:** {summary}\n\n **Tareas Detectadas:**\n"
        for task in tasks:
            response_text += f"- [{task['priority']}] {task['title']} ({task['type']})\n"
            
        # Imprimir el JSON en la terminal
        print("\n--- JSON GENERADO ---")
        print(json.dumps(structured_data, indent=2, ensure_ascii=False))
        print("---------------------\n")

        await context.bot.send_message(chat_id=chat_id, text=response_text)

    except Exception as e:
        logging.error(f"ERROR: {e}", exc_info=True)
        await context.bot.send_message(chat_id=chat_id, text="Algo salió mal procesando los datos.")
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    
    print("Iniciando Scriba Assistant...")
    application.run_polling()
