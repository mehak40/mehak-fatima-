"""
Language Detector Module
Detects language (English/Urdu) and validates activation phrases
"""

import re

class LanguageDetector:
    def __init__(self):
        self.urdu_chars = set('آابپتثجحخدذرزژسشصضطظعغفقکگلمنںوہیے')
        
        # Activation phrases
        self.activation_phrases_en = ['nova', 'oh nova', 'hey nova']
        self.activation_phrases_ur = ['نوا', 'ہے نوا', 'اے نوا']
        
        # Common Urdu words for detection
        self.urdu_keywords = [
            'کھول', 'تلاش', 'گوگل', 'یوٹیوب', 'واٹس ایپ',
            'آواز', 'خاموش', 'یاد', 'کیا', 'کہو', 'بتاؤ'
        ]
    
    def detect(self, text):
        """
        Detect language from text
        Returns: 'en' for English, 'ur' for Urdu
        """
        if not text:
            return 'en'
        
        urdu_count = sum(1 for char in text if char in self.urdu_chars)
        total_chars = len(text)
        
        # If more than 30% Urdu characters, classify as Urdu
        if total_chars > 0 and (urdu_count / total_chars) > 0.3:
            return 'ur'
        
        # Check for Urdu keywords
        for keyword in self.urdu_keywords:
            if keyword in text.lower():
                return 'ur'
        
        return 'en'
    
    def is_activation_phrase(self, text):
        """
        Check if text contains activation phrase
        """
        text_lower = text.lower().strip()
        
        # Check English activation
        for phrase in self.activation_phrases_en:
            if phrase in text_lower or text_lower.startswith(phrase):
                return True
        
        # Check Urdu activation
        for phrase in self.activation_phrases_ur:
            if phrase in text:
                return True
        
        return False
    
    def normalize_text(self, text, language='en'):
        """
        Normalize text for processing
        """
        text = text.strip()
        
        if language == 'ur':
            # Remove diacritics from Urdu
            diacritics = '\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652'
            for diacritic in diacritics:
                text = text.replace(diacritic, '')
        
        return text
    
    def split_text(self, text):
        """
        Split text into words
        Handles both English and Urdu word boundaries
        """
        # Handle both spaces and Urdu word boundaries
        words = text.split()
        return words
