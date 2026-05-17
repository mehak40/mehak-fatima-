"""
Command Processor Module
Parses and categorizes voice commands
"""

import re
from urllib.parse import quote

class CommandProcessor:
    def __init__(self):
        self.commands = {
            'open': ['open', 'کھول'],
            'search': ['search', 'تلاش'],
            'google': ['google', 'گوگل'],
            'youtube': ['youtube', 'یوٹیوب'],
            'whatsapp': ['whatsapp', 'واٹس ایپ'],
            'volume': ['volume', 'آواز'],
            'mute': ['mute', 'خاموش'],
            'unmute': ['unmute', 'آواز کھولو'],
            'remember': ['remember', 'یاد رکھو'],
            'what': ['what', 'کیا'],
        }
    
    def parse_command(self, text, language='en'):
        """
        Parse voice command text
        Returns: (command_type, parameters)
        """
        text_lower = text.lower().strip()
        
        # Detect command type
        if any(kw in text_lower for kw in self.commands['search']):
            return self._parse_search_command(text)
        
        elif any(kw in text_lower for kw in self.commands['google']):
            return ('open_browser', {'url': 'https://google.com', 'app_name': 'Google'})
        
        elif any(kw in text_lower for kw in self.commands['youtube']):
            query = self._extract_query(text, ['youtube', 'یوٹیوب'])
            if query:
                url = f"https://www.youtube.com/results?search_query={quote(query)}"
                return ('search', {'url': url, 'query': query, 'app_name': 'YouTube'})
            return ('open_browser', {'url': 'https://youtube.com', 'app_name': 'YouTube'})
        
        elif any(kw in text_lower for kw in self.commands['whatsapp']):
            contact = self._extract_contact(text)
            return ('open_app', {'app_name': 'whatsapp', 'contact': contact})
        
        elif any(kw in text_lower for kw in self.commands['volume']):
            action = self._parse_volume_command(text)
            return ('control_pc', {'action': action})
        
        elif any(kw in text_lower for kw in self.commands['remember']):
            memory = self._extract_memory_data(text)
            return ('remember', {'data': memory})
        
        else:
            return ('unknown', {})
    
    def _parse_search_command(self, text):
        """
        Parse search command
        Example: 'search for python programming'
        """
        query = self._extract_query(text, ['search', 'تلاش', 'search for'])
        if query:
            return ('search', {'query': query})
        return ('unknown', {})
    
    def _parse_volume_command(self, text):
        """
        Parse volume control command
        """
        text_lower = text.lower()
        if any(kw in text_lower for kw in ['up', 'increase', 'بڑھا', 'بڑھاؤ']):
            return 'volume_up'
        elif any(kw in text_lower for kw in ['down', 'decrease', 'کم', 'کم کرو']):
            return 'volume_down'
        elif any(kw in text_lower for kw in ['mute', 'خاموش', 'بند']):
            return 'mute'
        return 'volume_neutral'
    
    def _extract_query(self, text, keywords):
        """
        Extract search query from command
        Example: 'search for python' -> 'python'
        """
        for keyword in keywords:
            pattern = rf"{keyword}\s+(?:for\s+)?(.+)$"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_contact(self, text):
        """
        Extract contact name from WhatsApp command
        Example: 'send message to ali' -> 'ali'
        """
        patterns = [
            r"to\s+([a-zA-Z\s]+?)(?:\s+message|\s+msg|$)",
            r"([a-zA-Z\s]+?)\s+(?:message|msg)"
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_memory_data(self, text):
        """
        Extract data to remember
        Example: 'remember that my password is 123' -> {data: '123', type: 'password'}
        """
        pattern = r"remember\s+(?:that\s+)?(.+)$"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return {
                'data': match.group(1).strip(),
                'type': 'custom',
                'timestamp': str(__import__('datetime').datetime.now())
            }
        return {}
