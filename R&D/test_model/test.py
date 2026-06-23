from fastapi import FastAPI
import threading, queue
import torch
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
from predict_news import predict_news
from schemas import news
from google_search_for_unknown.searched_link_scrapper import scrape_related_text_and_summarize
from unknown_claim_verifier import unknown_claim_verifier
from apply_transfer_learning import apply_TL
import csv
import re
from google_search_for_unknown.retrieve_summarization import generate_summarization
# ============================
# 1️⃣ Load tokenizer & model
# ============================
tokenizer = BertTokenizer.from_pretrained("fine_tuned_tokenizer_bert_base_multilingual_uncased")
model = BertForSequenceClassification.from_pretrained("fine_tuned_bert_base_multilingual_uncased")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()
print("✅ Model ready for inference")

# ============================
# 2️⃣ Globals for background training
# ============================
train_queue = queue.Queue()
model_swap_lock = threading.Lock()  # ONLY for safe swap

# ============================
# 3️⃣ Background trainer
# ============================
def background_trainer():
    global model

    while True:
        new_samples = []
        sample = train_queue.get()
        new_samples.append(sample)

        while not train_queue.empty():
            new_samples.append(train_queue.get())

        print(f"\n🟡 Background training on {len(new_samples)} samples")

        try:
            # CPU copy for safe fine-tuning
            training_model = BertForSequenceClassification.from_pretrained("fine_tuned_bert_base_multilingual_uncased")
            training_model.train()
            
            apply_TL(
                new_samples=new_samples,
                model=training_model,
                tokenizer=tokenizer,
                old_data_path="final_dataset.csv",
                epochs=1,
                lr=5e-5
            )

            training_model.eval()

            # Swap updated model
            with model_swap_lock:
                model = training_model.to(device)

            print("🔁 Model swapped & moved to device")

        except Exception as e:
            print("❌ Background training failed:", e)
        finally:
            for _ in new_samples:
                train_queue.task_done()
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'[\n\r]', ' ', text)        # remove newlines
    text = re.sub(r'["\',]', '', text)         # remove quotes and commas
    text = re.sub(r'\s+', ' ', text).strip()   # collapse multiple spaces
    return text

# ============================
# 4️⃣ Start background thread
# ============================
threading.Thread(target=background_trainer, daemon=True).start()

# ============================
# 5️⃣ FastAPI app
# ============================
app = FastAPI()

@app.post("/response")
async def response(content: news):
    text = content.text

    # Snapshot for inference (non-blocking)
    with model_swap_lock:
        model_snapshot = model

    prediction = predict_news(
        text,
        tokenizer,
        model_snapshot,
        threshold=0.9
    )

    # return prediction

    if prediction["label"] != "UNKNOWN":
        return prediction

    # # UNKNOWN handling
    summary = scrape_related_text_and_summarize(text)

    # Summary from Google search results can be noisy, so 
    # we clean it before passing to the verifier
    cleaned_summary=clean_text(summary)
    # We also clean the original text to ensure the verifier gets 
    # a consistent format
    cleaned_summarized_text=clean_text(text)

    opinion = unknown_claim_verifier(cleaned_summarized_text, cleaned_summary)
    opinion=opinion.lower()
    lines = cleaned_summarized_text.splitlines()
    title = lines[0] if lines else "N/A"
    description = " ".join(lines[1:]) if len(lines) > 1 else title
    label = 0 if opinion == "real" else 1

   # Clean the row fields
    row = {
        "title": title,
        "description": description,
        "label": label 
    }

    # Add to training queue
    train_queue.put(row)

    # Append safely to CSV
    pd.DataFrame([row]).to_csv(
        "final_dataset.csv",
        mode="a",
        header=not pd.io.common.file_exists("final_dataset.csv"),
        index=False,
        quoting=1
    )

    if opinion=="real":
        return  {
        "label": "REAL",
        "probs": {"REAL": 1.0, "FAKE": 0}
        }
    else:
        return  {
        "label": "FAKE",
        "probs": {"REAL": 0, "FAKE": 1.0}
        }
