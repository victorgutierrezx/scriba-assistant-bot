# Bot de Tareas Inteligente para Telegram

Herramienta de automatización desarrollada en **Python** que actúa como un asistente personal de productividad. Recibe notas de voz a través de Telegram, las transcribe y extrae automáticamente tareas estructuradas utilizando la inteligencia artificial de **OpenAI**.

## 📋 Características

-   **Transcripción de Audio:** Utiliza el modelo **Whisper-1** para convertir notas de voz en texto con alta precisión.
-   **Análisis Inteligente:** Emplea **GPT-4o-mini** para interpretar el contexto, resumir el contenido y detectar tareas accionables.
-   **Salida Estructurada (GTD):** Clasifica las tareas automáticamente por:
    -   Prioridad (Alta/Media/Baja)
    -   Tipo (Personal/Trabajo/Idea)
-   **Privacidad:** Los archivos de audio se eliminan automáticamente del servidor local tras ser procesados.
-   **Feedback Inmediato:** Responde en el chat con un resumen y la lista de tareas formateada, mientras muestra el JSON en la terminal.

------------------------------------------------------------------------

## 📦 Requisitos

-   Python **3.8 o superior**
-   Una cuenta de Telegram y un Bot Token (debes crearlo en el chat de Telegram de @BotFather)
-   Una API Key de OpenAI (con crédito disponible)
-   FFmpeg (generalmente necesario para el manejo de audio en el sistema)

------------------------------------------------------------------------

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone [https://github.com/victorgutierrezx/telegram-ai-bot.git](https://github.com/victorgutierrezx/telegram-ai-bot.git)
cd telegram-ai-bot
```

### 2. Crear y activar entorno virtual

**Windows**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Modifica el archivo llamado .env en la raíz del proyecto y añade tus credenciales:
TELEGRAM_TOKEN=<agregar-token>
OPENAI_API_KEY=<agregar-api-key>

------------------------------------------------------------------------

## ▶️ Uso

### 1. Iniciar el Bot

Accede a la directorio /src jecuta el script principal:
```bash
cd src
python main.py
```

### 2. Interactuar en Telegram

1. Busca tu bot en Telegram y pulsa Start.
2. Envíale una nota de voz contando tus tareas pendientes (ej: "Mañana tengo que llamar urgentemente al cliente de Santander a las 9 y comprar leche al volver a casa").

### 3. Revisar resultados
- En Telegram: Recibirás un mensaje de texto con el resumen y las tareas organizadas con iconos.
- En la Terminal: Verás el objeto JSON estructurado que generó la IA.

------------------------------------------------------------------------

## 📁 Estructura del Proyecto

    telegram_bot/
    ├── .env                 # Variables de entorno (Token y Key)
    ├── main.py              # Lógica del bot y conexión con OpenAI
    ├── requirements.txt     # Dependencias
    └── README.md



------------------------------------------------------------------------

## 📩 Contacto

**Email:** contacto@victorgutierrez.dev **Autor:** Víctor Gutiérrez
