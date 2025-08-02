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
git clone TakdanaiGH/Qwen-Agent-CMKL-Hackathon.git
cd Qwen-Agent-CMKL-Hackathon
pip install -r requirements.txt
```

### Run the API
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### API Usage
```bash
curl -X POST http://YourPort/eval \
     -H "Content-Type: application/json" \
     -d '{"question":"ผู้ที่ต้องการใส่ฟันปลอมต้องมีอายุเท่าใดขึ้นไป?  ก. 40 ปี ข. 50 ปี ค. 60 ปี ง. ไม่ได้จำกัดอายุ"}'
```


