# 🤖 AI Agent with Tool Calling

An AI agent that decides which tool to use to answer any question.
Built to understand and demonstrate the core concept of **tool calling** in LLM-based agents.

---

## 🧠 How it works

The agent receives a question and decides autonomously which tool to use:

```
User question
    → LLM decides which tool to use
    → Tool executes and returns result
    → LLM formulates final answer with the result
    → Repeat if more tools are needed
```

This loop continues until the LLM has enough information to answer — it can call multiple tools in one conversation turn.

---

## 🔧 Tools

| Tool | Description |
|---|---|
| `get_current_datetime` | Returns the current date and time |
| `web_search` | Searches the web for current information (Tavily) |
| `read_file` | Reads and returns the content of a text or PDF file |

---

## 🛠️ Stack

- **LLM:** Groq API (`openai/gpt-oss-20b`)
- **Web search:** Tavily API (free tier)
- **UI:** Streamlit

---

## 🚀 How to run

### 1. Clone the repository
```bash
git clone https://github.com/Gus-IA/ai-agent.git
cd ai-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 4. Start the app
```bash
streamlit run app.py
```

### 5. Open in browser
```
http://localhost:8501
```

---

## 📁 Project Structure

```
ai-agent/
├── tools/
│   ├── __init__.py
│   ├── datetime_tool.py     # Current date and time
│   ├── web_search.py        # Web search via Tavily
│   └── file_reader.py       # Read text and PDF files
├── agent.py                 # Agent loop with tool calling
├── app.py                   # Streamlit UI
├── requirements.txt
└── .env.example
```

---

## 🔑 Environment Variables

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
LLM_MODEL=openai/gpt-oss-20b
```

- Groq API key (free): [console.groq.com](https://console.groq.com)
- Tavily API key (free): [app.tavily.com](https://app.tavily.com)

---

## 💡 Example Questions

- `What time is it right now?`
- `Search for the latest news about robotics and AI`
- `Read the file data/notes.txt and summarize it`
- `What is the current state of reinforcement learning?`