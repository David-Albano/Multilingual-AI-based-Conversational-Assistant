import time, whisper, streamlit as st
from audio_transcription import record_audio, get_transcription, get_slower_transcription
from check_running import check_running
from load_env import get_openai_client
from answer_tts_play import speak
from faster_whisper import WhisperModel
from settings import DEFAULT_TRANSCRIPTION, DEFAULT_ANSWERS, DEFAULT_GOODBYES

client = get_openai_client()

FASTER_WHISPER_FLAG = True
TRANSCRIPTION_FLAG = True
MODEL_USAGE_FLAG = True

import torch
print(torch.cuda.is_available())
print(torch.version.cuda)

print("\nLoading Whisper model...") if TRANSCRIPTION_FLAG else None

if FASTER_WHISPER_FLAG:
    transcription_model = WhisperModel(
        "small",
        device="cuda", # -> or "cpu"
        compute_type="int8" # -> or "int8_float16"/"float16" depending on device (cpu/gpu usage)
    ) if TRANSCRIPTION_FLAG else None

else:
    transcription_model = whisper.load_model("small") if TRANSCRIPTION_FLAG else None


# ======================================================

def get_answer(transcription, language_expected):
    print("\n\n** - Generating response...")

    prompt = f"""
        You are a helpful, friendly and professional assistant.

        RULES:
        - Answer strictly in the following language: '{language_expected}'.
        - Do not use any formatting: no asterisks, no bold, no italics, no Markdown.
        - Use plain text only. Before sending your answer, make sure it contains zero asterisks.\n\n

        Here is the text you need to respond to:\n
        {transcription}\n\n

        "Please provide your answer now."
    """

    try:
        start_time = time.time()

        # <<<<****>>>>
        check_running()

        response = client.chat.completions.create(
            # model='gpt-4.1-nano',
            model='gpt-4o',
            messages=[
                {
                    'role': 'system',
                    'content': (
                        "You are a helpful, friendly and professional assistant.\n"
                        "IMPORTANT FORMATTING RULE:\n"
                        "- Never use asterisks of any kind (* or **).\n"
                        "- Do not use Markdown formatting.\n"
                        "- Do not use bold, italics, or emphasis markers.\n"
                        "- Use plain text only.\n"
                        "Before sending your final answer, verify that it contains zero asterisks."
                    )
                },
                {'role': 'user', 'content': prompt}
            ]
        )

        # <<<<****>>>>
        check_running()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"** - Response generated in {elapsed_time:.2f} seconds.")

        print("\n** - 🤖 Model Response:\n")
        print('\tª', response.choices[0].message.content.replace('*', '').strip(), '\n\n')

        return response.choices[0].message.content.replace('*', '').strip()

    except Exception as e:
        print("❌ Error generating response:", e)
        return "My apologies, I ran into an error generating a response."


def get_transcription_and_lang(audio_buffer):
    if TRANSCRIPTION_FLAG:

        if FASTER_WHISPER_FLAG:
            # <<<<****>>>>
            check_running()
            transcription, language_detected = get_transcription(transcription_model, audio_buffer)
        
        else:
            # <<<<****>>>>
            check_running()
            transcription, language_detected = get_slower_transcription(transcription_model, audio_buffer)


    else:
        # <<<<****>>>>
        check_running()
        language_detected = input(f"Enter language code for default transcription (en, es, pt, fr, de, it, nl): ")
        transcription = DEFAULT_TRANSCRIPTION.get(language_detected, DEFAULT_TRANSCRIPTION['en'])
    
    print("\n** - 👤 Transcription:\n")
    print('\tº', transcription)

    print("\n** - Detected language:", language_detected)

    return transcription, language_detected

def recording():
    # <<<<****>>>>
    check_running()

    if TRANSCRIPTION_FLAG:
        return record_audio()

    return None

# def start_conversation():
#     print("\n\n** - Starting conversation. Press Enter or Ctrl+C to stop.")

#     while True:
#         # <<<<****>>>>
#         check_running()

#         print('\n==================== ********* ====================\n')

#         if TRANSCRIPTION_FLAG:
#             audio_buffer = record_audio()

#             start_time = time.time() # time from here

#             if FASTER_WHISPER_FLAG:
#                 # <<<<****>>>>
#                 check_running()
#                 transcription, language_detected = get_transcription(transcription_model, audio_buffer)
            
#             else:
#                 # <<<<****>>>>
#                 check_running()
#                 transcription, language_detected = get_slower_transcription(transcription_model, audio_buffer)


#         else:
#             start_time = time.time() # time from here

            
#             # <<<<****>>>>
#             check_running()
#             language_detected = input(f"Enter language code for default transcription (en, es, pt, fr, de, it, nl): ")
#             transcription = DEFAULT_TRANSCRIPTION.get(language_detected, DEFAULT_TRANSCRIPTION['en'])
            
        
#         if not transcription:
#             # <<<<****>>>>
#             check_running()
#             speak("I'm not sure I heard anything. Could you please repeat?", 'en')
#             continue


#         print("\n** - 👤 Transcription:\n")
#         print('\tº', transcription)

#         print("\n** - Detected language:", language_detected)

        
#         # <<<<****>>>>
#         check_running()
#         model_answer = get_answer(transcription, language_detected) if MODEL_USAGE_FLAG else DEFAULT_ANSWERS.get(language_detected, DEFAULT_ANSWERS['en'])

#         end_time = time.time()

#         print("\n** - 🤖 Model Response:\n")
#         print('\tª', model_answer, '\n\n')
#         print(f"\n** =====*===== Total processing time from transcription to model response : {end_time - start_time:.2f} seconds =====*=====")

#         # 🔊 Speak it (blocking by default)
        
#         # <<<<****>>>>
#         check_running()
#         speak(model_answer, language_detected)

#         # user_input = input("\nPress Enter to continue... type 'quit' to end conversation: ")

#         # if user_input.lower() in ['quit', 'q', 'exit', 'stop'] or user_input != '':
#         #     speak(DEFAULT_GOODBYES.get(language_detected, DEFAULT_GOODBYES['en']), language_detected)
#         #     break


# if __name__ == "__main__":
#     print("Starting recording and transcription...")
#     start_conversation()
