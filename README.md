# Fake Real News Pipeline

An end-to-end fake-news detection pipeline that combines:

- A fine-tuned BERT classifier for direct real/fake prediction
- Google search scraping for uncertain claims
- LLM-based verification for cases that the classifier marks as `UNKNOWN`
- A FastAPI backend and a Streamlit UI for user interaction

The project is geared toward news text in Bangla/English news contexts and uses a curated list of trusted news domains when checking supporting evidence.

## What It Does

1. Accepts a news title or full article text.
2. Runs the text through a fine-tuned BERT classifier.
3. If the model is confident, it returns `REAL` or `FAKE`.
4. If the model is uncertain, it:
   - searches Google for related articles
   - filters results to trusted sources
   - summarizes the evidence
   - asks an Ollama-hosted LLM to decide between `Real` and `Fake`
5. Stores uncertain samples for future retraining.

## Repository Layout

- `main.py` - Google search scraping helper with a trusted-site filter
- `search_google.py` - alternate helper for collecting trusted links
- `searched_link_scrapper.py` - pages and summarizes search results
- `requirements.txt` - Python dependencies
- `R&D/test_model/test.py` - FastAPI app and inference pipeline
- `R&D/test_model/predict_news.py` - BERT inference logic
- `R&D/test_model/unknown_claim_verifier.py` - Ollama-based fallback verifier
- `R&D/test_model/ui.py` - Streamlit frontend
- `R&D/test_model/Frontend/` - static HTML/CSS/JS frontend prototype
- `R&D/model_pipeline.ipynb` - notebook for experimentation and training
- `R&D/Fake_Data_combined.ipynb` - data preparation notebook

## Requirements

The project uses:

- Python 3.10+
- Chrome browser and a matching Selenium-compatible driver
- Ollama running locally for the fallback verifier
- A fine-tuned model and tokenizer folder:
  - `fine_tuned_bert_base_multilingual_uncased`
  - `fine_tuned_tokenizer_bert_base_multilingual_uncased`

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

If you plan to use the Selenium scraper, make sure Chrome is installed and accessible on your machine.

If you plan to use the fallback LLM verifier, make sure Ollama is running and the model is available:

```bash
ollama serve
```

and pull the model if needed:

```bash
ollama pull llama3.1:8b
```

## Running The Backend

The main API lives in `R&D/test_model/test.py` and exposes:

- `POST /response`

Run it with Uvicorn from the `R&D/test_model` directory:

```bash
cd R&D/test_model
uvicorn test:app --host 127.0.0.1 --port 9000 --reload
```

The request body should look like:

```json
{
  "text": "your news text here"
}
```

The response returns:

```json
{
  "label": "REAL",
  "probs": {
    "REAL": 1.0,
    "FAKE": 0.0
  }
}
```

## Running The Streamlit UI

The Streamlit app in `R&D/test_model/ui.py` expects the backend at `http://127.0.0.1:9000/response`.

Start it with:

```bash
cd R&D/test_model
streamlit run ui.py
```

## Google Scraping Utilities

There are helper scripts for gathering Google results and trusted sources:

- `main.py`
- `search_google.py`
- `searched_link_scrapper.py`
- `R&D/test_model/google_search_for_unknown/`

These scripts use Selenium, BeautifulSoup, and trusted-domain filtering to extract and process supporting evidence.

## Model Flow

The inference path in `R&D/test_model/test.py` works like this:

1. Load the tokenizer and BERT classifier.
2. Predict `REAL`, `FAKE`, or `UNKNOWN`.
3. If `UNKNOWN`, scrape related news sources.
4. Summarize the search results.
5. Ask `unknown_claim_verifier()` to produce a final `Real` or `Fake`.
6. Append the sample to `final_dataset.csv` for future retraining.

## Notes

- The repository includes research notebooks and prototype frontend files under `R&D/`.
- Some paths in the code are relative to `R&D/test_model`, so running from that directory is important.
- The scraper may depend on Google page structure, which can change over time.

## License

No license file is currently included in the repository.
