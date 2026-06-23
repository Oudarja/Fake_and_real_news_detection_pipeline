import re
import torch
import torch.nn.functional as F
from transformers import BertTokenizer, BertModel ,BertForSequenceClassification


tokenizer = BertTokenizer.from_pretrained("fine_tuned_tokenizer_bert_base_multilingual_uncased")
model = BertForSequenceClassification.from_pretrained("fine_tuned_bert_base_multilingual_uncased")

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

model.to(device)

def predict_news(text, tokenizer, model, threshold, unknown_margin=0.2):
    model.eval()

    text = re.sub(r'\s+', ' ', text).strip()

    enc = tokenizer(
        text,
        truncation=True,
        padding=True,
        max_length=512,
        return_tensors="pt"
    )
    enc = {k: v.to(device) for k, v in enc.items()}

    with torch.no_grad():
        outputs = model(**enc)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1)[0]

    real_prob = probs[0].item()
    fake_prob = probs[1].item()

    # UNKNOWN if too close
    if abs(real_prob - fake_prob) <= unknown_margin:
        return {
            "label": "UNKNOWN",
            "probs": {"REAL": real_prob, "FAKE": fake_prob}
        }

    # Threshold-based decision
    if fake_prob >= threshold:
        label = "FAKE"
    elif real_prob >= threshold:
        label = "REAL"
    else:
        return {
            "label": "UNKNOWN",
            "probs": {"REAL": real_prob, "FAKE": fake_prob}
        }


    return {
        "label": label,
        "probs": {"REAL": real_prob, "FAKE": fake_prob}
    }