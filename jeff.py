import sys
import os
from dotenv import load_dotenv
from openai import OpenAI
import time
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import threading
import speech_recognition as sr

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Convert text to speech using OpenAI TTS
def text_to_speech(input_text, voice="fable", format="mp3"):
    try:
        max_length = 4096

        # Split the text into smaller chunks if it's too long
        if len(input_text) > max_length:
            text_parts = textwrap.wrap(input_text, max_length, break_long_words=False)
        else:
            text_parts = [input_text]

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}") as temp_audio_file:
            audio_file_path = temp_audio_file.name

            for part in text_parts:
                response = client.audio.speech.create(
                    model="tts-1", 
                    voice=voice,
                    input=part,
                    response_format=format  # Defaults to 'mp3'
                )
                # Write the response content to the file
                temp_audio_file.write(response.read())

        return audio_file_path

    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")
        return None

# Text-to-Speech playback
def jarvis_speak(text):
    audio_file_path = text_to_speech(text, voice="fable")
    if audio_file_path:
        os.system(f"afplay {audio_file_path}")  # macOS audio player
        os.remove(audio_file_path)

# Real-time recognition and processing
def recognize_speech(callback):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Calibrating microphone for ambient noise...")

    def listen_and_process():
        print("Listening for the keyword 'Jeff'...")
        while True:
            try:
                with mic as source:
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio).lower()
                    print(f"Recognized: {command}")

                    if "jeff" in command:
                        jarvis_speak("Yes?")
                        print("Keyword detected. Listening for your command...")
                        
                        # Listen for the actual command
                        with mic as source:
                            audio = recognizer.listen(source)
                            command = recognizer.recognize_google(audio)
                            print(f"Command recognized: {command}")
                            callback(command)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

    # Start the listening in a separate thread
    listen_thread = threading.Thread(target=listen_and_process)
    listen_thread.daemon = True
    listen_thread.start()

# Generate AI Response using the OpenAI API with retry mechanism
def generate_response(prompt, retries=3):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error generating response: {e}")
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return "Sorry, something went wrong after multiple attempts."

# GUI Application with Avatar and typed input
class JarvisApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jeff")
        self.setGeometry(100, 100, 500, 600)

        layout = QVBoxLayout()

        # Avatar Image (make sure you have the correct path for the image)
        self.label = QLabel(self)
        pixmap = QPixmap('avatar.png')  # Make sure 'avatar.png' is in the correct path
        if pixmap.isNull():
            print("Error loading image, check the path.")
        self.label.setPixmap(pixmap.scaled(300, 400, Qt.KeepAspectRatio))
        layout.addWidget(self.label)

        # Command display
        self.command_label = QLabel("Say something...", self)
        layout.addWidget(self.command_label)

        # Text input for typed commands
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Type a command here...")
        layout.addWidget(self.text_input)

        # Submit button for typed commands
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.on_submit_command)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

        # Start speech recognition in a separate thread
        self.listen_thread = threading.Thread(target=self.run_jarvis)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    # Process voice or typed commands
    def process_command(self, command):
        self.command_label.setText(f"You said: {command}")

        if "exit" in command:
            jarvis_speak("Alright, buddy. Catch you next time.")
            sys.exit()
        else:
            ai_response = generate_response(f"Respond like a tipsy friend: {command}")
            jarvis_speak(ai_response)
            self.command_label.setText(f"JARVIS: {ai_response}")

    # Callback function to pass recognized speech to the main thread
    def run_jarvis(self):
        recognize_speech(self.process_command)

    # Called when user types a command and presses submit
    def on_submit_command(self):
        user_command = self.text_input.text()
        if user_command:
            self.process_command(user_command)
            self.text_input.clear()

# Run the GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    jarvis = JarvisApp()
    jarvis.show()
    sys.exit(app.exec_())
