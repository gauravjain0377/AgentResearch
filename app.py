import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

st.set_page_config(
    page_title="Agent Research · Intelligence Engine",
    page_icon="❖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    box-sizing: border-box;
}

.stApp {
    background: #000000;
    background-image:
        radial-gradient(ellipse 60% 50% at 15% 0%, rgba(34, 211, 238, 0.08) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 85% 100%, rgba(16, 185, 129, 0.05) 0%, transparent 55%);
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem; max-width: 1280px; }

/* Hero */
.hero {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    padding: 2.5rem 0 1.5rem;
    width: 100%;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 100px;
    padding: 0.4rem 1.2rem;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #a3e635;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.6rem, 5.5vw, 4.5rem);
    font-weight: 700;
    line-height: 1.0;
    letter-spacing: -0.04em;
    color: #ffffff;
    margin: 0 0 1rem;
    text-align: center !important;
}
.hero h1 .accent {
    background: linear-gradient(135deg, #a3e635 0%, #22d3ee 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #94a3b8;
    max-width: 550px;
    margin: 0 auto !important;
    line-height: 1.6;
    text-align: center !important;
}

/* Divider */
.hr {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    margin: 1.5rem 0;
}

/* Input Card */
.input-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 1.8rem 2rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(12px);
}

/* Base Input & Buttons Overrides for Streamlit */
/* Making inputs look dark and sleek */
[data-testid="stTextInput"] input {
    background: #0a0a0a !important;
    border: 1px solid #333 !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    padding: 0.8rem 1rem !important;
    font-size: 1rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #22d3ee !important;
    box-shadow: 0 0 0 2px rgba(34, 211, 238, 0.2) !important;
}
[data-testid="stTextInput"] label {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #a3e635 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-size: 0.75rem !important;
}

/* Primary Button */
[data-testid="baseButton-secondary"] {
    background: rgba(255,255,255,0.05) !important;
    color: #cbd5e1 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    transition: all 0.2s !important;
}
[data-testid="baseButton-secondary"]:hover {
    background: rgba(255,255,255,0.1) !important;
    color: #fff !important;
    border-color: rgba(255,255,255,0.2) !important;
}

[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #a3e635 0%, #22d3ee 100%) !important;
    color: #000000 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 2rem !important;
    box-shadow: 0 4px 15px rgba(34,211,238,0.2) !important;
}
[data-testid="baseButton-primary"]:hover {
    box-shadow: 0 6px 20px rgba(34,211,238,0.4) !important;
    transform: translateY(-1px);
}

/* Suggestion Chips Area */
.chip-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    color: #64748b;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    display: inline-block;
    margin-bottom: 0.5rem;
}

/* Pipeline section */
.pipeline-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 1.2rem;
}

/* Step Card */
.step-card {
    background: #0a0a0a;
    border: 1px solid #1a1a1a;
    border-radius: 14px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: all 0.3s;
}
.step-card.active {
    background: rgba(34, 211, 238, 0.05);
    border-color: rgba(34, 211, 238, 0.3);
}
.step-card.done {
    background: rgba(16, 185, 129, 0.03);
    border-color: rgba(16, 185, 129, 0.2);
}

/* Step number badge */
.step-badge {
    position: relative;
    width: 44px;
    height: 44px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}
.step-badge-inner {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    position: relative;
    z-index: 1;
}
.badge-waiting .step-badge-inner {
    background: #111;
    border: 1px solid #222;
    color: #444;
}
.badge-active .step-badge-inner {
    background: rgba(34, 211, 238, 0.1);
    border: 1px solid rgba(34, 211, 238, 0.4);
    color: #22d3ee;
}
.badge-done .step-badge-inner {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.4);
    color: #10b981;
}

/* Spinning ring */
.spin-ring {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 2px solid transparent;
    border-top-color: #22d3ee;
    border-right-color: rgba(34,211,238,0.3);
    animation: spin 1s linear infinite;
}
@keyframes spin {
    to { transform: rotate(360deg); }
}

.step-info { flex: 1; }
.step-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 0.2rem;
    line-height: 1.2;
}
.step-desc {
    font-size: 0.8rem;
    color: #64748b;
}
.step-status {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    flex-shrink: 0;
    text-transform: uppercase;
}
.s-waiting { color: #333; }
.s-active  { color: #22d3ee; }
.s-done    { color: #10b981; }

/* Section label */
.section-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #94a3b8;
    margin: 2rem 0 1rem;
}

/* Result panels */
.result-panel {
    background: #0a0a0a;
    border: 1px solid #1a1a1a;
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 0.5rem;
}
.result-panel-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #a3e635;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1a1a1a;
}
.result-content {
    font-size: 0.9rem;
    line-height: 1.6;
    color: #cbd5e1;
    white-space: pre-wrap;
}

.report-panel {
    background: #0a0a0a;
    border: 1px solid rgba(34, 211, 238, 0.2);
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1rem;
}
.feedback-panel {
    background: #0a0a0a;
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1rem;
}
.panel-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    padding-bottom: 0.8rem;
}
.panel-label.cyan {
    color: #22d3ee;
    border-bottom: 1px solid rgba(34, 211, 238, 0.1);
}
.panel-label.emerald {
    color: #10b981;
    border-bottom: 1px solid rgba(16, 185, 129, 0.1);
}

/* Markdown overrides */
.report-panel p, .feedback-panel p,
.report-panel li, .feedback-panel li {
    color: #cbd5e1 !important;
    font-size: 1rem !important;
    line-height: 1.7 !important;
}
.report-panel h1, .report-panel h2, .report-panel h3,
.feedback-panel h1, .feedback-panel h2, .feedback-panel h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    margin-top: 1.5rem !important;
}

/* Expander */
details summary {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.8rem !important;
    color: #94a3b8 !important;
    letter-spacing: 0.05em !important;
    cursor: pointer;
}

/* Footer*/
.footer {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    color: #333;
    text-align: center;
    margin-top: 4rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# Helper: step card
def step_card(num: str, title: str, desc: str, state: str):
    if state == "running":
        badge_cls = "badge-active"
        status_html = '<span class="step-status s-active">● Active</span>'
        spin_html   = '<div class="spin-ring"></div>'
        card_cls    = "active"
        num_display = num
    elif state == "done":
        badge_cls = "badge-done"
        status_html = '<span class="step-status s-done">✓ Verified</span>'
        spin_html   = ""
        card_cls    = "done"
        num_display = "✓"
    else:
        badge_cls = "badge-waiting"
        status_html = '<span class="step-status s-waiting">Standby</span>'
        spin_html   = ""
        card_cls    = ""
        num_display = num

    st.markdown(f"""<div class="step-card {card_cls}">
<div class="step-badge {badge_cls}">
{spin_html}
<div class="step-badge-inner">{num_display}</div>
</div>
<div class="step-info">
<div class="step-title">{title}</div>
<div class="step-desc">{desc}</div>
</div>
{status_html}
</div>""", unsafe_allow_html=True)


# Session state
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False

if "topic_input_widget" not in st.session_state:
    st.session_state.topic_input_widget = ""

def set_topic(topic: str):
    st.session_state.topic_input_widget = topic


# Hero
st.markdown("""
<div class="hero">
    <div class="hero-badge">❖ DISTRIBUTED INTELLIGENCE</div>
    <h1>Agent<span class="accent">Research</span></h1>
    <p class="hero-sub">
        A cooperative swarm of specialized agents-Scout, Synthesizer, Author, and Auditor-working in unison to generate comprehensive, verified intelligence briefs.
    </p>
</div>
<div class="hr"></div>
""", unsafe_allow_html=True)


# Layout
col_left, col_gap, col_right = st.columns([5, 0.4, 4])

with col_left:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    
    # We use the key to let session state auto-sync with the widget
    topic = st.text_input(
        "Intelligence Target",
        placeholder="e.g. AGI timelines and architectural breakthroughs...",
        key="topic_input_widget",
    )

    run_btn = st.button("Execute Protocol", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chip-label">Quick Directives</div>', unsafe_allow_html=True)
    
    # Clickable Suggestion Chips using columns
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.button("AGI", key="c_agi", on_click=set_topic, args=("Recent architectural breakthroughs in AGI",))
    with c2:
        st.button("CRISPR", key="c_crispr", on_click=set_topic, args=("Clinical trials for CRISPR therapies",))
    with c3:
        st.button("Fusion", key="c_fusion", on_click=set_topic, args=("Commercial viability of magnetic fusion",))
    with c4:
        st.button("Quantum", key="c_quantum", on_click=set_topic, args=("Developments in logical quantum qubits",))

with col_right:
    st.markdown('<div class="pipeline-title">⬡ Execution Graph</div>', unsafe_allow_html=True)

    r    = st.session_state.results
    steps = ["search", "reader", "writer", "critic"]

    def get_state(step):
        if not r and not st.session_state.running:
            return "waiting"
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("I",   "Phase I: Reconnaissance",  "Scans the web for live data",           get_state("search"))
    step_card("II",  "Phase II: Deep Extraction","Parses and extracts primary sources",    get_state("reader"))
    step_card("III", "Phase III: Synthesis",     "Drafts the intelligence brief",          get_state("writer"))
    step_card("IV",  "Phase IV: Peer Review",    "Critiques and refines the output",       get_state("critic"))


# Trigger
if run_btn:
    if not st.session_state.topic_input_widget.strip():
        st.warning("Please enter an intelligence target first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done    = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results   = {}
    topic_val = st.session_state.topic_input_widget

    with st.spinner("📡  Deploying Scout Agent..."):
        search_agent = build_search_agent()
        sr = search_agent.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]})
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("🧠  Deploying Synthesizer Agent..."):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({"messages": [("user",
            f"Based on the following search results about '{topic_val}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{results['search'][:800]}")]})
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("✍️  Deploying Author Agent..."):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({"topic": topic_val, "research": research_combined})
        st.session_state.results = dict(results)

    with st.spinner("⚖️  Deploying Auditor Agent..."):
        results["critic"] = critic_chain.invoke({"report": results["writer"]})
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done    = True
    st.rerun()


# Results
r = st.session_state.results

if r:
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">⬡ Output Brief</div>', unsafe_allow_html=True)

    if "search" in r or "reader" in r:
        col_r1, col_r2 = st.columns(2)
        if "search" in r:
            with col_r1:
                with st.expander("📡 Scout Telemetry"):
                    st.markdown(
                        f'<div class="result-panel"><div class="result-panel-title">Raw Search Vectors</div>'
                        f'<div class="result-content">{r["search"]}</div></div>',
                        unsafe_allow_html=True)
        if "reader" in r:
            with col_r2:
                with st.expander("🧠 Synthesizer Telemetry"):
                    st.markdown(
                        f'<div class="result-panel"><div class="result-panel-title">Extracted Context</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>',
                        unsafe_allow_html=True)

    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label cyan">📄 Primary Intelligence Brief</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="⬇  Export Intelligence (.md)",
            data=r["writer"],
            file_name=f"nexus_brief_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label emerald">⚖️ Auditor Review Logs</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# Footer
st.markdown("""
<div class="footer">
    Agent Research · Distributed Swarm Protocol
</div>
""", unsafe_allow_html=True)