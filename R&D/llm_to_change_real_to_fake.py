import ollama
import pandas as pd
import os

CSV_FILE = "web_news_selected_.csv"

def generate_fake_news(title, content):
    """
    Generate a fake news article (title + description) based on the provided content using LLaMA 3.2 via Ollama.
    Saves both to a CSV file for fake news training purposes.
    """
    try:
        # Call the model with updated prompt for both title and description
        response = ollama.chat(
       model="llama3.1:8b",
       messages=[
        {
            "role": "system",
    "content": (
        "You are an AI system designed to generate fake news strictly for academic research "
        "and fake-news-detection dataset creation.\n\n"

        "The input news may be written in English, Bengali, or any other language.\n\n"

        "You will be given a REAL news title and a REAL news description.\n"
        "Your task is to CREATE FAKE NEWS ON THE SAME CONTEXT AND EVENT by:\n"
        "1️⃣ Generating a misleading fake news headline (one sentence) about the SAME topic.\n"
        "2️⃣ Writing a fake news description (4–10 sentences) that stays within the SAME context\n"
        "   but alters, exaggerates, fabricates, or twists key facts.\n\n"

        "Important rules:\n"
        "- The topic, place, and event MUST remain the same\n"
        "- The facts, causes, actions, or outcomes MUST be distorted or fabricated\n"
        "- The fake headline MUST NOT be identical or a close paraphrase of the real headline\n"
        "- Do NOT introduce unrelated events or random scenarios\n"
        "- The fake news must sound realistic and news-like\n"
        "- Do NOT include disclaimers, warnings, or explanations\n"
        "- Do NOT mention that the news is fake or AI-generated\n\n"

        "Return ONLY the following format:\n"
        "Fake title: <generated fake title>\n"
        "Fake description: <generated fake description>"
    ),

        },
        {
            "role": "user",
            "content": f"Real news title: {title}\nDescription: {content}"
        }
    ]
)

        # Extract fake title and description from model output
        fake_news_text = response["message"]["content"]

        # Split lines to get title and description
        fake_title = ""
        fake_description = ""
        for line in fake_news_text.splitlines():
            if line.lower().startswith("fake title:"):
                fake_title = line.split(":", 1)[1].strip()
            elif line.lower().startswith("fake description:"):
                fake_description = line.split(":", 1)[1].strip()
        
        if fake_title == "N/A" or fake_description == "N/A" or fake_title is None or fake_description is None or fake_title.strip() == "" or fake_description.strip() == "":
            # print("Failed to extract fake title or description from model output.")
            return "N/A", "N/A"

        # Save to CSV
        row = {"title": fake_title, "description": fake_description, "label": 1}  # label 1 = fake
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
            # print(f"Current number of entries in CSV: {len(df)}")
        else:
            df = pd.DataFrame([row])

        df.to_csv(CSV_FILE, index=False, encoding="utf-8")

        print(f"Current number of entries in CSV: {len(df)}")
        # Also save to text file (optional)
        with open("fake_output.txt", "a", encoding="utf-8") as f:
            f.write(f"{fake_title}\n{fake_description}\n")

        # print(f"Fake news saved: {fake_title}\n{fake_description}\n")
        return fake_title,fake_description

    except Exception as e:
        print(f"Error generating fake news: {e}")
        return "N/A", "N/A"
