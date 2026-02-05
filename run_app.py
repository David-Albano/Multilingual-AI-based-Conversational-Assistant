import streamlit as st

from check_running import StopConversation

if "running" not in st.session_state:
    st.session_state.running = False

def import_starting():
    from test_speech_and_model_response import start_conversation
    return start_conversation

# Page config
st.set_page_config(
    page_title="Ambrósio GPT",
    layout="centered"
)

# Main title
st.markdown(
    "<h1 style='text-align: center;'>Ambrósio GPT</h1>",
    unsafe_allow_html=True
)

st.write("")  # spacer

# Centered logo section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo_3.png", width='content')


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
        font-size: 18px;
        font-weight: 600;
        color: #2f59e2;
    }

    .dots::after {
        content: '';
        animation: dots 1.5s infinite;
    }

    @keyframes dots {
        0% { content: ''; }
        25% { content: '.'; }
        50% { content: '..'; }
        75% { content: '...'; }
    }
    </style>

    <div class="loader-container">
        Preparing everything to start<span class="dots"></span>
    </div>
    """,
    unsafe_allow_html=True
)

# Run your expensive setup
start_talk = import_starting()

# Remove loader
loader.empty()

# ===== UI continues =====

# Centered buttons (stacked)
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])

with btn_col2:

    if not st.session_state.running:
        
        start = st.button("Start", width='stretch')

        if start:
            st.session_state.running = True
            st.rerun()

    else:
        # st.button(
        #     "Conversation started...",
        #     width='stretch',
        #     disabled=True
        # )

        talking_loader = st.empty()

        talking_loader.markdown(
            """
            <style>
            .talking_loader-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 80px;
                font-size: 24px;
                font-weight: 800;
                color: #2f59e2;
            }

            .dots::after {
                content: '';
                animation: dots 1.5s infinite;
            }

            @keyframes dots {
                0% { content: ''; }
                25% { content: '.'; }
                50% { content: '..'; }
                75% { content: '...'; }
            }
            </style>

            <div class="talking_loader-container">
                Talking<span class="dots"></span>
            </div>
            """,
            unsafe_allow_html=True
        )

        stop = st.button("Stop", width='stretch')

        if stop:
            st.session_state.running = False
            print("Stopped...")
            st.rerun()


if st.session_state.running:
    try:
        start_talk()
        
    except StopConversation:
        st.session_state.running = False
        print("\n\nStopped...")
        