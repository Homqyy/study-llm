'''
load dataset
'''
from modelscope import MsDataset
from datasets import Dataset
import os


project_dir = os.path.join(os.path.dirname(__file__), '..')
os.chdir(project_dir)  # Change the current working directory to project_dir
print("Current Working Directory:", os.getcwd())  # Print the current working directory

files = [
    f'{project_dir}/datasets/computer_programming_code/chinese/low/rank_00163.parquet',
    f'{project_dir}/datasets/computer_programming_code/english/low/rank_01598.parquet',
    f'{project_dir}/datasets/computer_programming_code/english/low/rank_01599.parquet',
    f'{project_dir}/datasets/computer_programming_code/english/low/rank_01600.parquet',
    f'{project_dir}/datasets/computer_programming_code/english/low/rank_01601.parquet',
    f'{project_dir}/datasets/computer_programming_code/english/low/rank_01602.parquet',
]

ds = MsDataset.load(dataset_name='parquet', data_files=files)

hf_ds: Dataset = ds.to_hf_dataset()
print('hf_ds:', hf_ds)

# only leave 'text' column
hf_ds = hf_ds.remove_columns([col for col in hf_ds.column_names if col != 'text'])

d = hf_ds.train_test_split(test_size=0.1)
print('train and test dataset:', d)

hf_ds = None # free memory

'''
training tokenizer: set params for training
'''

special_tokens = [
    "[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]", "<S>", "<T>"
]
# training the tokenizer on the training set
files = [f"{project_dir}/datasets/for_train/ds-train.txt"]
# 30,522 vocab is BERT's default vocab size, feel free to tweak
vocab_size = 30_522
# maximum sequence length, lowering will result to faster training (when increasing batch size)
max_length = 512
# whether to truncate
truncate_longer_samples = False
model_path = f"{project_dir}/models/pretrained-bert"

print('set params for training tokenizer')

'''
preprocessing datasets
'''
from transformers import BertTokenizerFast

def encode_with_truncation(examples):
    """Mapping function to tokenize the sentences passed with truncation"""
    return tokenizer(examples["text"], truncation=True, padding="max_length",
            max_length=max_length, return_special_tokens_mask=True)

def encode_without_truncation(examples):
    """Mapping function to tokenize the sentences passed without truncation"""
    return tokenizer(examples["text"], return_special_tokens_mask=True)

# when the tokenizer is trained and configured, load it as BertTokenizerFast
tokenizer = BertTokenizerFast.from_pretrained(model_path)
print('load model from', model_path)

# the encode function will depend on the truncate_longer_samples variable
encode = encode_with_truncation if truncate_longer_samples else encode_without_truncation
# tokenizing the train dataset
train_dataset = d["train"].map(encode, batched=True)
# tokenizing the testing dataset
test_dataset = d["test"].map(encode, batched=True)
if truncate_longer_samples:
    # remove other columns and set input_ids and attention_mask as PyTorch tensors
    train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask"])
    test_dataset.set_format(type="torch", columns=["input_ids", "attention_mask"])
else:
    # remove other columns, and remain them as Python lists
    test_dataset.set_format(columns=["input_ids", "attention_mask", "special_tokens_mask"])
    train_dataset.set_format(columns=["input_ids", "attention_mask", "special_tokens_mask"])
print('done of preprocessing datasets')
d = None # free memory

# group texts
from itertools import chain

def group_texts(examples):
    print("keys:", examples.keys())
    # Concatenate all texts.
    concatenated_examples = {k: list(chain(*examples[k])) for k in examples.keys()}
    # Compute length of concatenated texts.
    total_length = len(concatenated_examples[list(examples.keys())[0]])
    # We drop the last samples to ensure they can be batched perfectly.
    if total_length >= max_length:
        total_length = (total_length // max_length) * max_length
    result = {
        k: [t[i : i + max_length] for i in range(0, total_length, max_length)]
        for k, t in concatenated_examples.items()
    }
    return result

if not truncate_longer_samples:
    print('begin to grouping texts')
    train_dataset = train_dataset.map(group_texts, batched=True, desc=f"Grouping texts in chunks of {max_length}")
    test_dataset = test_dataset.map(group_texts, batched=True, desc=f"Grouping texts in chunks of {max_length}")

    # convert to torch tensors
    train_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask'])
    test_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask'])

print('done of preprocessing')

'''
training model
'''
from transformers import BertConfig, BertForMaskedLM, DataCollatorForLanguageModeling, Trainer, TrainingArguments

model_config = BertConfig(vocab_size=vocab_size, max_position_embeddings=max_length)
model = BertForMaskedLM(config=model_config)

# init data collator: randomly masks 20% of the token
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=True,
    mlm_probability=0.2
)

training_args = TrainingArguments(
    output_dir=f'{project_dir}/models/results',
    evaluation_strategy="steps",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=10,
    gradient_accumulation_steps=8,
    per_device_eval_batch_size=64,
    logging_steps=1000,
    save_steps=1000,
    # load_best_model_at_end=True,
    # save_total_limit=3,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

trainer.train()