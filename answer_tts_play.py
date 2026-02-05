import asyncio
import edge_tts
import sounddevice as sd
import numpy as np
import subprocess
from settings import VOICE_LANG_MAP
from check_running import check_running


SAMPLE_RATE = 24000  # edge-tts default
CHANNELS = 1
DTYPE = "float32"


async def speak_streaming(text: str, language: str = 'en'):

    voice_language = VOICE_LANG_MAP.get(language, VOICE_LANG_MAP['en'])  # default to English if not found

    # <<<<****>>>>
    check_running()

    communicate = edge_tts.Communicate(
        text,
        voice_language
    )

    # <<<<****>>>>
    check_running()

    # ffmpeg process: MP3 → raw float32 PCM
    ffmpeg = subprocess.Popen(
        [
            "ffmpeg",
            "-loglevel", "quiet",
            "-i", "pipe:0",
            "-f", "f32le",
            "-ar", str(SAMPLE_RATE),
            "-ac", str(CHANNELS),
            "pipe:1",
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    # <<<<****>>>>
    check_running()

    def audio_callback(outdata, frames, time, status):
        data = ffmpeg.stdout.read(frames * 4)  # 4 bytes per float32
        if not data:
            raise sd.CallbackStop
        outdata[:] = np.frombuffer(data, dtype=np.float32).reshape(-1, 1)

    print("\n==== speaking (streaming)")

    with sd.OutputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=DTYPE,
        callback=audio_callback,
    ):
        async for chunk in communicate.stream():
            # <<<<****>>>>
            check_running()

            if chunk["type"] == "audio":
                ffmpeg.stdin.write(chunk["data"])

        ffmpeg.stdin.close()
        ffmpeg.wait()

    print("==== speak done")


# sync wrapper (same pattern you already use)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def speak(text: str, language: str = 'en'):
    # <<<<****>>>>
    check_running()
    loop.run_until_complete(speak_streaming(text, language))

