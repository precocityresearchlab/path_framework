#!/usr/bin/env python3
"""
AWS Bedrock API - Amazon Q Alternative
Use Bedrock's Claude models programmatically
"""

import boto3
import json

def bedrock_code_generation(instruction: str):
    """Use AWS Bedrock Claude model like Amazon Q"""
    try:
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        prompt = f"""Human: {instruction}

Please provide a complete Python function that accomplishes this task.

Assistant:"""
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
        
        response = bedrock.invoke_model(
            body=body,
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            accept="application/json",
            contentType="application/json"
        )
        
        result = json.loads(response.get('body').read())
        return result['content'][0]['text']
        
    except Exception as e:
        return f"Error: {e}"

def main():
    """Test Bedrock code generation"""
    instruction = "Write a Python function that connects to S3 and lists all buckets"
    
    print("Bedrock Code Generation Test")
    print("=" * 30)
    print(f"Instruction: {instruction}")
    print("\nGenerated Code:")
    
    code = bedrock_code_generation(instruction)
    print(code)

if __name__ == "__main__":
    main()