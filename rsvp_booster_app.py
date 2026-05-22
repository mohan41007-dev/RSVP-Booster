import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load secure environment tokens from .env file
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_API_KEY')

# --- Streamlit Web Presentation Configuration ---
st.set_page_config(page_title="FE fundinfo RSVP Booster", page_icon="📈", layout="wide")

# -------------------------------------------------------------------------
# 🎨 FE FUNDINFO DESIGN SYSTEM (CSS INJECTION)
# -------------------------------------------------------------------------
st.markdown("""
    <style>
        /* Global Background Adjustments - Deep Institutional Slate */
        .main {
            background-color: #0A0F18;
            color: #E2E8F0;
        }
        
        /* App Main Header Typography */
        .main-header {
            font-size: 2.4rem !important;
            font-weight: 800 !important;
            color: #FFFFFF;
            margin-bottom: 0.2rem;
            letter-spacing: -0.03em;
        }
        .brand-accent {
            color: #00D4FF; /* FE fundinfo Digital Cyan Accent */
        }
        
        .sub-header-text {
            color: #94A3B8;
            font-size: 1.05rem;
            margin-bottom: 2rem;
        }

        /* Sidebar Container Layout */
        [data-testid="stSidebar"] {
            background-color: #0F141C !important;
            border-right: 1px solid #1E293B;
        }

        /* Sidebar exclusive text alignment */
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] h2 {
            color: #E2E8F0 !important;
        }

        /* Chat Message Frames High-Visibility Override */
        div[data-testid="stChatMessage"] {
            background-color: #131B26 !important;
            border: 1px solid #233145 !important;
            border-radius: 8px !important;
            padding: 1.5rem !important;
            margin-bottom: 1.2rem !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        }

        /* Chat Inner Typography Visibility */
        div[data-testid="stChatMessage"] p, 
        div[data-testid="stChatMessage"] li, 
        div[data-testid="stChatMessage"] h1, 
        div[data-testid="stChatMessage"] h2, 
        div[data-testid="stChatMessage"] h3, 
        div[data-testid="stChatMessage"] h4 {
            color: #FFFFFF !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
        }
        
        /* Agent Name Headings inside chat boxes */
        div[data-testid="stChatMessage"] h4 {
            color: #00D4FF !important;
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            margin-bottom: 0.75rem !important;
        }

        /* Trigger Action Button Styling */
        div.stButton > button:first-child {
            background-color: #00D4FF !important;
            color: #0A0F18 !important;
            font-weight: 700 !important;
            border: none !important;
            padding: 0.6rem 1.5rem !important;
            border-radius: 6px !important;
            transition: all 0.2s ease-in-out !important;
            width: 100% !important;
            margin-top: 1rem;
        }
        
        div.stButton > button:first-child:hover {
            background-color: #00B4D8 !important;
            transform: translateY(-1px) !important;
        }

        /* Download Button Component Override */
        div[data-testid="stDownloadButton"] > button {
            background-color: #10B981 !important;
            color: white !important;
            font-weight: 700 !important;
            border: none !important;
            padding: 0.6rem 1.5rem !important;
            border-radius: 6px !important;
            width: 100% !important;
        }
        div[data-testid="stDownloadButton"] > button:hover {
            background-color: #059669 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Display Styled Brand Header ---
st.markdown("<h1 class='main-header'>🌐 FE fundinfo <span class='brand-accent'>RSVP Booster Squad</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header-text'>Autonomous tracking velocity monitor intercepts and corrects registration deficits for institutional fund webinars.</p>", unsafe_allow_html=True)

# Initialize UI session matrices for runtime memory tracking
if "booster_logs" not in st.session_state:
    st.session_state.booster_logs = []
if "booster_download_ready" not in st.session_state:
    st.session_state.booster_download_ready = False

# -------------------------------------------------------------------------
# 🏢 SIDEBAR TRACKING CONFIGURATION HUB
# -------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='font-size:1.2rem; font-weight:700; margin-bottom: 0.5rem;'>📊 Live Event Telemetry</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    days_to_go = st.slider("Days Remaining Until Event Launch:", 2, 30, 10)
    current_rsvps = st.number_input("Current Verified RSVP Ingest Count:", min_value=0, value=42)
    target_rsvps = st.number_input("Target Seat Registration Threshold:", min_value=10, value=150)
    
    st.markdown("---")
    st.markdown("<h2 style='font-size:1.1rem; font-weight:700;'>🎯 Intervention Settings</h2>", unsafe_allow_html=True)
    booster_channel = st.selectbox("Primary Rescue Channel Focus:", ("Targeted LinkedIn Direct-Match", "Urgent Segmented Email Blast", "Co-Marketing Partner Push"))
    
    st.markdown("---")
    submit_btn = st.button("🚀 Analyze Metric Velocity")
    
    st.divider()
    st.caption("🤖 Multi-Agent Pipeline Status: **Online**")

# --- Main Page Layout Matrix Columns ---
col_input, col_output = st.columns([1, 1.2])

with col_input:
    st.markdown("<h3 style='color:#FFFFFF; font-size:1.15rem; font-weight:700; margin-bottom:0.5rem;'>📝 Live Webinar Ingestion Summary</h3>", unsafe_allow_html=True)
    
    # Pre-calculated telemetry diagnostics box
    calculated_velocity = round(current_rsvps / days_to_go, 2)
    deficit = target_rsvps - current_rsvps
    required_velocity = round(deficit / days_to_go, 2)
    
    telemetry_summary = (
        f"EVENT PROFILE: Q3 Global ESG Fund Compliance Briefing\n"
        f"ACTIVE TELEMETRY SUMMARY:\n"
        f"- Registration Runway: {days_to_go} Days Remaining.\n"
        f"- Target Attendee Seats: {target_rsvps} Profiles.\n"
        f"- Current Registered Seats: {current_rsvps} Profiles.\n"
        f"- Gross Seat Deficit: {deficit} Registrations Required.\n"
        f"VELOCITY DATA METRICS:\n"
        f"- Current Registration Pace: {calculated_velocity} sign-ups per day.\n"
        f"- Target Pace Needed: {required_velocity} sign-ups per day.\n"
        f"CRISIS ANALYSIS STATUS:\n"
        f"Warning: Registration tracking velocity profile is pacing significantly below model goals."
    )
    
    raw_telemetry_input = st.text_area("Webinar Ingestion Summary", value=telemetry_summary, height=360, label_visibility="collapsed")

# -------------------------------------------------------------------------
# AutoGen Multi-Agent Brain Core Loop
# -------------------------------------------------------------------------
async def run_booster_agent_factory(telemetry_data: str, rescue_channel: str):
    if not OPENAI_KEY or OPENAI_KEY.strip() == "":
        st.error("🔑 Missing Variable: OPENAI_API_KEY was not found inside your local `.env` file.")
        return []

    model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=OPENAI_KEY)

    # 1. THE DATA INGEST ROUTER
    router = AssistantAgent(
        name="Telemetry_Analyst_Agent",
        model_client=model_client,
        system_message="Analyze the raw event pacing metrics. Isolate the target seat deficit and calculate the daily registration acquisition increase required to save the event pipeline. Hand parameters to the Growth_Hacker."
    )

    # 2. THE GROWTH HACKER
    growth_hacker = AssistantAgent(
        name="Growth_Hacker_Strategist",
        model_client=model_client,
        system_message=f"Review the data metrics analysis. Formulate a highly direct, high-conversion promotional campaign strategy explicitly tailored for the chosen target channel: '{rescue_channel}'. Pass the tactical plan framework to the Copywriter."
    )

    # 3. THE COPYWRITER
    copywriter = AssistantAgent(
        name="Ad_Copywriter_Agent",
        model_client=model_client,
        system_message="Review the strategy plan. Write ready-to-deploy, high-urgency marketing copy assets (e.g., ad variations, catchy email hooks, or urgency messaging tags) designed to drive instant sign-ups. Pass text blocks to the Director."
    )

    # 4. THE OPERATIONS DIRECTOR
    director = AssistantAgent(
        name="Intervention_Director",
        model_client=model_client,
        system_message="Consolidate all tracking calculations, channel strategy structures, and copy assets into a unified Event Rescue & RSVP Playbook. Conclude the session message exactly with: [BOOSTER_DEPLOYED]"
    )

    termination_rule = TextMentionTermination("[BOOSTER_DEPLOYED]")
    booster_team = RoundRobinGroupChat(
        participants=[router, growth_hacker, copywriter, director],
        termination_condition=termination_rule,
        max_turns=8
    )

    local_logs = []
    result = await booster_team.run(task=f"Formulate an event pacing correction model for this telemetry log:\n{telemetry_data}")
    
    for msg in result.messages:
        role_map = "user" if msg.source == "Intervention_Director" else "assistant"
        local_logs.append({
            "sender": msg.source.replace("_", " "),
            "content": msg.content,
            "role": role_map
        })
    
    return local_logs

# -------------------------------------------------------------------------
# Output Rendering Interface Column
# -------------------------------------------------------------------------
with col_output:
    st.markdown("<h3 style='color:#00D4FF; font-size:1.15rem; font-weight:700; margin-bottom:0.5rem;'>📊 Live Strategy Blueprint Stream</h3>", unsafe_allow_html=True)
    live_output_window = st.empty()
    
    if submit_btn:
        st.session_state.booster_logs = []
        st.session_state.booster_download_ready = False
        
        with st.spinner("Pacing metrics evaluated. Ingestion Router deploying task force..."):
            try:
                # Isolate the thread loop to ensure compatibility with Streamlit
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                compiled_results = loop.run_until_complete(run_booster_agent_factory(
                    telemetry_data=raw_telemetry_input,
                    rescue_channel=booster_channel
                ))
                
                st.session_state.booster_logs = compiled_results
                st.session_state.booster_download_ready = True
                loop.close()
                
                if st.session_state.booster_logs:
                    st.balloons()
                    
            except Exception as e:
                st.error(f"### 💥 AutoGen Runtime Error:\n{str(e)}")

    # Clean rendering of agent text frames
    if st.session_state.booster_logs:
        with live_output_window.container():
            for log in st.session_state.booster_logs:
                with st.chat_message(log["role"]):
                    st.markdown(f"#### 🤖 {log['sender']}")
                    st.markdown(log["content"])
            
            # --- DOWNLOAD DATA COMPONENT ---
            if st.session_state.booster_download_ready:
                st.markdown("### 📥 Export Intervention Package")
                
                raw_download_payload = f"# WEBINAR RSVP BOOSTER INTERVENTION PLAYBOOK\n"
                raw_download_payload += f"**Rescue Channel Execution Focus:** {booster_channel}\n\n"
                raw_download_payload += "---\n\n"
                
                for log in st.session_state.booster_logs:
                    raw_download_payload += f"## Agent Block: {log['sender']}\n"
                    raw_download_payload += f"{log['content']}\n\n"
                    raw_download_payload += "---\n\n"
                
                st.download_button(
                    label="📥 Download RSVP Intervention Plan (.md)",
                    data=raw_download_payload,
                    file_name="FE_fundinfo_RSVP_Rescue_Plan.md",
                    mime="text/markdown"
                )