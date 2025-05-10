# 🔍 DebugDeck - A Helpdesk Utility for Log Analysis

DebugDeck is a log analysis utility that demonstrates how to simulate error-prone logs using an AWS Lambda function, fetch those logs from CloudWatch, and use Amazon Bedrock (Titan Text model) to generate meaningful summaries and error insights. The logs and AI-generated explanations are displayed in a user-friendly Streamlit UI.

---

## 🧠 What This Project Does

- Creates a Lambda function (`ErrorGeneratingLambda`) that logs both successful and failed operations.
- Stores these logs in **CloudWatch Logs**.
- A separate application (`logAnalysisOnBedrock.py`) fetches these logs.
- Uses **Amazon Bedrock (Titan Text)** to analyze and summarize error logs based on user queries.
- Displays everything through a **Streamlit-based UI**.

---

## 🧾 Prerequisites

Make sure the following are set up before you begin:

- ✅ An AWS Account
- ✅ AWS CLI configured with credentials and access to:
  - Lambda
  - CloudWatch Logs
  - Bedrock (Titan Text)
- ✅ Python 3.8 or higher
- ✅ Git
- ✅ Streamlit installed (instructions below)

---

## 🚀 Step 1: Clone This Repository

```bash
git clone https://github.com/<your-username>/debugdeck-log-analysis.git
cd debugdeck-log-analysis
