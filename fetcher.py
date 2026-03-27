import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from bs4 import BeautifulSoup
import streamlit as st
from datetime import datetime
import os

from summariser import summarize_text
from filter import is_allowed_sender

# ==============================
# CONFIG
# ==============================
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# ==============================
# STREAMLIT UI
# ==============================
st.title("EMAIL INTELLIGENCE")
st.header("Today's Output")

# ==============================
# HELPERS
# ==============================
def decode_mime_words(s: str) -> str:
    """Decode MIME encoded words into readable string."""
    if not s:
        return ""
    decoded = decode_header(s)
    result = ""
    for part, encoding in decoded:
        if isinstance(part, bytes):
            result += part.decode(encoding or "utf-8", errors="ignore")
        else:
            result += part
    return result

def clean_html(body: str) -> str:
    """Convert HTML body to plain text."""
    if "<html" in body.lower():
        soup = BeautifulSoup(body, "html.parser")
        body = soup.get_text(separator=" ")
    return " ".join(body.split())

# ==============================
# CONNECT TO GMAIL
# ==============================
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

# ==============================
# FETCH EMAILS
# ==============================
status, messages = mail.search(None, "ALL")
email_ids = messages[0].split()

# Load last checked timestamp
with open("last_checked.txt", "r") as f:
    last_checked = datetime.strptime(f.read().strip(), "%Y-%m-%d %H:%M:%S")

print("Last checked:", last_checked)

FLAG = True

# Process emails (latest first)
for i in email_ids[::-1]:
    if FLAG == False:
        break

    status, msg_data = mail.fetch(i, "(RFC822)")
    for response_part in msg_data:
        if not isinstance(response_part, tuple):
            continue

        msg = email.message_from_bytes(response_part[1])

        # Extract metadata
        from_ = decode_mime_words(msg.get("From"))
        subject = decode_mime_words(msg.get("Subject"))
        try:
            date_str = msg.get("Date")
            mail_time = parsedate_to_datetime(date_str).replace(tzinfo=None)
        except:
            continue


        # Skip old emails
        if mail_time < last_checked:
            FLAG = False
            break

        # Skip disallowed senders
        if not is_allowed_sender(from_):
            continue

        # ==============================
        # BODY EXTRACTION
        # ==============================
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                try:
                    payload = part.get_payload(decode=True)
                    if not payload:
                        continue
                    text = payload.decode(errors="ignore")

                    if content_type == "text/plain":
                        body = text
                        break
                    elif content_type == "text/html" and not body:
                        body = text  # fallback if no plain text
                except Exception:
                    continue
        else:
            try:
                body = msg.get_payload(decode=True).decode(errors="ignore")
            except Exception:
                body = ""

        # Clean body
        body = clean_html(body)

        # Summarize
        summary = summarize_text(body)

        # ==============================
        # DISPLAY
        # ==============================
        st.divider()
        st.write("FROM:", from_)
        st.write("SUBJECT:", subject)
        st.write("SUMMARY:\n", summary)

# ==============================
# UPDATE LAST CHECKED
# ==============================
with open("last_checked.txt", "w") as f:
    f.write(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

print("Updated last checked:", last_checked)
st.write("Updated last checked:", last_checked)
st.subheader("Emails are summarised. OR there are no more emails to summarise")

# ==============================
# LOGOUT
# ==============================
mail.logout()