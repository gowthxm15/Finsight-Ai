import os
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(message: str, df) -> str:
    csv_preview = df.head(250).to_csv(index=False)

    prompt = f"""
You are a highly skilled corporate finance expert assistant who has 30 years of expirience and have attended prestigious business schools . Here's a preview of the data:
{csv_preview}

Answer the following user query based on the data above:
{message}
"""

    try:
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {e}"
