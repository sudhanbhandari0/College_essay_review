!pip install datasets
!pip install --upgrade transformers --quiet

import pandas as pd
import json
import pandas as pd
import torch
import os
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset

df = pd.read_csv("/college_essays.csv")
print("Shape of data:", df.shape)
print(df.head())
print("Columns:", df.columns.tolist())

df = pd.read_csv("/college_essays.csv")



with open("college_essays.jsonl", "w", encoding="utf-8") as f:
  for i in range(len(df)):
    essay = df.loc[i, 'Essay']
    feedback = df.loc[i, 'Feedback']
    data = {"essay": essay, "feedback": feedback}
    json_line = json.dumps(data)
    f.write(json_line + "\n")

print("JSONL file created: college_essays.jsonl")

with open("college_essays.jsonl", "r", encoding="utf-8") as f:
    for _ in range(5):
        print(f.readline())

print("Files in current directory:", os.listdir('.'))
print("JSONL file exists:", os.path.exists('college_essays.jsonl'))

with open('college_essays.jsonl', 'r') as f:
    for i, line in enumerate(f):
        if i < 3:  # Show first 3 lines
            print(f"Line {i+1}: {line[:100]}...")
        else:
            break



# Manual loading - this works!
data = []
with open("college_essays.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            data.append(json.loads(line.strip()))

# Create dataset
dataset = Dataset.from_list(data)
print(f"✓ Dataset loaded with {len(dataset)} samples")
print(f"✓ Columns: {dataset.column_names}")

#dataset = load_dataset("json", data_files="college_essays.jsonl", split="train")

split_dataset = dataset.train_test_split(test_size=0.2)
train_dataset = split_dataset['train']
val_dataset = split_dataset['test']

model_name = "gpt2"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(model_name)

if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token
    model.resize_token_embeddings(len(tokenizer))

model.config.pad_token_id = tokenizer.pad_token_id

def tokenize_function(examples):
    combined_texts = [
        "Essay:\n" + e + "\n\nFeedback:\n" + f
        for e, f in zip(examples["essay"], examples["feedback"])
    ]
    return tokenizer(combined_texts, truncation=True, max_length=1024, padding="max_length")

tokenized_train = train_dataset.map(tokenize_function, batched=True, remove_columns=["essay", "feedback"], load_from_cache_file=False,)
tokenized_val = val_dataset.map(tokenize_function, batched=True, remove_columns=["essay", "feedback"], load_from_cache_file=False,)

print("Tokenizer vocab size:", len(tokenizer))
print("Model embedding matrix size:", model.get_input_embeddings().weight.shape[0])

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)


training_args = TrainingArguments(
    output_dir="./gpt2_finetuned_essay",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=5,
    learning_rate=5e-6,
    weight_decay=0.1,
    fp16=True,
    save_steps=200,
    logging_steps=50,
    eval_strategy="steps",  # Use eval_strategy instead of evaluation_strategy
    eval_steps=200,
    save_strategy="steps",
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",

)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,  # Add this line
    data_collator=data_collator,
    tokenizer=tokenizer,
)
trainer.train()
trainer.save_model()