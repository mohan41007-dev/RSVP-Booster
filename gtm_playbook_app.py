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
st.set_page_config(page_title="FE fundinfo GTM Engine", page_icon="🌐", layout="wide")

# -------------------------------------------------------------------------
# 🎨 FE FUNDINFO PROFESSIONAL DESIGN SYSTEM (CSS INJECTION)
# -------------------------------------------------------------------------
st.markdown("""
    <style>
        /* Global Background - Deep Institutional Corporate Slate */
        .main {
            background-color: #0A0F18;
            color: #E2E8F0;
        }
        
        /* App Main Header Typography - Clean & Professional */
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

        /* Sidebar Container */
        [data-testid="stSidebar"] {
            background-color: #0F141C !important;
            border-right: 1px solid #1E293B;
        }

        /* 🎯 SIDEBAR ONLY TEXT FIX: Target elements inside the sidebar wrapper exclusively */
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] h2 {
            color: #E2E8F0 !important;
        }

        /* 🎯 CHAT CONTAINER FIX: Clean, readable containers for agent outputs */
        div[data-testid="stChatMessage"] {
            background-color: #131B26 !important;
            border: 1px solid #233145 !important;
            border-radius: 8px !important;
            padding: 1.5rem !important;
            margin-bottom: 1.2rem !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        }

        /* 🎯 CHAT TYPOGRAPHY FIX: Force clear visibility inside chat messages */
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
        
        /* Dynamic headers inside chat boxes */
        div[data-testid="stChatMessage"] h4 {
            color: #00D4FF !important; /* Standout agent names */
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            margin-bottom: 0.75rem !important;
        }

        /* Action Buttons Styling - Flat Professional Teal Accent */
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

        /* Native Download Button Style Override */
        div[data-testid="stDownloadButton"] > button {
            background-color: #10B981 !important; /* Success Green */
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
st.markdown("<h1 class='main-header'>🌐 FE fundinfo <span class='brand-accent'>GTM Playbook Hub</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header-text'>Transform dynamic fund data specifications and asset management architectures into unified distribution materials.</p>", unsafe_allow_html=True)

# Initialize UI session matrices
if "gtm_logs" not in st.session_state:
    st.session_state.gtm_logs = []
if "download_ready" not in st.session_state:
    st.session_state.download_ready = False

# -------------------------------------------------------------------------
# 🏢 SIDEBAR CONTROL HUB
# -------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='font-size:1.2rem; font-weight:700; margin-bottom: 0.5rem;'>🛠️ Configuration Engine</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    target_industry = st.selectbox(
        "Target Market Segment:",
        ("B2B Enterprise SaaS", "FinTech / Payments / WealthTech", "Institutional Asset Managers"),
        index=1
    )
    
    brand_tone = st.radio(
        "Brand Voice Matrix Configuration:",
        ("Bold & Conversational", "Authoritative & Technical", "Compliant & Analytical"),
        index=2
    )
    
    launch_budget = st.slider("Campaign Expenditure Threshold ($):", 5000, 100000, 25000, step=5000)
    
    st.markdown("---")
    submit_btn = st.button("🚀 Run AutoGen Task Force")
    
    st.divider()
    st.caption("🤖 Multi-Agent Framework State: **Operational**")

# --- Main Page Layout Columns ---
col_input, col_output = st.columns([1, 1.2])

with col_input:
    st.markdown("<h3 style='color:#FFFFFF; font-size:1.15rem; font-weight:700; margin-bottom:0.5rem;'>📝 Core Technical Intake Profile</h3>", unsafe_allow_html=True)
    
    default_spec = (
        "PRODUCT NAME: FE fundinfo OpenFunds Hub (NextGen Integration Engine)\n"
        "TECHNICAL FEATURES:\n"
        "- Automated ingestion streams for openfunds-compliant data formats (XLSX, XML, CSV).\n"
        "- Real-time data validation algorithms checking across 500+ regulatory semantic data points (such as MiFID II, PRIIPs EPT, and SFDR templates).\n"
        "- Instant data distribution webhooks communicating with global fund platforms, distributors, and wealth management custodians.\n"
        "- Automated generation of updated fund fact sheets via an asynchronous PDF compilation loop.\n"
        "LIMITATIONS:\n"
        "- Native schema ingestion is strictly limited to openfunds-v1.3 data structures.\n"
        "- Requires mutual API gateway whitelisting and does not support on-premise relational database synchronization."
    )
    
    raw_spec_input = st.text_area("Product Specification Input", value=default_spec, height=360, label_visibility="collapsed")

# -------------------------------------------------------------------------
# AutoGen Multi-Agent Brain Core Loop
# -------------------------------------------------------------------------
async def run_gtm_agent_factory(product_spec: str, industry: str, tone: str, budget: int):
    if not OPENAI_KEY or OPENAI_KEY.strip() == "":
        st.error("🔑 Missing Variable: OPENAI_API_KEY was not found inside your local `.env` file.")
        return []

    model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=OPENAI_KEY)

    router = AssistantAgent(
        name="Input_Router_Agent",
        model_client=model_client,
        system_message=f"Analyze this spec sheet. Extract key capabilities and outline target user limitations within the '{industry}' vertical. Pass your insights to the Product_Marketing_Manager."
    )

    pmm = AssistantAgent(
        name="Product_Marketing_Manager",
        model_client=model_client,
        system_message=f"Convert raw engineering functions into distinct value propositions for asset management buyers. Draft 3 institutional messaging pillars in a strict '{tone}' tone profile. Pass to the Media_Planner."
    )

    media_planner = AssistantAgent(
        name="Media_Planner",
        model_client=model_client,
        system_message=f"Outline a 30-day cross-channel campaign deployment roadmap. Structure an explicit marketing spend distribution chart matching the allocation limit of ${budget:,}. Pass your model framework to the Operations_Director."
    )

    director = AssistantAgent(
        name="Operations_Director",
        model_client=model_client,
        system_message="Review all team inputs. Consolidate the absolute definitive Go-To-Market Strategy Blueprint cleanly using Markdown headings, lists, and tables. Close out the session by concluding with exactly: [PLAYBOOK_COMPILED]"
    )

    termination_rule = TextMentionTermination("[PLAYBOOK_COMPILED]")
    gtm_team = RoundRobinGroupChat(
        participants=[router, pmm, media_planner, director],
        termination_condition=termination_rule,
        max_turns=8
    )

    local_logs = []
    result = await gtm_team.run(task=f"Compile Go-To-Market Playbook assets for this product profile:\n{product_spec}")
    
    for msg in result.messages:
        role_map = "user" if msg.source == "Operations_Director" else "assistant"
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
        if not raw_spec_input.strip():
            st.warning("Please insert some engineering specifications first.")
        else:
            st.session_state.gtm_logs = []
            st.session_state.download_ready = False
            
            with st.spinner("Processing framework logic... Core task force compiling data matrices..."):
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    compiled_results = loop.run_until_complete(run_gtm_agent_factory(
                        product_spec=raw_spec_input,
                        industry=target_industry,
                        tone=brand_tone,
                        budget=launch_budget
                    ))
                    
                    st.session_state.gtm_logs = compiled_results
                    st.session_state.download_ready = True
                    loop.close()
                    
                    if st.session_state.gtm_logs:
                        st.balloons()
                        
                except Exception as e:
                    st.error(f"### 💥 AutoGen Runtime Error:\n{str(e)}")

    # Render clean markdown text blocks inside corrected high-visibility chat components
    if st.session_state.gtm_logs:
        with live_output_window.container():
            for log in st.session_state.gtm_logs:
                with st.chat_message(log["role"]):
                    st.markdown(f"#### 🤖 {log['sender']}")
                    st.markdown(log["content"])
            
            # --- ASSET EXPORT INTERFACE MODULE ---
            if st.session_state.download_ready:
                st.markdown("### 📥 Export Final Asset Package")
                
                raw_download_payload = f"# GO-TO-MARKET PLAYBOOK STRATEGY\n"
                raw_download_payload += f"**Target Vertical Segment:** {target_industry}\n"
                raw_download_payload += f"**Brand Compliance Voice:** {brand_tone}\n"
                raw_download_payload += f"**Financial Allocation Budget Limit:** ${launch_budget:,}\n\n"
                raw_download_payload += "---\n\n"
                
                for log in st.session_state.gtm_logs:
                    raw_download_payload += f"## Agent Contribution: {log['sender']}\n"
                    raw_download_payload += f"{log['content']}\n\n"
                    raw_download_payload += "---\n\n"
                
                st.download_button(
                    label="📥 Download GTM Playbook Document (.md)",
                    data=raw_download_payload,
                    file_name="FE_fundinfo_GTM_Playbook.md",
                    mime="text/markdown"
                )