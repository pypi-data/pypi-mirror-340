from setuptools import setup, find_packages

setup(
    name="gemini_tts",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "websockets>=12.0",
        "wave>=0.0.2",
    ],
    author="Gemini TTS Developer",
    author_email="example@example.com",
    description="A simple TTS library using Google Gemini API",
    keywords="tts, text-to-speech, gemini, google",
    python_requires=">=3.7",
) 