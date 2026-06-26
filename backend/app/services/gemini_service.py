import google.generativeai as genai

from app.core.config import GEMINI_API_KEY

# ==========================
# GEMINI CONFIG
# ==========================

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# ==========================
# GENERATE EMAIL
# ==========================

def generate_email(
    sender_name: str,
    recipient_name: str,
    email_type: str,
    tone: str,
    template: str,
    prompt: str
):

    final_prompt = f"""
Generate a complete professional email.

SENDER INFORMATION:
Sender Name: {sender_name}

RECIPIENT INFORMATION:
Recipient Name: {recipient_name}

EMAIL DETAILS:
Email Type: {email_type}
Tone: {tone}
Template: {template}

USER REQUEST:
{prompt}

IMPORTANT RULES:

1. NEVER use placeholders such as:
   - [Your Name]
   - [Manager Name]
   - [Recipient Name]
   - [Date]
   - [Start Date]
   - [End Date]
   - [Company Name]

2. Use the sender name exactly:
   {sender_name}

3. Use the recipient name exactly:
   {recipient_name}

4. Generate realistic content.

5. Generate realistic dates if needed.

6. Create a professional subject line.

7. Make the email immediately ready to send.

8. The email must contain:

   Subject

   Greeting

   Body

   Closing

9. Sign the email using:
   {sender_name}

10. Return ONLY the email content.
Do not add explanations.
Do not add markdown.
Do not wrap in code blocks.
"""

    try:

        response = model.generate_content(
            final_prompt
        )

        return response.text.strip()

    except Exception as e:

        return (
            f"Gemini Error: {str(e)}"
        )