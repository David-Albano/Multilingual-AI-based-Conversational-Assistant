import time, numpy as np, sounddevice as sd
from check_running import check_running

# ---------------- CONFIG ----------------
SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 1024

SILENCE_THRESHOLD = 0.02   # lower = more sensitive
SILENCE_DURATION = 3.0     # seconds of silence to stop
MAX_RECORD_SECONDS = 25 if input('\nPresenting on call? (y/n): ').lower() == 'y' else 10    # safety cap
# ----------------------------------------


def record_audio():
    silence_time = 0.0
    total_time = 0.0
    audio_buffer = []

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        blocksize=BLOCK_SIZE,
        dtype="float32"
    ) as stream:

        print("\n** - Recording...\n")

        while True:
            # <<<<****>>>>
            check_running()
            
            audio, _ = stream.read(BLOCK_SIZE)
            audio_buffer.append(audio)

            block_time = BLOCK_SIZE / SAMPLE_RATE
            total_time += block_time

            # ---- Silence detection ----
            rms = np.sqrt(np.dot(audio.flatten(), audio.flatten()) / audio.size)

            if rms < SILENCE_THRESHOLD:
                silence_time += block_time
            else:
                silence_time = 0.0

            if silence_time >= SILENCE_DURATION:
                print("** - Silence detected. Stopping recording.")
                break

            if total_time >= MAX_RECORD_SECONDS:
                print("** - Max recording time reached.")
                break
    
        return audio_buffer


def get_transcription(model, audio_buffer):

    if not audio_buffer:
        return None
    
    
    # <<<<****>>>>
    check_running()

    print("** - Concatenating...")
    audio_np = np.concatenate(audio_buffer, axis=0).flatten()

    # <<<<****>>>>
    check_running()

    print("** - Transcribing...")
    start_time = time.time()

    # <<<<****>>>>
    check_running()

    segments, info = model.transcribe(
        audio_np,
        beam_size=5,
    )

    # <<<<****>>>>
    check_running()

    # Build the final text from segments
    text_parts = []
    for segment in segments:
        text_parts.append(segment.text)

    full_text = " ".join(text_parts).strip()

    # <<<<****>>>>
    check_running()

    end_time = time.time()
    elapsed_time = end_time - start_time

    print('\n====================')
    print(f"** - Transcription completed in {elapsed_time:.2f} seconds.")
    print('====================')

    return full_text.strip(), info.language.lower()



# Version with Whisper (no faster-whisper)

def get_slower_transcription(model, audio_buffer):

    if not audio_buffer:
        return None

    print("** - Concatenating...")
    audio_np = np.concatenate(audio_buffer, axis=0).flatten()

    print("** - Transcribing...")
    start_time = time.time()

    result = model.transcribe(
        audio_np,
        fp16=False
    )

    end_time = time.time()
    elapsed_time = end_time - start_time

    print('\n====================')
    print(f"** - Transcription completed in {elapsed_time:.2f} seconds.")
    print('====================')

    return result.get("text", "").strip(), result["language"].lower().strip()
