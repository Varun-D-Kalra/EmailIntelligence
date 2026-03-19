# 📧 Email Summariser

An intelligent email processing system that fetches, cleans, summarizes, and extracts actionable insights from emails.

---

## 🚀 Features

### 1. Email Fetching
- Connects to email inbox using IMAP (Gmail supported)
- Extracts:
  - Subject
  - Sender
  - Body
  - Timestamp

---

### 2. Preprocessing Engine
- Removes HTML tags
- Cleans signatures and unnecessary text
- Normalizes email content for analysis

---

### 3. Summarisation Engine
- Extractive summarisation (initial phase)
- Converts long emails into concise summaries
- Upgrade path: LLM-based summarisation

---

### 4. Priority Classification
Classifies emails into:
- 🔴 Urgent
- 🟠 Important
- 🟡 Normal
- ⚪ Low Priority

Approach:
- Rule-based (keywords)
- Upgrade: Machine Learning model

---

### 5. Action Item Extraction
Extracts actionable tasks from emails.

Example:
> "Please submit the report by Monday"

Output:
- Task: Submit report  
- Deadline: Monday  

---

### 6. Dashboard (UI)
Built with Streamlit:
- Displays summaries
- Shows priority labels
- Highlights action items

---

### 7. Search & Filters
- Filter emails by:
  - Sender
  - Priority
  - Date
- Search specific emails

---

## 🏗️ Project Structure
