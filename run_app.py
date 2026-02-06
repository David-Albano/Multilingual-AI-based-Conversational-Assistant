import time, streamlit as st

from answer_tts_play import speak
from check_running import StopConversation
from settings import DEFAULT_ANSWERS

app_name = 'Ambrósio GPT'

if "running" not in st.session_state:
    st.session_state.running = False

def import_starting():
    from test_speech_and_model_response import MODEL_USAGE_FLAG, get_answer, get_transcription_and_lang, recording
    return MODEL_USAGE_FLAG, get_answer, get_transcription_and_lang, recording

color_map = {
    "Listening": "#e24b4b",
    "Processing": "#f0a500",
    "Generating answer": "#2f59e2",
    "Speaking": "#2fbf71"
}

def update_status(message):
    status_box.markdown(
        f"""
        <style>
        .status-wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 140px;
            gap: 14px;
        }}

        .pulse-core {{
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: {color_map[message]};
            box-shadow: 0 0 0 rgba(250, 250, 250, 0.6);
            animation: pulse 1.6s infinite;
        }}

        @keyframes pulse {{
            0% {{
                box-shadow: 0 0 0 0 rgba(250, 250, 250, 0.6);
                transform: scale(1);
            }}
            70% {{
                box-shadow: 0 0 0 26px rgba(250, 250, 250, 0);
                transform: scale(1.1);
            }}
            100% {{
                box-shadow: 0 0 0 0 rgba(250, 250, 250, 0);
                transform: scale(1);
            }}
        }}

        .status-text {{
            font-size: 20px;
            font-weight: 700;
            color: {color_map[message]};
            letter-spacing: 0.4px;
        }}
        </style>

        <div class="status-wrapper">
            <div class="pulse-core"></div>
            <div class="status-text">{message}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Page config
st.set_page_config(
    page_title=f"{app_name}",
    page_icon='logo_3.png',
    layout="centered"
)

# Main title
st.markdown(
    f"""<div
            style='
                background: linear-gradient(64deg, #e31937 2%, #a82465 44%, #3e1bb1 84%);
                display:flex;
                gap: 8px;
                justify-content: center;
                align-items: center;
                font-family: Arial;
                font-size: 45px;
                border: none;
                border-radius: 15px;
                padding-top: 1rem;
                width: 430px;
                height: 95px;
                margin: 0 auto;
                box-shadow: rgba(0, 0, 0, 0.1) 0px 30px 60px -12px inset, rgba(0, 0, 0, 0.1) 0px 18px 36px -18px inset;
            '
        >
            <p style='color:#f1f1f1;font-weight: bold;' >Ambrósio</p>
            <p
                style='
                    font-size: 52px;
                    font-weight: bold;
                    color:#4b4a4a;
                    filter: drop-shadow(0 0 10px rgba(0, 0, 0, 0.15));
                    -webkit-text-stroke: 0.7px rgba(250, 250, 250, 0.7);
                '
            >
                GPT
            </p>
        </div>
    """,
    unsafe_allow_html=True
)

st.write("")  # spacer

# Centered logo section
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("logo.png")

st.markdown(
    """
    <style>
    img {
        margin-top: 1.5rem;
        filter: drop-shadow(0 0 10px rgba(62, 27, 177, 0.3));
        transform: scale(1.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ===== Animated loader =====

loader = st.empty()

loader.markdown(
    """
    <style>
    .loader-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80px;
        font-size: 22px;
        font-weight: 600;
        color: #2f59e2;
    }

    .dots::after {
        content: '';
        animation: dots 1.5s infinite;
    }

    @keyframes dots {
        0%   { content: ''; }
        20%  { content: '.'; }
        40%  { content: '..'; }
        60%  { content: '...'; }
        80%  { content: '..'; }
        90% { content: '.'; }
        100% { content: ''; }
    }
    </style>

    <div class="loader-container">
        Preparing everything to start<span class="dots"></span>
    </div>
    """,
    unsafe_allow_html=True
)

# Run your expensive setup
MODEL_USAGE_FLAG, get_answer, get_transcription_and_lang, recording = import_starting()

# Remove loader
loader.empty()

# ===== UI continues =====

# Centered buttons (stacked)
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])

with btn_col2:

    if not st.session_state.running:
        
        start = st.button("Let's talk!", width='stretch')

        if start:
            st.session_state.running = True
            st.rerun()

    else:
        stop = st.button("Stop", width='stretch')

        if stop:
            st.session_state.running = False
            st.rerun()


if st.session_state.running:
    status_box = st.empty()

    try:
        while st.session_state.running:
            # 1. Recording ------
            update_status('Listening')
            audio_buffer = recording()

            start_time = time.time()

            # 2. Transcription ------
            update_status('Processing')
            transcription, language_detected = get_transcription_and_lang(audio_buffer)

            if not transcription:
                update_status('Speaking')
                speak("I'm not sure I heard anything. Could you please repeat?", 'en')
                continue

            # 3. Answer generation ------
            update_status('Generating answer')
            model_answer = get_answer(transcription, language_detected) if MODEL_USAGE_FLAG else DEFAULT_ANSWERS.get(language_detected, DEFAULT_ANSWERS['en'])
            
            end_time = time.time()
            print(f"\n** =====*===== Total processing time from transcription to model response : {end_time - start_time:.2f} seconds =====*=====")

            # 4. Speak ------
            update_status('Speaking')
            speak(model_answer, language_detected)
        
    except StopConversation:
        print("\n\nStopped...")
        status_box.empty()
        st.session_state.running = False
        