from groq import Groq
import os
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def summarize_text(text):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an elite email intelligence system designed for high-performance users.\n\n"

                        "Your job is NOT just to summarize, but to EXTRACT VALUE.\n\n"

                        "Follow these rules strictly:\n"
                        "- Focus on ideas, insights, and useful information.\n"
                        "- Explain WHAT is happening and WHY it matters.\n"
                        "- Remove fluff, greetings, and noise.\n"
                        "- Separate promotional content clearly.\n"
                        "- Do NOT copy text. Rephrase intelligently.\n\n"

                        "Output format:\n\n"

                        "1. Core Summary (3-5 bullets)\n"
                        "- Each bullet should explain the idea with context (not just headlines)\n\n"

                        "2. Key Insight (2-3 lines)\n"
                        "- What is the deeper takeaway?\n"
                        "- Why should someone care?\n\n"

                        "3. Promotion\n"
                        "- Clearly describe what is being sold or promoted (or 'None')\n\n"

                        "4. Category\n"
                        "- Choose from: AI / Business / Health / Coding / General\n\n"

                        "Write like a sharp analyst, not a newsletter."
                    )
                },
                {
                    "role": "user",
                    "content": f"Analyze this email and extract real value:\n\n{text[:1200]}"
                }
            ]
        )

        return response.choices[0].message.content


    except Exception as e:
        return f"ERROR: {str(e)}"