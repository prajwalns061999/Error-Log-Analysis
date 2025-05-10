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
git clone https://github.com/prajwalns061999/Error-Log-Analysis.git
cd Error-Log-Analysis
```

## 📂 Step 2: Create the Lambda Function on AWS

1. Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda).
2. Click **Create function**.
3. Set:
   - **Function name**: `ErrorGeneratingLambda`
   - **Runtime**: `Python 3.8+`
   - **Permissions**: Choose or create a role with permissions to write to CloudWatch Logs.
4. After creation, go to the **Code** section and **replace** it with the following:

    ```python
    import json

    def lambda_handler(event, context):
        for i in range(20):
            try:
                if i < 10:
                    result = 10 / 2
                    print(f"Success: Operation {i} completed. Result: {result}")
                else:
                    result = 10 / 0
                    print(f"Success: Operation {i} completed. Result: {result}")
            except Exception as e:
                print(f"Error occurred at operation {i}: {str(e)}")

        return {
            'statusCode': 200,
            'body': json.dumps('Lambda function completed with both success and errors')
        }
    ```

5. Click **Deploy**.
6. Click **Test** and configure a dummy test event (e.g., `{"key": "value"}`).
7. Run the function once or twice to populate logs in CloudWatch.

---

## ☁️ Step 3: Verify Logs in CloudWatch

1. Navigate to **CloudWatch > Logs > Log groups**.
2. Locate the group `/aws/lambda/ErrorGeneratingLambda`.
3. Make sure logs are visible for your recent executions.

---

## 🧑‍💻 Step 4: Set Up the Local Environment

### 1. Create a Python Virtual Environment (Optional but recommended)

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### 2. Install Required Dependencies
If you have a **requirements.txt** file:
```bash
pip install -r requirements.txt
```
Otherwise, manually install:
```bash
pip install boto3 streamlit numpy faiss-cpu openai
```

### 🔐 Step 5: Configure AWS Credentials
Make sure your terminal has access to your AWS credentials:
```bash
aws configure
```
Input your:
 - AWS Access Key ID
 - AWS Secret Access Key
 - Region (e.g., us-east-1)

Note: Your IAM user must have permissions for CloudWatch, Lambda, and Bedrock.

### 🧪 Step 6: Run the Streamlit Application
Create a new file logAnalysisOnBedrock.py in the project directory and the copy the given code.
In the project directory:
```bash
streamlit run logAnalysisOnBedrock.py
```

###  What You'll See
The app will open in your browser with:
 - A dropdown menu to select an application name.
 - An input box to ask a question (e.g., “What caused the errors in the latest execution?”).
 - A detailed AI-generated explanation of the Lambda error logs.

### 🛠️ How It Works
1. lambda_function.py generates logs, simulating both success and failure.
2. logAnalysisOnBedrock.py:
   - Fetches logs from /aws/lambda/ErrorGeneratingLambda using Boto3.
   - Sends those logs along with your query to Amazon Bedrock’s Titan Text model.
   - Parses the AI-generated response and displays it via Streamlit.

### 🔧 Configuration
You can customize:
   - Log Group Name: Edit log_group_name in logAnalysisOnBedrock.py
   - Applications List: Modify APPLICATION_NAMES list
   - Bedrock Model: Uses amazon.titan-text-premier-v1:0

### Folder Structure
```bash
Error-Log-Analysis/
│
├── lambda_function.py            # Lambda logic that generates logs
├── logAnalysisOnBedrock.py       # Log analyzer and Streamlit UI
├── requirements.txt              # Python dependencies (optional)
├── README.md                     # Project instructions
```
