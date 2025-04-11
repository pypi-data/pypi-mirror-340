from openai import OpenAI
import dashscope


def call_openai_sdk(**args):
    key = args['key']
    base_url = args['url']
    client = OpenAI(
        api_key=key,
        base_url=base_url,
    )
    del args['key']
    del args['url']
    completion = client.chat.completions.create(
        **args
    )
    return completion

def call_dashscope_sdk(**args):
    key = args['key']
    url = args['url']
    model = args['model']
    messages = args['messages']
    temperature = args['temperature']
    response = dashscope.Generation.call(
                model=model,
                messages=messages,
                result_format="message",
                temperature=temperature,
            )
    completion = response['output']['choices'][0]['message']['content']
    del args['key']
    del args['url']

    return completion

