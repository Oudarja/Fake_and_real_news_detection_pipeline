import ollama

def unknown_claim_verifier(content,summary):
    try:
        # Call the model
        response = ollama.chat(
        model="llama3.1:8b",
         messages=[
        {
            "role": "system",
            "content": (
                "You are a professional fact-checking AI."
                "You will be given:"
                "1) A news claim (full content)"
                "2) A summary of information collected from Google search results"

                "Your task is to decide whether the news claim is FACTUALLY REAL or FAKE"
                "based ONLY on the provided evidence summary."

                "Decision rules:"
                "- Return \"Real\" if the evidence clearly supports or confirms the claim."
                "- Return \"Fake\" if the evidence contradicts  the claim."
                "- If the evidence is weak, unclear, incomplete, or does not mention the claim directly,"

                "IMPORTANT:"
                "- You MUST return exactly ONE word."
                "- Allowed outputs: Real or Fake"
                "- Do NOT explain your answer."
                "- Do NOT add any extra text."

                "Claim:"
                "<FULL CLAIM OR NEWS CONTENT>"

                "Evidence summary:"
                "<GOOGLE SCRAPED & SUMMARIZED TEXT>"

                "Answer:"
            )
        },
        {
            "role": "user",
            "content": f"Claim: {content}\nEvidence summary: {summary}"
        }
    ]
    )

        result = response["message"]["content"]

        return result

    except Exception as e:
        print(f"Error generating summary: {e}")
        return f"\nN/A\n==========\n"