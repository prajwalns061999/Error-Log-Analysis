import boto3
import json
import time
# from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import streamlit as st
import openai
import os
from botocore.exceptions import ClientError

# Set OpenAI API key
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

APPLICATION_NAMES = [
    "ValuationFlow", "Diligence360", "LoanSight", "AssureDocs", "RiskNest"
]


def fetch_cloudwatch_logs(log_group_name, application_name, start_time, end_time):
    
    # Filter pattern to match application name in the log messages
    filter_pattern = f'"{application_name}"'

    
    client = boto3.client('logs')
    response = client.filter_log_events(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        # filterPattern=filter_pattern
    )
    return response['events']


def generate_error_summary(log_messages, query):
    """
    Use AWS Bedrock's Titan Text Express v1 model to generate a summary of errors based on user query.
    """
    log_messages = "\n".join([log['message'] for log in logs])
    model_id = "amazon.titan-text-premier-v1:0"
    # Prompt the model to summarize the error message in plain English
    prompt = f"""User's query: '{query}'. The error logs are as follows:{log_messages} 
        You are a log analyzer and you will analyze the logs in detail." 
        Describe step by step what caused the errors, including any specific code lines, functions, or operations that led to the error.
        Provide possible solutions to fix the errors, and explain why these solutions would work. Exclude irrelevant details like request IDs, runtime versions, etc.
        Example: Generate a sample code that can be used to fix the error.
    """
    native_request = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 1500,
            "temperature": 0,
        },
    }
       
    request = json.dumps(native_request)
    try:
        # Invoke the model with the request.
        response = bedrock_client.invoke_model(modelId=model_id, body=request)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

    # Decode the response body.
    model_response = json.loads(response["body"].read())
    
    # Extract and print the response text.
    response_text = model_response["results"][0]["outputText"]
    return response_text

# answer = generate_error_summary("Summarize the logs", logs)
# Streamlit UI
st.title('DebugDeck - A Helpdesk Utility')

application_name = st.selectbox("Select Application Name", APPLICATION_NAMES)

# User input query
query = st.text_input("Ask a question about...")

log_group_name = '/aws/lambda/ErrorGeneratingLambda'  

# logs = fetch_cloudwatch_logs(log_group_name)
end_time = int(time.time() * 1000)  # Current time in milliseconds
start_time = end_time - 8640000

if application_name and query:
    # Fetch logs for the selected application
    logs = fetch_cloudwatch_logs(log_group_name, application_name, start_time, end_time)
    
    # If logs are found, summarize them using the AI model
    if logs:
        answer = generate_error_summary(logs, query)
        # Display the user query and AI response
        st.write(f"**User Query:** {query}")
        st.write(f"**AI Response:** {answer}")
    else:
        st.write(f"No logs found for {application_name}")


