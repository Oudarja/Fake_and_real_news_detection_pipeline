# retrive_summarization.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# =========================
# Load model and tokenizer once
# =========================
MODEL_NAME = "data-silence/any-news-sum"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    model.to(device)
    model.eval()
    print("✅ Summarization model loaded successfully")
except Exception as e:
    print("❌ Failed to load summarization model:", e)
    tokenizer = None
    model = None

# =========================
# Generate summary function
# =========================
def generate_summarization(content):
    if tokenizer is None or model is None:
        return "\nN/A\n==========\n"

    try:
        # Tokenize input
        inputs = tokenizer(
            content,
            return_tensors="pt",
            max_length=512,
            truncation=True
        ).to(device)

        # Generate summary
        outputs = model.generate(
            **inputs,
            max_length=512,
            num_return_sequences=1,
            no_repeat_ngram_size=4
        )

        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text

    except Exception as e:
        print(f"Error generating summary: {e}")
        return "\nN/A\n==========\n"
