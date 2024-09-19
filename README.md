# JEFF

JEFF is an AI assistant that integrates OpenAI's text and speech capabilities. This project currently supports generating text responses using OpenAI's API, text-to-speech conversion using OpenAI's TTS, and a GUI with PyQt5.

## Getting Started

To set up and run this project on your local machine, follow these steps:

### Prerequisites

- Python 3.x installed
- Homebrew (for macOS)

### Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/ZanderDent/JEFF.git
    cd JEFF
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate     # On Windows
    ```

3. Install `portaudio` (required for speech recognition) using Homebrew (macOS):
    ```bash
    brew install portaudio
    ```

4. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

Run the application using the following command:
```bash
python jeff.py
```

## Current Status

- **Text Generation**: Working. The application uses OpenAI's `gpt-3.5-turbo` model for generating responses to user input.
- **Text-to-Speech**: Working. The application uses OpenAI's TTS model to convert text responses into speech.
- **Speech-to-Text Input**: Not working. The speech recognition component is not currently functioning correctly. We are looking for help with this issue.

## Help Wanted

We are looking for contributions in the following areas:

1. **Speech Recognition to AI Input**: We are currently facing issues with integrating speech recognition into the AI input. If you have experience with `speech_recognition` or any other voice-to-text APIs, your input would be highly valuable.

2. **3D Animated Model Integration**: We are interested in replacing the current 2D avatar with a 3D animated model that can sync with the AI responses. If you have experience with 3D modeling and animation integration into Python applications, please reach out!

