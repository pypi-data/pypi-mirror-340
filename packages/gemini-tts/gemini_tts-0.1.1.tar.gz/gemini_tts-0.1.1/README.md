# Gemini TTS - Қарапайым мәтіннен сөйлеуге айналдыру кітапханасы

Бұл кітапхана Google Gemini API арқылы мәтінді сөйлеуге айналдыруға арналған.

## Орнату (Installation)

### Pip арқылы орнату (болашақта)
```bash
# Негізгі функционалдылық
pip install gemini-tts

# Аудио ойнату қолдауымен (ұсынылады)
pip install gemini-tts[audio]
```

### Кодтан орнату
```bash
git clone https://github.com/dauitsuragan002/gemini-tts.git
cd gemini-tts
pip install -e .
# Аудио ойнату үшін
pip install -e .[audio]
```

## Қажетті компоненттер
- Python 3.7+
- websockets
- wave
- pygame (опционалды, аудио ойнату үшін)

## Қолдану (Usage)

### 1. Класс арқылы қолдану (ұсынылған әдіс)
```python
from gemini_tts import GeminiTTS

# Клиент жасау
client = GeminiTTS(api_key="your_api_key_here", default_voice="Puck")

# Сөйлеуге айналдыру және аудио файлын сақтау
client.say("Бұл класс арқылы жасалған мысал")

# Дауыс түрін өзгерту
client.say("Бұл басқа дауыс", voice="Kore")

# Аудионы ойнатпау
client.say("Тек файлға сақтау", play_audio=False)
```

### 2. Терең дауыстар үшін
```python
from gemini_tts import GeminiTTS

# Kore немесе Bassett дауыстары терең дауысты ерлер үшін жақсы
client = GeminiTTS(api_key="your_api_key_here", default_voice="Bassett")

# Дауысты тыңдау
client.say("Бұл терең дауыс мысалы")
```

### 3. Аудионы тікелей ойнату
```python
from gemini_tts import GeminiTTS

client = GeminiTTS(api_key="your_api_key_here")

# Мәтінді сөйлеуге айналдыру және бірден ойнату
client.say("Бұл дыбыс автоматты түрде ойнатылады", play_audio=True)
```

## Толық мысалдар

- `example.py` - негізгі функцияларды көрсетеді
- `example_minimal.py` - ең қарапайым қолдану
- `example_playback.py` - аудио ойнату мысалы

## Дауыс түрлері
Gemini API ұсынатын кейбір дауыс түрлері:
- **Ерлер дауыстары:**
  - Kore (терең)
  - Bassett (терең)
- **Әйелдер дауыстары:**
  - Puck
  - Pixie
  - Lumina
  - Orea

## Нұсқа тарихы

### v0.1.1
- Тікелей аудио ойнату қосылды
- Дауыс параметрлерін оңтайландыру (терең ерлер дауыстары үшін)
- Дауыстарды категориялар бойынша ұйымдастыру

### v0.1.0
- Алғашқы нұсқа

## Авторлар
- Әзірлеуші: David Suragan
- AI көмекші: Claude (Anthropic)

## Алғыс білдіру
Бұл жоба [agituts/gemini-2-tts](https://github.com/agituts/gemini-2-tts) репозиторийінен шабыт алды. Осы жобаның авторына шексіз алғысымызды білдіреміз.

## Лицензия
MIT
