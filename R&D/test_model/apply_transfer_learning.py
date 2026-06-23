import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.utils import shuffle
import time
import csv

def apply_TL(new_samples, model, tokenizer, old_data_path="final_dataset.csv",
             batch_size=16, epochs=1, lr=5e-5, device=None):
    """
    Fine-tune the BertForSequenceClassification model safely on new data + old data.
    """
    device = torch.device("cpu")  # Always fine-tune on CPU to not block FastAPI
    model.to(device)
    model.train()

    # ----------------------------
    # 1️⃣ Prepare new + old data
    # ----------------------------
    print(f"🔹 Preparing data: {len(new_samples)} new samples + 5% of old data...")
    new_df = pd.DataFrame(new_samples)
    old_df = pd.read_csv(old_data_path,on_bad_lines='skip')

    old_df = old_df.sample(frac=0.2, random_state=42)  # 10% old data

    train_df = pd.concat([old_df, new_df], ignore_index=True)
    train_df = shuffle(train_df).reset_index(drop=True)

    texts = (train_df['title'] + " " + train_df['description']).tolist()
    labels = train_df['label'].tolist()

    enc = tokenizer(texts, truncation=True, padding=True, max_length=512, return_tensors="pt")
    dataset = TensorDataset(enc['input_ids'], enc['attention_mask'], torch.tensor(labels))
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # ----------------------------
    # 2️⃣ Freeze BERT base layers
    # ----------------------------
    for param in model.bert.parameters():
        param.requires_grad = False

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()

    # ----------------------------
    # 3️⃣ Training loop
    # ----------------------------
    total_batches = len(loader)
    for epoch in range(epochs):
        total_loss = 0
        start_time = time.time()
        for batch_idx, batch in enumerate(loader, 1):
            input_ids, attention_mask, batch_labels = [b.to(device) for b in batch]
            optimizer.zero_grad()
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            loss = loss_fn(logits, batch_labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            print(f"    Batch {batch_idx}/{total_batches}, Batch Loss: {loss.item():.4f}")

        epoch_time = time.time() - start_time
        print(f"✅ Epoch {epoch+1}/{epochs} finished, Avg Loss: {total_loss/total_batches:.4f}, Time: {epoch_time:.2f}s")

    # Save updated model
    model.save_pretrained("fine_tuned_bert_base_multilingual_uncased")
    print("🏁 Fine-tuning complete and model updated.")
