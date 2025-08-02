import re
import concurrent.futures
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from qwen_agent.agents import Assistant
from qwen_agent.tools.base import BaseTool, register_tool
from qwen_agent.utils.output_beautify import typewriter_print

app = FastAPI()

llm_cfg = {
    'model': 'unsloth/Qwen3-30B-A3B-Thinking-2507-FP8',
    'model_server': 'http://localhost:8444/v1',
    'api_key': 'EMPTY',
    'generate_cfg': {
        'top_p': 0.2,
    }
}

tools = [{
    "mcpServers": {
        "medical": {
            "url": "https://mcp-hackathon.cmkl.ai/mcp",
            "type": "streamable-http"
        }
    }
}]

system_prompt = """
    You are a world-renowned medical expert.
    Think step-by-step and write your reasoning inside <think> ... </think> tags.
    You must always finish your reasoning and write the final answer BEFORE reaching the end of the output.
    Finally, give your final answer ONLY as one of ก, ข, ค, ง inside <answer> ... </answer> tags. Use only these letters for your answer (can't have even special character).
    Do not write anything else outside these tags.
    Think compactly and directly, avoid overthinking, and answer precisely.
"""

files = ["combined_ocr.txt"]

bot = Assistant(llm=llm_cfg,
                system_message=system_prompt,
                function_list=tools,
                files=files)

class QueryRequest(BaseModel):
    question: str

def run_bot(messages):
    response_plain_text = ''
    for response in bot.run(messages=messages):
        response_plain_text = typewriter_print(response, response_plain_text)
    return response_plain_text

def clean_answer(raw_answer: str) -> str:
    # Keep only ก, ข, ค, ง and remove everything else
    allowed_chars = "กขคง"
    cleaned = ''.join([ch for ch in raw_answer if ch in allowed_chars])
    return cleaned if cleaned else 'ก'  # default ก if nothing left

@app.get("/")
def read_root():
    return {"status": "OK"}

@app.post("/eval")
def make_request(request: QueryRequest):
    question = request.question
    messages = [{'role': 'user', 'content': question}]

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_bot, messages)
            response_plain_text = future.result(timeout=90)
    except concurrent.futures.TimeoutError:
        return {
            "question": question,
            "answer": "ก",
            "reason": ""
        }

    # Extract <answer> content
    answer_match = re.search(r"<answer>\s*(.*?)\s*</answer>", response_plain_text)
    raw_answer = answer_match.group(1).strip() if answer_match else 'ก'
    final_answer = clean_answer(raw_answer)

    # Remove the <answer> block from response to get reasoning
    reason = re.sub(r"<answer>.*?</answer>", "", response_plain_text, flags=re.DOTALL).strip()

    return {
        "question": question,
        "answer": final_answer,
        "reason": reason
    }
