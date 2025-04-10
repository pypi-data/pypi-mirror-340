USER_PROMPT = """
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