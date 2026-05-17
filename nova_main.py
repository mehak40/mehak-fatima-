"""
NOVA - Intelligent Voice Assistant
Main Entry Point
Supports: Urdu + English, Voice Commands, Self-Learning
"""

import os
import sys
import json
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import webbrowser
import subprocess

# Import custom modules
from voice_engine import VoiceEngine
from command_processor import CommandProcessor
from language_detector import LanguageDetector
from memory_manager import MemoryManager
from self_learning import SelfLearning

class NovaAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("NOVA - Voice Assistant")
        self.root.geometry("900x600")
        self.root.configure(bg="#1a1a2e")
        
        # Initialize components
        self.voice_engine = VoiceEngine()
        self.command_processor = CommandProcessor()
        self.language_detector = LanguageDetector()
        self.memory_manager = MemoryManager()
        self.self_learning = SelfLearning()
        
        # State
        self.is_listening = False
        self.is_activated = False
        self.current_language = "en"  # en or ur
        
        # Setup UI
        self.setup_ui()
        
        # Load previous memory
        self.memory_manager.load_memory()
        self.self_learning.load_learning_data()
        
    def setup_ui(self):
        """Create GUI Interface"""
        
        # Header
        header_frame = tk.Frame(self.root, bg="#16213e", height=60)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="🎤 NOVA - Voice Assistant",
            font=("Arial", 18, "bold"),
            bg="#16213e",
            fg="#00d4ff"
        )
        title_label.pack(pady=10)
        
        # Status Frame
        status_frame = tk.Frame(self.root, bg="#0f3460")
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Status: Waiting for activation (Say 'Nova')",
            font=("Arial", 11),
            bg="#0f3460",
            fg="#00d4ff"
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.activation_button = tk.Button(
            status_frame,
            text="🎙️ Start Listening",
            command=self.toggle_listening,
            bg="#e94560",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5
        )
        self.activation_button.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Output Display
        output_label = tk.Label(
            self.root,
            text="Voice Commands & Responses:",
            font=("Arial", 11, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        output_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        self.output_text = scrolledtext.ScrolledText(
            self.root,
            height=15,
            width=100,
            bg="#0f3460",
            fg="#00ff00",
            font=("Courier", 9),
            insertbackground="#00d4ff"
        )
        self.output_text.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)
        
        # Control Frame
        control_frame = tk.Frame(self.root, bg="#1a1a2e")
        control_frame.pack(fill=tk.X, padx=15, pady=10)
        
        clear_button = tk.Button(
            control_frame,
            text="Clear",
            command=lambda: self.output_text.delete(1.0, tk.END),
            bg="#4a4a6a",
            fg="white",
            font=("Arial", 9)
        )
        clear_button.pack(side=tk.LEFT, padx=5)
        
        save_button = tk.Button(
            control_frame,
            text="Save Log",
            command=self.save_log,
            bg="#4a4a6a",
            fg="white",
            font=("Arial", 9)
        )
        save_button.pack(side=tk.LEFT, padx=5)
        
        exit_button = tk.Button(
            control_frame,
            text="Exit",
            command=self.exit_app,
            bg="#e94560",
            fg="white",
            font=("Arial", 9)
        )
        exit_button.pack(side=tk.RIGHT, padx=5)
        
        self.log(f"[{self.get_time()}] NOVA Initialized - Ready to listen for 'Nova' activation")
    
    def toggle_listening(self):
        """Toggle voice listening"""
        if not self.is_listening:
            self.is_listening = True
            self.activation_button.config(text="🎙️ Stop Listening", bg="#4a7c7e")
            self.status_label.config(text="Status: Listening... Say 'Nova' to activate")
            self.log(f"[{self.get_time()}] 🎤 Started listening for activation phrase 'Nova'")
            
            # Start listening in separate thread
            listening_thread = threading.Thread(target=self.listen_loop, daemon=True)
            listening_thread.start()
        else:
            self.is_listening = False
            self.is_activated = False
            self.activation_button.config(text="🎙️ Start Listening", bg="#e94560")
            self.status_label.config(text="Status: Stopped")
            self.log(f"[{self.get_time()}] ⏹️ Stopped listening")
    
    def listen_loop(self):
        """Main listening loop"""
        while self.is_listening:
            try:
                # Listen for audio
                audio_text = self.voice_engine.listen_for_speech()
                
                if not audio_text:
                    continue
                
                # Detect language
                self.current_language = self.language_detector.detect(audio_text)
                
                self.log(f"[{self.get_time()}] 🎙️ You said: {audio_text} [{self.current_language.upper()}]")
                
                # Check for activation
                if self.language_detector.is_activation_phrase(audio_text):
                    self.is_activated = True
                    self.status_label.config(text="Status: ACTIVATED ✓")
                    response = self.voice_engine.speak(
                        "نوا یہاں ہے" if self.current_language == "ur" else "Nova here",
                        self.current_language
                    )
                    self.log(f"[{self.get_time()}] 🤖 Nova: Activated and ready for commands")
                    continue
                
                # Process command if activated
                if self.is_activated:
                    self.process_voice_command(audio_text)
                    
            except Exception as e:
                self.log(f"[{self.get_time()}] ❌ Error: {str(e)}")
    
    def process_voice_command(self, command_text):
        """Process voice command"""
        try:
            # Parse command
            command_type, parameters = self.command_processor.parse_command(
                command_text,
                self.current_language
            )
            
            self.log(f"[{self.get_time()}] 📝 Command: {command_type} | Params: {parameters}")
            
            # Execute command
            result = self.execute_command(command_type, parameters)
            
            # Speak response
            response_text = result.get("response", "")
            if response_text:
                self.voice_engine.speak(response_text, self.current_language)
                self.log(f"[{self.get_time()}] 🤖 Nova: {response_text}")
            
            # Learn from interaction
            self.self_learning.learn_interaction(
                command_text,
                command_type,
                parameters,
                result.get("success", False),
                self.current_language
            )
            
            # Save to memory
            self.memory_manager.save_interaction(
                command_text,
                command_type,
                result
            )
            
        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            self.log(f"[{self.get_time()}] ❌ {error_msg}")
            self.voice_engine.speak(error_msg, self.current_language)
    
    def execute_command(self, command_type, parameters):
        """Execute recognized command"""
        result = {
            "success": False,
            "response": "",
            "action": command_type
        }
        
        try:
            if command_type == "open_browser":
                url = parameters.get("url", "https://google.com")
                webbrowser.open(url)
                result["success"] = True
                result["response"] = f"Opening {parameters.get('app_name', 'website')}" if self.current_language == "en" else f"{parameters.get('app_name', 'ویب سائٹ')} کھول رہا ہوں"
                
            elif command_type == "search":
                query = parameters.get("query", "")
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(search_url)
                result["success"] = True
                result["response"] = f"Searching for {query}" if self.current_language == "en" else f"{query} تلاش کر رہا ہوں"
                
            elif command_type == "open_app":
                app_name = parameters.get("app_name", "").lower()
                if app_name == "whatsapp":
                    subprocess.Popen(["start", "whatsapp"], shell=True)
                    result["response"] = "Opening WhatsApp" if self.current_language == "en" else "واٹس ایپ کھول رہا ہوں"
                result["success"] = True
                
            elif command_type == "control_pc":
                action = parameters.get("action", "")
                if action == "volume_up":
                    os.system("nircmd changesysvolume 3000")
                    result["response"] = "Increasing volume" if self.current_language == "en" else "آواز بڑھا رہا ہوں"
                result["success"] = True
                
            elif command_type == "remember":
                data = parameters.get("data", {})
                self.memory_manager.add_memory(data)
                result["response"] = "I'll remember that" if self.current_language == "en" else "میں یہ یاد رکھوں گا"
                result["success"] = True
                
            else:
                result["response"] = "Command not recognized" if self.current_language == "en" else "کمانڈ معلوم نہیں"
                
        except Exception as e:
            result["response"] = f"Error: {str(e)}"
        
        return result
    
    def log(self, message):
        """Log message to UI"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()
    
    def save_log(self):
        """Save conversation log"""
        try:
            log_filename = f"nova_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(log_filename, "w", encoding="utf-8") as f:
                f.write(self.output_text.get(1.0, tk.END))
            self.log(f"[{self.get_time()}] 💾 Log saved: {log_filename}")
            messagebox.showinfo("Success", f"Log saved as {log_filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save log: {str(e)}")
    
    def exit_app(self):
        """Exit application"""
        self.is_listening = False
        self.memory_manager.save_memory()
        self.self_learning.save_learning_data()
        self.root.quit()
    
    @staticmethod
    def get_time():
        """Get current time"""
        return datetime.now().strftime("%H:%M:%S")

def main():
    root = tk.Tk()
    app = NovaAssistant(root)
    root.mainloop()

if __name__ == "__main__":
    main()
