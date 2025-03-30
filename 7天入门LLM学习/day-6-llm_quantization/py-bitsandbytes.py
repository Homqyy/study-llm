from modelscope import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained(
  'qwen/Qwen-1_8B-Chat',
  load_in_8bit=True,
  trust_remote_code=True)

tokenizer = AutoTokenizer.from_pretrained('qwen/Qwen-1_8B-Chat', trust_remote_code=True)

print(model(**tokenizer('how are you?', return_tensors='pt')))