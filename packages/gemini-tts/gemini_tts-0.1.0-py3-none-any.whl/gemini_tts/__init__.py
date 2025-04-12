"""
Gemini TTS - A simple library for text-to-speech conversion using Google Gemini API
"""

from .tts import GeminiTTS, say, text_to_speech, create_client

__version__ = "0.1.0"
__all__ = ["GeminiTTS", "say", "text_to_speech", "create_client"] 