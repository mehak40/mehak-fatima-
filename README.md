# NOVA - Intelligent Voice Assistant

![NOVA](https://img.shields.io/badge/NOVA-Voice%20Assistant-brightgreen)

NOVA is an advanced voice-controlled AI assistant that supports **English and Urdu** languages. It can execute commands, remember information, and learn from interactions.

## Features

✨ **Core Features:**
- 🎤 **Voice Activation** - Activate with "Nova" voice command
- 🌍 **Bilingual Support** - English & Urdu
- 🧠 **Self-Learning** - Improves over time with interactions
- 💾 **Memory Management** - Remembers contacts, preferences, and history
- 🎯 **Command Execution** - Opens apps, searches, controls PC
- 🪟 **Desktop GUI** - Modern, easy-to-use interface
- 🔊 **Voice Response** - Speaks back to you

## Supported Commands

### 1. **Open Applications**
```
"Open Google"
"Open YouTube"
"Open WhatsApp"
```

### 2. **Search**
```
"Search for Python programming"
"تلاش کریں مختلف موضوع"
```

### 3. **Media Control**
```
"Volume up"
"Mute"
"Play music"
```

### 4. **Memory**
```
"Remember my password is 123"
"یاد رکھو میرا نمبر 03123456789"
```

### 5. **PC Control**
```
"Take a screenshot"
"Open file manager"
"Shutdown computer"
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Microphone connected
- Internet connection (for speech recognition)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/mehak40/nova-assistant.git
cd nova-assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run NOVA**
```bash
python nova_main.py
```

## Usage

1. **Launch the application**
   ```bash
   python nova_main.py
   ```

2. **Click "Start Listening"** button or let it auto-start

3. **Say "Nova"** to activate
   - You'll hear: "Nova here" (English) or "نوا یہاں ہے" (Urdu)

4. **Give commands** in English or Urdu
   - NOVA will execute and respond

5. **Commands are logged** with timestamps

## Project Structure

```
nova-assistant/
├── nova_main.py              # Main application
├── voice_engine.py           # Speech recognition & TTS
├── command_processor.py      # Command parsing
├── language_detector.py      # Language detection
├── memory_manager.py         # Storage & retrieval
├── self_learning.py          # Learning algorithms
├── requirements.txt          # Dependencies
├── nova_memory.json          # Stored memories
├── nova_contacts.json        # Contact list
├── nova_history.json         # Command history
├── nova_learning.json        # Learned patterns
└── README.md                 # This file
```

## Module Documentation

### voice_engine.py
Handles all voice input/output:
- `listen_for_speech()` - Captures and recognizes speech
- `speak()` - Converts text to speech
- Supports English and Urdu

### command_processor.py
Parses voice commands:
- Pattern matching for command types
- Parameter extraction
- Handles multiple languages

### language_detector.py
Automatically detects language:
- English/Urdu detection
- Text normalization
- Activation phrase recognition

### memory_manager.py
Manages all data storage:
- Contact management
- Command history
- User preferences
- Persistent storage (JSON files)

### self_learning.py
Improves over time:
- Learns command patterns
- Tracks success rates
- Suggests similar commands
- Self-optimizes

## Configuration

### Adjust Voice Speed
```python
# In voice_engine.py
self.tts_engine.setProperty('rate', 150)  # 0-200
```

### Adjust Microphone Sensitivity
```python
# In voice_engine.py
self.recognizer.energy_threshold = 4000  # Lower = more sensitive
```

### Add Custom Commands
Edit `command_processor.py` and add to `self.commands` dictionary

## Troubleshooting

### Microphone not detected
```bash
# Test microphone
python -m speech_recognition
```

### Speech not recognized
- Speak clearly and slowly
- Ensure internet connection (for Google Speech API)
- Adjust microphone sensitivity

### TTS not working
- Install pyttsx3 correctly:
  ```bash
  pip install --upgrade pyttsx3
  ```

## Self-Learning Features

NOVA learns from every interaction:

1. **Pattern Learning** - Recognizes similar commands
2. **Success Tracking** - Knows which commands work best
3. **Preference Learning** - Adapts to your habits
4. **Language Switching** - Improves bilingual understanding

## Data Privacy

- All data stored locally in JSON files
- No cloud synchronization by default
- All commands logged locally
- You have full control over data

## Future Enhancements

- 🔗 WhatsApp message sending
- 📅 Calendar integration
- 🎵 Music player control
- 🌐 Real-time translation
- ☁️ Cloud sync option
- 🤖 Advanced NLP
- 🎮 Custom voice profiles

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [Create Issue]
- Email: mehak40@github.com

## Acknowledgments

- Google Speech Recognition API
- pyttsx3 for text-to-speech
- Python speech_recognition library

---

**Made with ❤️ by Mehak**

*Last Updated: 2026*
