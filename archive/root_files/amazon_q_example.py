#!/usr/bin/env python3
"""
Amazon Q Client Example - Trial Key Version
Demonstrates using Amazon Q trial key to generate AWS S3 code
"""

import os
import requests
import json

def main():
    # Get trial key from environment variable or replace with your actual key
    trial_key = os.getenv('AMAZON_Q_TRIAL_KEY', 'DQRW-JDJB')
    
    print(f"Using trial key: {trial_key}")
    print("Attempting to generate S3 code...")
    
    # Amazon Q Developer API endpoint for code generation
    api_url = "https://q.aws.amazon.com/api/v1/generate"
    
    headers = {
        "Authorization": f"Bearer {trial_key}",
        "Content-Type": "application/json"
    }
    
    # Define instruction for code generation
    instruction = "Write a Python function that connects to S3 and lists all buckets"
    
    payload = {
        "model": "claude-sonnet-4",
        "instruction": instruction,
        "max_tokens": 1000
    }
    
    try:
        # Generate code using Amazon Q
        response = requests.post(api_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("Generated Code:")
            print(result.get('code', result.get('response', 'No code returned')))
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    main()