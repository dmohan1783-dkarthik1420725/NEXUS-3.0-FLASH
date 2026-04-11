import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import pytz
import requests
import random
import io

# --- VEDA 3.1 ULTRA: TELEMETRY-HARDENED CONFIGURATION ---
st.set_page_config(page_title="VEDA 3.1 ULTRA", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    button[kind="header"] { color: #ff8c00 !important; }
    .centered-title { 
        text-align: center; color: #ff8c00; text-shadow: 2px 2px #000000; 
        font-family: 'Courier New', Courier, monospace; margin-top: -30px;
        font-weight: bold; letter-spacing: 2px;
    }
    @keyframes shadowPulse {
        0% { opacity: 0.2; text-shadow: 0 0 5px #000; }
        50% { opacity: 1; text-shadow: 0 0 20px #ff8c00; }
        100% { opacity: 0.2; text-shadow: 0 0 5px #000; }
    }
    .thinking-text {
        text-align: center; color: #ff8c00; font-family: 'Courier New', Courier, monospace;
        font-size: 1.2rem; animation: shadowPulse 2s infinite ease-in-out; margin-bottom: 20px;
    }
    .wip-text {
        color: #ff8c00; font-family: 'Courier New', Courier, monospace;
        font-weight: bold; border: 1px solid #ff8c00; padding: 10px;
        text-align: center; border-radius: 5px; background: rgba(255, 140, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 1. SIDEBAR: THE TRISHUL STATION
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #ff8c00; margin-top: -20px;'>🔱</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>VEDA 3.1 ULTRA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("⌚ **Live Time (IST):**")
    st.components.v1.html("""
        <div id="clock" style="color: white; font-family: 'Courier New', monospace; font-weight: bold; font-size: 16px;"></div>
        <script>
        function updateClock() {
            var now = new Date();
            var options = { timeZone: 'Asia/Kolkata', hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' };
            document.getElementById('clock').innerHTML = now.toLocaleTimeString('en-GB', options);
        }
        setInterval(updateClock, 1000);
        updateClock();
        </script>
    """, height=35)
    st.markdown("---")
    mode = st.radio("SELECT FREQUENCY:", ["MEDHA (CHAT)", "SRIJAN (IMAGE)", "SANGEET (MUSIC)", "DRISHYAM (VIDEO)"])
    st.markdown("---")
    st.info("ARCHITECT: DUMPALA KARTHIK")

# --- MODE: MEDHA (CHAT) ---
if mode == "MEDHA (CHAT)":
    st.markdown("<h1 class='centered-title'>MEDHA: INTELLIGENCE HUB</h1>", unsafe_allow_html=True)
    if prompt := st.chat_input("Command Medha..."):
        with st.chat_message("assistant"):
            pulse = st.empty()
            pulse.markdown("<div class='thinking-text'>🔱 THINKING WITH VEDA...</div>", unsafe_allow_html=True)
            try:
                client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
