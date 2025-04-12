# Gemini TTS - Қарапайым мәтіннен сөйлеуге айналдыру кітапханасы

Бұл кітапхана Google Gemini API арқылы мәтінді сөйлеуге айналдыруға арналған.

## Орнату (Installation)

### Pip арқылы орнату (болашақта)
```
pip install gemini-tts
```

### Кодтан орнату
```
git clone https://github.com/davidsuragan/gemini-tts.git
cd gemini-tts
pip install -e .
```

## Қажетті компоненттер
- Python 3.7+
- websockets
- wave

## Қолдану (Usage)

### 1. Класс арқылы қолдану (ұсынылған әдіс)
```python
from gemini_tts import GeminiTTS

# Клиент жасау
client = GeminiTTS(api_key="your_api_key_here", default_voice="Puck")

# Сөйлеуге айналдыру
client.say("Бұл класс арқылы жасалған мысал")

# Дауыс түрін өзгерту
client.say("Бұл басқа дауыс", voice="Kore")

# Басқа файл атын қолдану
client.say("Бұл басқа файлға сақталады", output_file="other_output.wav")
```

### 2. Қарапайым функция қолдану
```python
from gemini_tts import say

# API кілтін тікелей беру
say("Сәлем, тікелей API кілтімен", api_key="your_api_key_here")

# API кілтін қоршаған ортадан алу (GOOGLE_API_KEY айнымалысы)
say("Сіздің мәтініңіз осында")
```

### 3. Асинхронды әдісті қолдану
```python
import asyncio
from gemini_tts import GeminiTTS

client = GeminiTTS(api_key="your_api_key_here")

async def main():
    # Асинхронды әдісті қолдану
    await client.text_to_speech_async(
        "Бұл асинхронды функцияны қолдану мысалы", 
        output_file="audio.wav", 
        voice="Puck"
    )

asyncio.run(main())
```

## Толық мысал

`example.py` файлы кітапхананы қалай қолдануға болатынын көрсетеді.

## Дауыс түрлері
Gemini API ұсынатын кейбір дауыс түрлері:
- Puck
- Kore
- Bassett
- Pixie
- Lumina
- Orea

## Авторлар
- Әзірлеуші: David Suragan
- AI көмекші: Claude (Anthropic)

## Алғыс білдіру
Бұл жоба [agituts/gemini-2-tts](https://github.com/agituts/gemini-2-tts) репозиторийінен шабыт алды. Осы жобаның авторына шексіз алғысымызды білдіреміз.

## Лицензия
MIT
