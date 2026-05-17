# NOVA Installation Guide

## Step-by-Step Installation

### Step 1: Install Python
1. Download Python 3.8+ from [python.org](https://python.org)
2. Install and make sure to check "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   ```

### Step 2: Install Visual Studio Code (Optional)
1. Download from [code.visualstudio.com](https://code.visualstudio.com)
2. Install Python extension
3. Install Pylance extension

### Step 3: Clone Repository
```bash
# Option A: Using Git
git clone https://github.com/mehak40/nova-assistant.git
cd nova-assistant

# Option B: Download ZIP
# Download from GitHub and extract
```

### Step 4: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

If you encounter issues:
```bash
# Update pip first
python -m pip install --upgrade pip

# Install packages individually
pip install SpeechRecognition==3.10.0
pip install pyttsx3==2.90
pip install numpy==1.24.0
```

### Step 6: Test Installation
```bash
python nova_main.py
```

You should see the NOVA window open.

## Troubleshooting Installation

### Error: "ModuleNotFoundError: No module named 'speech_recognition'"
```bash
pip install SpeechRecognition --upgrade
```

### Error: "No module named 'pyttsx3'"
```bash
pip install pyttsx3 --upgrade
```

### Error: "Microphone not found"
1. Check if microphone is connected
2. Test in system settings
3. Try different USB microphone if available

### Error: "ModuleNotFoundError: No module named 'tkinter'"

**Windows:**
```bash
# Tkinter comes with Python, may need to reinstall
python -m pip install tk
```

**macOS:**
```bash
# Using Homebrew
brew install python-tk
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

### Error: "Speech recognition failed"
1. Check internet connection
2. Speak clearly and slowly
3. Adjust microphone volume

## Verify Installation

```bash
# Test each component

# Test 1: Speech Recognition
python -c "import speech_recognition as sr; print('SR: OK')"

# Test 2: Text to Speech
python -c "import pyttsx3; print('TTS: OK')"

# Test 3: Tkinter
python -c "import tkinter; print('Tkinter: OK')"

# Test 4: Full NOVA
python nova_main.py
```

## Using in Visual Studio Code

1. Open folder in VS Code
2. Select Python interpreter:
   - Ctrl+Shift+P
   - Type: "Python: Select Interpreter"
   - Choose the one from venv
3. Run with F5 or Ctrl+F5

## First Run Setup

1. Launch NOVA
2. Click "Start Listening"
3. Speak clearly: "Nova"
4. Wait for confirmation: "Nova here"
5. Try a command: "Open Google"

## Permissions (Windows)

If you get microphone permission errors:
1. Settings > Privacy & Security > Microphone
2. Allow Python to access microphone
3. Restart NOVA

## Updating NOVA

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Need Help?

- Check GitHub Issues
- Review README.md
- Test microphone separately
- Check internet connection
