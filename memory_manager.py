"""
Memory Manager Module
Stores and retrieves interaction history and user data
"""

import json
import os
from datetime import datetime
from pathlib import Path

class MemoryManager:
    def __init__(self):
        self.memory_file = 'nova_memory.json'
        self.contacts_file = 'nova_contacts.json'
        self.history_file = 'nova_history.json'
        
        self.memory = {}
        self.contacts = {}
        self.history = []
        
        self.load_memory()
    
    def load_memory(self):
        """
        Load memory from files
        """
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
            
            if os.path.exists(self.contacts_file):
                with open(self.contacts_file, 'r', encoding='utf-8') as f:
                    self.contacts = json.load(f)
            
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"Error loading memory: {e}")
    
    def save_memory(self):
        """
        Save memory to files
        """
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
            
            with open(self.contacts_file, 'w', encoding='utf-8') as f:
                json.dump(self.contacts, f, ensure_ascii=False, indent=2)
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def add_memory(self, data):
        """
        Add item to memory
        """
        key = data.get('key', 'custom')
        self.memory[key] = {
            'data': data.get('data'),
            'type': data.get('type', 'custom'),
            'timestamp': datetime.now().isoformat()
        }
        self.save_memory()
    
    def get_memory(self, key):
        """
        Retrieve item from memory
        """
        return self.memory.get(key)
    
    def add_contact(self, name, phone=None, email=None):
        """
        Add contact to memory
        """
        self.contacts[name.lower()] = {
            'name': name,
            'phone': phone,
            'email': email,
            'added_at': datetime.now().isoformat()
        }
        self.save_memory()
    
    def get_contact(self, name):
        """
        Get contact by name
        """
        return self.contacts.get(name.lower())
    
    def list_contacts(self):
        """
        List all contacts
        """
        return list(self.contacts.values())
    
    def save_interaction(self, command, command_type, result):
        """
        Save command interaction to history
        """
        interaction = {
            'command': command,
            'type': command_type,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        self.history.append(interaction)
        
        # Keep only last 1000 interactions
        if len(self.history) > 1000:
            self.history = self.history[-1000:]
        
        self.save_memory()
    
    def get_history(self, limit=10):
        """
        Get last N interactions
        """
        return self.history[-limit:]
    
    def search_history(self, query):
        """
        Search history for interactions
        """
        results = []
        query_lower = query.lower()
        for interaction in self.history:
            if query_lower in interaction['command'].lower():
                results.append(interaction)
        return results
