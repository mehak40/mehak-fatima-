"""
Voice Engine Module
Handles speech recognition and text-to-speech
"""

import speech_recognition as sr
from pyttsx3 import init as tts_init
import pyttsx3
import threading
from queue import Queue

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        
        # TTS Engine
        self.tts_engine = tts_init()
        self.tts_engine.setProperty('rate', 150)  # Speed
        self.tts_engine.setProperty('volume', 0.9)  # Volume
        
        # Queue for async speech
        self.speech_queue = Queue()
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()
    
    def listen_for_speech(self, timeout=10):
        """
        Listen for speech input
        Returns: Recognized text or empty string
        """
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            # Try Google Speech Recognition
            text = self.recognizer.recognize_google(audio, language='en-US')
            return text.strip()
            
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"API Error: {e}")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""
    
    def speak(self, text, language='en'):
        """
        Convert text to speech
        language: 'en' for English, 'ur' for Urdu
        """
        if not text:
            return False
        
        try:
            # Set language
            if language == 'ur':
                self.tts_engine.setProperty('voice', self._get_urdu_voice())
            else:
                self.tts_engine.setProperty('voice', self._get_english_voice())
            
            # Queue for async processing
            self.speech_queue.put(text)
            return True
            
        except Exception as e:
            print(f"TTS Error: {e}")
            return False
    
    def _speech_worker(self):
        """
        Worker thread for asynchronous speech
        """
        while True:
            try:
                text = self.speech_queue.get()
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"Speech worker error: {e}")
    
    def _get_english_voice(self):
        """
        Get English voice ID
        """
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            if 'english' in voice.name.lower() or voice.name.lower().startswith('david'):
                return voice.id
        return voices[0].id if voices else None
    
    def _get_urdu_voice(self):
        """
        Get Urdu voice ID (fallback to English if not available)
        """
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            if 'urdu' in voice.name.lower():
                return voice.id
        # Fallback to female voice
        for voice in voices:
            if 'zira' in voice.name.lower() or 'zira' in voice.name.lower():
                return voice.id
        return voices[0].id if voices else None
    
    def listen_for_urdu(self):
        """
        Listen specifically for Urdu speech
        """
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
            
            # Google Speech API with Urdu language code
            text = self.recognizer.recognize_google(audio, language='ur-PK')
            return text.strip()
            
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"API Error: {e}")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""
