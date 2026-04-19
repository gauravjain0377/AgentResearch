# ❖ Agent Research
**Distributed Swarm Protocol**

Agent Research is a highly-technical, multi-agent AI framework designed to autonomously conduct deep research, synthesize findings, and generate comprehensive intelligence briefs on any given target.

Built with an aggressive, dark-mode aesthetic and powered by a distributed "swarm" of specialized AI agents, the system completely automates the traditional research pipeline.

## 🧠 The Swarm Architecture
The engine relies on four distinct agents working in unison:
1. **Phase I: Scout (Reconnaissance)** - Scans the live web using advanced search vectors to identify the most relevant, high-fidelity sources.
2. **Phase II: Synthesizer (Deep Extraction)** - Parses the raw HTML of primary sources, extracting only the most critical context.
3. **Phase III: Author (Synthesis)** - Drafts the primary intelligence brief using the extracted data, organizing it into a professional, easily digestible markdown format.
4. **Phase IV: Auditor (Peer Review)** - Critiques the generated brief for accuracy, bias, and completeness, acting as a final layer of quality control.

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/agent-research.git
cd agent-research
```

### 2. Set up the environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add your Environment Variables
Create a `.env` file in the root directory and add your OpenAI API Key (or other necessary keys):
```toml
OPENAI_API_KEY="sk-your-key-here"
```

### 4. Execute the Protocol
Launch the sleek, dark-mode Streamlit UI:
```bash
streamlit run app.py
```

## 🛠️ Tech Stack
- **Frontend & UI**: Streamlit (with custom CSS for a premium, high-contrast dark aesthetic)
- **Agent Framework**: LangChain
- **LLM Engine**: OpenAI GPT (configurable)
- **Search capabilities**: LangChain native tools / Tavily

---
*Developed for autonomous intelligence gathering and accelerated learning.*
