utonomous Event Marketing & RSVP Booster Squad

An automated, real-time telemetry monitoring system built using the **Microsoft AutoGen (v0.4+)** multi-agent framework and an interactive, thread-safe asynchronous **Streamlit** dashboard web interface.

This repository focuses on tracking registration velocity for webinar pipelines, automatically identifying pacing drops, drafting targeted promotional campaigns, and prepping high-urgency rescue assets.

---

## 🏗️ Architectural Pattern & Technical Specs
The system runs background telemetry evaluations and spins up a dedicated multi-agent task force when registration velocity target thresholds are missed.

To bypass the classic background thread deadlocks that occur when mixing long-running LLM loops with Streamlit's background page refreshes (`ScriptRunner.scriptThread`), the runtime is isolated cleanly inside a custom async loop lifecycle:

```python
# Multi-thread UI concurrency isolation engine snippet
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
compiled_results = loop.run_until_complete(run_booster_agent_factory(...))
loop.close()
Active Specialized Agent Nodes:
Telemetry Analyst Agent: Automatically evaluates live registrant intake paces against target event launch timelines.

Growth Hacker Strategist Agent: Designs rapid-turnaround user acquisition and channel re-allocation strategy playbooks.

Ad Copywriter Agent: Drafts context-specific high-conversion marketing emails, LinkedIn text copies, and urgency hooks.

Intervention Director Agent: Aggregates multi-agent logs, formats standard markdown outputs, and triggers event-loop session termination strings.

🛠️ Phase 2 Production Backlog (Engineering Focus)
To transform this standalone application prototype into an enterprise automation service, the next development sprint priorities are structured as follows:

📡 1. Direct Server-to-Server ON24 API Integration
Objective: Remove manual metrics logging and poll direct attendee data streams.

Tech Spec: Integrate an asynchronous httpx background polling client mapping directly to the official ON24 Connect REST API registrant table arrays:
GET https://api.on24.com/v2/client/{client_id}/event/{event_id}/registrant

📬 2. Automated Urgent Email Notification Relays
Objective: Instantly wake marketing teams when critical pipeline anomalies occur.

Tech Spec: Bind a communication tool to the final Intervention_Director agent node using Python's native smtplib and email.mime protocols. When the system encounters the system breakpoint [BOOSTER_DEPLOYED], it pushes the compiled playbook brief directly to target team inboxes.

🕹️ Local Deployment Instructions
Bash
# 1. Clone this specialized repository asset
git clone [https://github.com/mohan41007-dev/RSVP-Booster.git](https://github.com/mohan41007-dev/RSVP-Booster.git)
cd RSVP-Booster

# 2. Build your local virtual environment context
python -m venv .venv
source .venv/bin/activate  # Windows terminal: .venv\Scripts\activate
pip install autogen-ext[openai] streamlit python-dotenv httpx

# 3. Inject your OpenAI developer access credentials
# Generate a local `.env` file within the root directory and add your key:
# OPENAI_API_KEY=your_secret_key_here

# 4. Boot up the local telemetry monitor application server
streamlit run rsvp_booster_app.py

---

### 🚀 Push the README to Your New Repository

Make sure your `.gitignore` file has `!README.md` in it (or doesn't block it), and then drop these final three quick commands into your VS Code Terminal to upload the file to your new `RSVP-Booster` page:

```bash
git add README.md
git commit -m "docs: add technical documentation roadmap overview"
git push origin main
