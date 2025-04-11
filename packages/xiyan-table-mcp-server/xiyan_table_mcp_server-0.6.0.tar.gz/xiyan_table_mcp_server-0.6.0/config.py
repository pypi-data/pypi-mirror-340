import os

# 默认配置
DEFAULT_CSV_PATH = os.path.join(os.path.dirname(__file__), "data.csv")
DEFAULT_MODEL_NAME = "pre-table"
DEFAULT_MODEL_API_KEY = "your-api-key"

# 用户配置（可以通过环境变量覆盖）
CSV_PATH = os.getenv("XIYAN_CSV_PATH", DEFAULT_CSV_PATH)
MODEL_NAME = os.getenv("XIYAN_MODEL_NAME", DEFAULT_MODEL_NAME)
MODEL_API_KEY = os.getenv("XIYAN_MODEL_API_KEY", DEFAULT_MODEL_API_KEY)

# LLM 配置
LLM_CONFIG = {
    "temperature": 0.01,
    "max_length": 1024,
    "top_k": 1,
}

# 提示词模板
PROMPT_TEMPLATE = """
You are a table analyst. Your task is to answer questions based on the table content.

The answer should follow the format below:
<answer>AnswerString</answer>

Ensure the final answer format is the last output line and can only be in the "<answer>AnswerString</answer>" form, no other form.

Let's think step by step and then give the final answer to the question.

Read the table below:
[TABLE]
{table}

Let's get start!
Question: {question}
""" 