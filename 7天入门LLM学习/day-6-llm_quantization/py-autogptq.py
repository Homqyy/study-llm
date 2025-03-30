# 例子来自于https://github.com/PanQiWei/AutoGPTQ
from modelscope import AutoTokenizer, snapshot_download
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
import logging
import shutil
import os

logging.basicConfig(
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S"
)

pretrained_model_dir = snapshot_download("qwen/Qwen-1_8B-Chat")
quantized_model_dir = "qwen-1_8B-4bit"

shutil.rmtree(quantized_model_dir, ignore_errors=True)
shutil.copytree(pretrained_model_dir, quantized_model_dir)
for _file in os.listdir(quantized_model_dir):
    if ".safetensors" in _file or ".bin" in _file:
        os.remove(os.path.join(quantized_model_dir, _file))

tokenizer = AutoTokenizer.from_pretrained(pretrained_model_dir, use_fast=True, trust_remote_code=True)
examples = [
    tokenizer(
        "auto-gptq is an easy-to-use model quantization library with user-friendly apis, based on GPTQ algorithm."
    )
]

quantize_config = BaseQuantizeConfig(
    bits=4,  # quantize model to 4-bit
    group_size=128,  # it is recommended to set the value to 128
    desc_act=False,  # set to False can significantly speed up inference but the perplexity may slightly bad
)

# load un-quantized model, by default, the model will always be loaded into CPU memory
model = AutoGPTQForCausalLM.from_pretrained(pretrained_model_dir, quantize_config, trust_remote_code=True).to(0)

# quantize model, the examples should be list of dict whose keys can only be "input_ids" and "attention_mask"
model.quantize(examples)

# save quantized model
model.save_quantized(quantized_model_dir)

# save quantized model using safetensors
model.save_quantized(quantized_model_dir, use_safetensors=True)

# load quantized model to the first GPU
model = AutoGPTQForCausalLM.from_quantized(quantized_model_dir, device="cuda:0", trust_remote_code=True)
# inference with model.generate
print(tokenizer.decode(model.generate(**tokenizer("auto_gptq is", return_tensors="pt").to(model.device))[0]))