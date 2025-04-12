"""
Core functionality for text-to-speech conversion using Google Gemini API
"""

import os
import base64
import json
import asyncio
import websockets
import wave
from typing import Optional, Tuple, Dict, Any

try:
    # Try to import audio playback library, but make it optional
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


class GeminiTTS:
    """
    A class for converting text to speech using Google Gemini API
    """
    
    def __init__(self, api_key: Optional[str] = None, default_voice: str = 'Puck'):
        """
        Initialize the GeminiTTS client
        
        Args:
            api_key: Google API key for Gemini. If None, will try to get from GOOGLE_API_KEY env var
            default_voice: Default voice to use for TTS
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.default_voice = default_voice or os.getenv('DEFAULT_VOICE', 'Puck')
        
        if not self.api_key:
            raise ValueError("API key must be provided either directly or via GOOGLE_API_KEY environment variable")
    
    def _get_voice_settings(self, voice: str) -> Dict[str, Any]:
        """Get the voice settings for the specified voice"""
        # Default settings
        settings = {
            "voice_config": {
                "prebuilt_voice_config": {
                    "voice_name": voice
                }
            }
        }
        
        # For deeper male voices
        if voice in ["Kore", "Bassett"]:
            settings["speaking_rate"] = 0.9
            settings["pitch"] = -2.0  # Lower pitch for deeper voice
            
        # For more natural female voices
        elif voice in ["Puck", "Lumina"]:
            settings["speaking_rate"] = 1.0
            
        return settings
    
    async def text_to_speech_async(self, text: str, output_file: str = 'output.wav', 
                                  voice: Optional[str] = None) -> str:
        """
        Convert text to speech using Google Gemini API (async version)
        
        Args:
            text: The text to convert to speech
            output_file: Path to save the output audio file
            voice: Voice name to use for text-to-speech. If None, default_voice will be used.
                Available voices include: Puck, Kore, Bassett, Pixie, Lumina, Orea
        
        Returns:
            Path to the saved audio file
        """
        if voice is None:
            voice = self.default_voice
            
        # API configuration
        host = 'generativelanguage.googleapis.com'
        model = "gemini-2.0-flash-exp"
        uri = f"wss://{host}/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key={self.api_key}"
        
        # Get specific voice settings
        voice_settings = self._get_voice_settings(voice)
        
        # Connect to WebSocket
        async with websockets.connect(uri) as ws:
            # Setup message
            setup_msg = {
                "setup": {
                    "model": f"models/{model}",
                    "generation_config": {
                        "speech_config": voice_settings
                    }
                }
            }
            await ws.send(json.dumps(setup_msg))
            await ws.recv()  # Read setup response
            
            # Send text to convert
            msg = {
                "client_content": {
                    "turn_complete": True,
                    "turns": [
                        {"role": "user", "parts": [{"text": text}]}
                    ]
                }
            }
            await ws.send(json.dumps(msg))
            
            # Receive audio data
            complete_audio = bytearray()
            
            async for raw_response in ws:
                response = json.loads(raw_response)
                
                # Process audio data
                try:
                    parts = response["serverContent"]["modelTurn"]["parts"]
                    for part in parts:
                        if "inlineData" in part:
                            b64data = part["inlineData"]["data"]
                            pcm_data = base64.b64decode(b64data)
                            complete_audio.extend(pcm_data)
                except KeyError:
                    pass
                    
                # Check for completion
                try:
                    if response["serverContent"].get("turnComplete", False):
                        break
                except KeyError:
                    pass
            
            if not complete_audio:
                raise ValueError("No audio data received from API")
                    
            # Save to WAV file
            with wave.open(output_file, 'wb') as wav_file:
                wav_file.setnchannels(2)  # Stereo
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(24000)  # 24kHz
                wav_file.writeframes(complete_audio)
                
            print(f"Audio saved to {output_file}")
            return output_file
    
    def text_to_speech(self, text: str, output_file: str = 'output.wav', voice: Optional[str] = None) -> str:
        """
        Convert text to speech using Google Gemini API (synchronous version)
        
        Args:
            text: The text to convert to speech
            output_file: Path to save the output audio file
            voice: Voice name to use for text-to-speech. If None, default_voice will be used.
                Available voices include: Puck, Kore, Bassett, Pixie, Lumina, Orea
        
        Returns:
            Path to the saved audio file
        """
        return asyncio.run(self.text_to_speech_async(text, output_file, voice))
    
    def say(self, text: str, output_file: str = 'output.wav', voice: Optional[str] = None, 
            play_audio: bool = True) -> str:
        """
        Simple alias for text_to_speech with option to play the audio immediately
        
        Args:
            text: The text to convert to speech
            output_file: Path to save the output audio file
            voice: Voice name to use for text-to-speech. If None, default_voice will be used.
                Available voices include: Puck, Kore, Bassett, Pixie, Lumina, Orea
            play_audio: Whether to play the audio immediately after generation
        
        Returns:
            Path to the saved audio file
        """
        file_path = self.text_to_speech(text, output_file, voice)
        
        if play_audio:
            self.play_audio(file_path)
            
        return file_path
    
    def play_audio(self, audio_file: str) -> None:
        """
        Play an audio file
        
        Args:
            audio_file: Path to the audio file to play
        """
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
            
        if PYGAME_AVAILABLE:
            pygame.mixer.init(frequency=24000)
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        else:
            print(f"Audio file created at {audio_file}")
            print("To play audio, install pygame: pip install pygame")
            
            # Try to play with the system default player as fallback
            try:
                if os.name == 'nt':  # Windows
                    os.system(f'start {audio_file}')
                elif os.name == 'posix':  # macOS or Linux
                    if os.uname().sysname == 'Darwin':  # macOS
                        os.system(f'open {audio_file}')
                    else:  # Linux
                        os.system(f'xdg-open {audio_file}')
            except Exception:
                pass


# Create module-level functions that use a default client for convenience
def create_client(api_key: Optional[str] = None, default_voice: str = 'Puck') -> GeminiTTS:
    """Create a new GeminiTTS client"""
    return GeminiTTS(api_key, default_voice)

def text_to_speech(text: str, output_file: str = 'output.wav', voice: Optional[str] = None, 
                   api_key: Optional[str] = None) -> str:
    """Module-level convenience function for text-to-speech conversion"""
    client = create_client(api_key)
    return client.text_to_speech(text, output_file, voice)

def say(text: str, output_file: str = 'output.wav', voice: Optional[str] = None, 
        api_key: Optional[str] = None, play_audio: bool = True) -> str:
    """Simple alias for text_to_speech with option to play the audio immediately"""
    client = create_client(api_key)
    return client.say(text, output_file, voice, play_audio) 