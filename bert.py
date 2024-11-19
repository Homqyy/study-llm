from datasets import concatenate_datasets, load_dataset


bookcorpus = load_dataset("bookcorpus", split="train")
wiki = load_dataset("wikimedia/wikipedia", "20231101.en", split="train")

wiki = wiki.remove_columns([col for col in wiki.column_names if col != "text"])

dataset = concatenate_datasets([bookcorpus, wiki])

d = dataset.train_test_split(test_size=0.1)

def dataset_to_text(dataset, output_filename="data.txt"):
    """Utility function to save dataset text to disk,
    useful for using the texts to train the tokenizer
    (as the tokenizer accepts files)"""
    with open(output_filename, "w") as f:
        for t in dataset["text"]:
            print(t, file=f)

# save the training set to train.txt
dataset_to_text(d["train"], "train.txt")
# save the testing set to test.txt
dataset_to_text(d["test"], "test.txt")