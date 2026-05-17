"""
Self-Learning Module
Improves command recognition and execution over time
"""

import json
import os
from collections import defaultdict
from datetime import datetime

class SelfLearning:
    def __init__(self):
        self.learning_file = 'nova_learning.json'
        self.command_patterns = defaultdict(list)
        self.command_success_rate = defaultdict(lambda: {'success': 0, 'total': 0})
        self.user_preferences = {}
        
        self.load_learning_data()
    
    def load_learning_data(self):
        """
        Load previously learned patterns
        """
        try:
            if os.path.exists(self.learning_file):
                with open(self.learning_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.command_patterns = defaultdict(list, data.get('patterns', {}))
                    self.command_success_rate = defaultdict(
                        lambda: {'success': 0, 'total': 0},
                        data.get('success_rate', {})
                    )
                    self.user_preferences = data.get('preferences', {})
        except Exception as e:
            print(f"Error loading learning data: {e}")
    
    def save_learning_data(self):
        """
        Save learned patterns
        """
        try:
            data = {
                'patterns': dict(self.command_patterns),
                'success_rate': {k: v for k, v in self.command_success_rate.items()},
                'preferences': self.user_preferences,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.learning_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving learning data: {e}")
    
    def learn_interaction(self, command_text, command_type, parameters, success, language):
        """
        Learn from user interaction
        """
        # Store command pattern
        pattern = {
            'text': command_text,
            'type': command_type,
            'parameters': parameters,
            'language': language,
            'timestamp': datetime.now().isoformat()
        }
        
        self.command_patterns[command_type].append(pattern)
        
        # Update success rate
        self.command_success_rate[command_type]['total'] += 1
        if success:
            self.command_success_rate[command_type]['success'] += 1
        
        # Keep only recent patterns
        if len(self.command_patterns[command_type]) > 100:
            self.command_patterns[command_type] = self.command_patterns[command_type][-100:]
        
        self.save_learning_data()
    
    def get_success_rate(self, command_type):
        """
        Get success rate for command type
        Returns: float between 0 and 1
        """
        stats = self.command_success_rate.get(command_type, {'success': 0, 'total': 0})
        if stats['total'] == 0:
            return 0
        return stats['success'] / stats['total']
    
    def get_similar_patterns(self, command_text, command_type, limit=5):
        """
        Find similar patterns for better matching
        """
        patterns = self.command_patterns.get(command_type, [])
        
        # Simple similarity based on word overlap
        command_words = set(command_text.lower().split())
        
        similarities = []
        for pattern in patterns:
            pattern_words = set(pattern['text'].lower().split())
            overlap = len(command_words & pattern_words)
            if overlap > 0:
                similarities.append((pattern, overlap))
        
        # Sort by overlap and return top matches
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [p[0] for p in similarities[:limit]]
    
    def get_statistics(self):
        """
        Get learning statistics
        """
        stats = {
            'total_commands': sum(len(patterns) for patterns in self.command_patterns.values()),
            'command_types': len(self.command_patterns),
            'success_rates': {k: self.get_success_rate(k) for k in self.command_success_rate.keys()},
            'most_used_command': self._get_most_used_command(),
            'learning_progress': self._calculate_learning_progress()
        }
        return stats
    
    def _get_most_used_command(self):
        """
        Get most frequently used command type
        """
        if not self.command_patterns:
            return None
        return max(self.command_patterns.items(), key=lambda x: len(x[1]))[0]
    
    def _calculate_learning_progress(self):
        """
        Calculate overall learning progress (0-100)
        """
        if not self.command_success_rate:
            return 0
        
        success_rates = [self.get_success_rate(cmd) for cmd in self.command_success_rate.keys()]
        if success_rates:
            return sum(success_rates) / len(success_rates) * 100
        return 0
