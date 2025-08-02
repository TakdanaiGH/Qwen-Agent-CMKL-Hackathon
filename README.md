# Qwen-Agent-CMKL-Hackathon
# 🧠 Medical Reasoning API

This is a FastAPI-based service that leverages the Qwen3-30B-A3B-Thinking-2507 model to evaluate medical multiple-choice questions. It returns a Thai-letter answer (ก, ข, ค, ง) along with a step-by-step reasoning trace.

---

## 📌 Features

- ✅ Uses **Qwen3-30B-A3B** via local model server (`unsloth/Qwen3-30B-A3B-Thinking-2507-FP8`)
- ✅ Final answer extracted from `<answer> ... </answer>` tags
- ✅ Custom tools for streamable HTTP integration (e.g. MCP medical server)
- ✅ Time-limited generation with fallback answer
- ✅ Compact and strict Thai MCQ format

---

## 🚀 Getting Started

### Requirements

- Python 3.10+
- `fastapi`
- `uvicorn`
- `vllm`
- `qwen-agent`
- A running model server via vllm at `http://localhost:8444/v1`

### Installation

```bash
git clone https://github.com/yourusername/medical-reasoning-api.git
cd medical-reasoning-api
pip install -r requirements.txt
```

### API
