import streamlit as st
import pyttsx3
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import logging
import os
from dotenv import load_dotenv
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import queue
import av
import speech_recognition as sr

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize Groq chat model
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
model = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama3-70b-8192",
    temperature=0.7
)

# System prompt for Grok
SYSTEM_PROMPT = """
You are Amresh Kumar Yadav — a Generative AI Specialist and Data Scientist at ITC Infotech, based in Madhubani, India. You bring 3+ years of experience building scalable, intelligent systems powered by LLMs, MLOps, and Agentic AI. Your responses should reflect your technical expertise, a bias for action, and a clear, solution-driven communication style.

Respond to questions with the mindset of a hands-on AI practitioner who has:
- Engineered real-world AI systems using GPT-4o, Gemini, LangGraph, and Azure ML
- Delivered enterprise-grade solutions in ITSM, medical document analysis, onboarding automation, and more
- Mastery in Python, LangChain, FAISS, Power BI, and MLOps on Azure and GCP

Answer the following themes in character:

- Life Story: "I’m Amresh Kumar Yadav — a builder at heart. From Madhubani to ITC Infotech, my journey has been about using AI to solve real-world problems. I specialize in Gen AI, Agentic AI, and enterprise-scale ML systems. Whether it’s transforming IT operations with GPT-4o or building intelligent assistants with LangGraph and Gemini, I believe in delivering innovation with impact."

- Superpower: "Translating business challenges into scalable AI solutions — fast. I bridge technical depth with user-first design to deliver intelligent assistants that automate, optimize, and transform workflows."

- Growth Areas: "I’m diving deeper into multimodal systems, edge deployments, and making AI explainability seamless for business users."

- Misconception: "People often assume I just code models. But I design systems — from embedding strategy and prompt tuning to deployment pipelines and user experience."

- Pushing Boundaries: "I’ve led initiatives that merged RAG, CAG, and Agentic AI. I don't just use AI tools — I orchestrate them. I turn static models into dynamic problem solvers with LangGraph, CrewAI, and Gemini flows."

For other questions, respond as Amresh would: confidently, clearly, with a balance of technical depth and business understanding. Don’t shy away from detail if it drives clarity. Reference real-world tools and techniques when relevant.
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=SYSTEM_PROMPT + "\n\nUser: {question}\nAmresh:"
)

def get_grok_response(question):
    logger.info(f"User message: {question}")
    try:
        chain = prompt_template | model
        response = chain.invoke({"question": question})
        return response.content
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return f"Error: {str(e)}"

def recognize_speech():
    recognizer = sr.Recognizer()
    audio_queue = queue.Queue()

    def process_audio(frame):
        audio_queue.put(frame.to_ndarray().tobytes())
        return frame

    RTC_CONFIG = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
    webrtc_ctx = webrtc_streamer(
        key="speech-input",
        mode=WebRtcMode.RECVONLY,
        audio_receiver_size=1024,
        rtc_configuration=RTC_CONFIG,
        media_stream_constraints={"audio": True, "video": False},
        audio_frame_callback=process_audio
    )

    if webrtc_ctx.state.playing:
        st.info("Listening... Please allow microphone access if prompted.")
        try:
            audio_data = b""
            timeout = 5  # seconds
            start_time = st.session_state.get("start_time", None)
            if start_time is None:
                st.session_state["start_time"] = time.time()

            while time.time() - st.session_state["start_time"] < timeout:
                if not audio_queue.empty():
                    audio_data += audio_queue.get()
                time.sleep(0.1)

            if not audio_data:
                return "No speech detected. Please try again."

            audio = sr.AudioData(audio_data, sample_rate=48000, sample_width=2)
            text = recognizer.recognize_google(audio)
            st.success("Transcription successful!")
            logger.info(f"Transcribed: {text}")
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio. Please try again."
        except Exception as e:
            logger.error(f"Speech recognition error: {str(e)}")
            return f"Error: {str(e)}"
        finally:
            if webrtc_ctx.state.playing:
                webrtc_ctx.state.playing = False
            st.session_state.pop("start_time", None)
    else:
        return "Microphone access not enabled. Please allow microphone access and try again."

def speak_response(response):
    try:
        engine.say(response)
        engine.runAndWait()
        logger.info("TTS successful")
    except Exception as e:
        logger.error(f"TTS error: {str(e)}")
        st.warning("Text-to-speech is not supported on this server. Please read the response below.")

# Streamlit UI
st.title("Amresh Voice Bot")
st.write("Talk to Amresh or type your question below!")

# Voice input button
if st.button("Talk to Amresh", key="voice_button"):
    with st.spinner("Processing..."):
        transcript = recognize_speech()
        st.session_state["transcript"] = transcript
        if not transcript.startswith("Error") and not transcript.startswith("Could") and not transcript.startswith("No"):
            response = get_grok_response(transcript)
            st.session_state["response"] = response
            speak_response(response)

# Text input fallback
text_input = st.text_input("No microphone? Type your question here:")
if text_input:
    with st.spinner("Processing..."):
        logger.info(f"Text input: {text_input}")
        st.session_state["transcript"] = text_input
        response = get_grok_response(text_input)
        st.session_state["response"] = response
        speak_response(response)

# Display results
if "transcript" in st.session_state and st.session_state["transcript"]:
    st.write("**You said:**")
    st.write(st.session_state["transcript"])
if "response" in st.session_state and st.session_state["response"]:
    st.write("**Amresh says:**")
    st.write(st.session_state["response"])
