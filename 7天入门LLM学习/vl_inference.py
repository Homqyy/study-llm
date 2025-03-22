#Qwen-VL 是阿里云研发的大规模视觉语言模型（Large Vision Language Model, LVLM）。Qwen-VL 可以以图像、文本、检测框作为输入，并以文本和检测框作为输出。Qwen-VL 系列模型性能强大，具备多语言对话、多图交错对话等能力，并支持中文开放域定位和细粒度图像识别与理解。
from modelscope import (
    snapshot_download, AutoModelForCausalLM, AutoTokenizer, GenerationConfig
)
from auto_gptq import AutoGPTQForCausalLM

model_dir = snapshot_download("qwen/Qwen-VL-Chat-Int4", revision='v1.0.0')

import torch
torch.manual_seed(1234)

# Note: The default behavior now has injection attack prevention off.
tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=model_dir, trust_remote_code=True)

# use cuda device
model = AutoModelForCausalLM.from_pretrained(
    pretrained_model_name_or_path=model_dir, 
    device_map="cuda", 
    trust_remote_code=True,
    use_safetensors=True).eval()

# 1st dialogue turn
query = tokenizer.from_list_format([
    {'image': 'https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg'},
    {'text': '这是什么'},
])
response, history = model.chat(tokenizer, query=query, history=None)
print(response)
# 图中是一名年轻女子在沙滩上和她的狗玩耍，狗的品种可能是拉布拉多。她们坐在沙滩上，狗的前腿抬起来，似乎在和人类击掌。两人之间充满了信任和爱。

# 2nd dialogue turn
response, history = model.chat(tokenizer, '输出"狗"的检测框', history=history)
print(response)

image = tokenizer.draw_bbox_on_latest_picture(response, history)
if image:
  image.save('al_test.jpg')
else:
  print("no box")