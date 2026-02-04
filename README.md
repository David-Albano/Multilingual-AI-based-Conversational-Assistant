# Multilingual AI-based Conversational Assistant

This repository contains the source code for a real-time, multilingual conversational AI assistant. The application captures audio from a user's microphone, transcribes it to text, generates a response using an AI language model, and speaks the answer back to the user in the detected language.

## Features

*   **Multilingual Voice Interaction**: Automatically detects the language being spoken and responds in the same language. Supported languages include English, Spanish, Portuguese, French, German, Italian, and Dutch.
*   **Real-time Audio Processing**: Records audio from the microphone and uses automatic silence detection to determine when the user has finished speaking.
*   **High-Performance Transcription**: Utilizes `faster-whisper` for efficient, GPU-accelerated speech-to-text conversion.
*   **AI-Powered Responses**: Integrates with the OpenAI API (GPT-4o) to generate contextually relevant and natural-sounding answers.
*   **Streaming Text-to-Speech (TTS)**: Employs `edge-tts` to stream audio playback, providing a low-latency and responsive user experience.

## How It Works

The assistant operates in a continuous loop, following these steps for each interaction:

1.  **Record Audio**: The `audio_transcription.py` script listens for and records audio from the microphone using `sounddevice`. Recording stops automatically after a predefined period of silence or when the maximum recording time is reached.
2.  **Transcribe Speech**: The recorded audio is processed by the `faster-whisper` model, which transcribes the speech into text and identifies the language spoken.
3.  **Generate AI Response**: The transcribed text is sent to the OpenAI API. A carefully crafted prompt instructs the model to act as a helpful assistant and respond in the detected language using plain text.
4.  **Synthesize and Play Speech**: The AI's text response is fed into the `edge-tts` service via `answer_tts_play.py`. The resulting audio is streamed directly to the user's speakers, providing a continuous and natural playback experience.
5.  **Loop or Exit**: The application waits for the user to press Enter to start another conversation or type 'quit' to exit.

## Technologies Used

*   **Speech-to-Text**: [faster-whisper](https://github.com/guillaumekln/faster-whisper)
*   **Language Model**: [OpenAI API](https://platform.openai.com/docs/api-reference) (GPT-4o)
*   **Text-to-Speech**: [edge-tts](https://github.com/rany2/edge-tts)
*   **Audio I/O**: [sounddevice](https://python-sounddevice.readthedocs.io/), [NumPy](https://numpy.org/)
*   **Core Logic**: Python 3

## Setup and Installation

### Prerequisites

*   Python 3.8+
*   A CUDA-enabled NVIDIA GPU (recommended for `faster-whisper` performance).
*   **FFmpeg**: You must have FFmpeg installed and accessible in your system's PATH. This is required for audio format conversion by `edge-tts`. You can download it from [ffmpeg.org](https://ffmpeg.org/download.html).

### Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/David-Albano/Multilingual-AI-based-Conversational-Assistant.git
    cd Multilingual-AI-based-Conversational-Assistant
    ```

2.  **Install Dependencies**
    Install the required Python packages using the `requirements.txt` file. It is highly recommended to do this within a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The `requirements.txt` file specifies CUDA-enabled versions of PyTorch. If you are using a different setup (e.g., CPU-only or a different CUDA version), you may need to install a different version of `torch` and `torchvision`.*

3.  **Set Up Environment Variables**
    You need an OpenAI API key to use the language model.
    *   Create a file named `.env` in the root directory of the project.
    *   Add your OpenAI API key to this file as shown below:
    
    ```.env
    OPENAI_API_KEY="your_openai_api_key_here"
    ```

## Usage

To run the conversational assistant, execute the main script from the project's root directory:

```bash
python test_speech_and_model_response.py
```

The application will initialize the models and start the conversation loop. When you see "** - Recording...**", you can begin speaking. The assistant will process your request and respond vocally.

After each response, you can press **Enter** to continue the conversation or type `quit` and press **Enter** to end the session.

### Configuration

You can modify the behavior of the assistant by changing the flags and settings in the source files:

*   **`test_speech_and_model_response.py`**:
    *   `FASTER_WHISPER_FLAG`: Set to `False` to use the original `openai-whisper` library.
    *   `TRANSCRIPTION_FLAG`: Set to `False` to skip audio recording and use default text prompts from `settings.py` for testing TTS.
    *   `MODEL_USAGE_FLAG`: Set to `False` to skip calling the OpenAI API and use default answers from `settings.py`.
    *   `WhisperModel` device: Change `device="cuda"` to `device="cpu"` if you do not have a compatible GPU. You may also want to adjust `compute_type` for performance.

*   **`audio_transcription.py`**:
    *   `SILENCE_THRESHOLD`: Adjust the sensitivity for silence detection (lower is more sensitive).
    *   `SILENCE_DURATION`: Change how many seconds of silence are required to stop recording.

*   **`settings.py`**:
    *   `VOICE_LANG_MAP`: Modify the voice used for each language by selecting from the available voices for `edge-tts`.