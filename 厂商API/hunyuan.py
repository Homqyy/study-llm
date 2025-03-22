import os
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

HUNYUAN_API_KEY = os.environ.get("HUNYUAN_API_KEY", "sk-iLAc28cobdM7S3XAZ5JIJPSTXvGd0o4d6sB2WTO5uz5IDB68")

client = OpenAI(
    api_key = HUNYUAN_API_KEY,
    base_url ="https://api.hunyuan.cloud.tencent.com/v1"
)

completion: ChatCompletion = client.chat.completions.create(
    model = "hunyuan-turbo",
    messages = [
        {
            "role": "user",
            "content": "你好",
        },
    ],
    extra_body = {
        "enable_enhancement": True,
        "enable_deep_search": False,
    },
)

for message in completion.choices:
    print(message.message.content)