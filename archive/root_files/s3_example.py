#!/usr/bin/env python3
"""
S3 Bucket Listing Example
Generated code for connecting to S3 and listing all buckets
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

def list_s3_buckets():
    """
    Connect to AWS S3 and list all buckets
    
    Returns:
        list: List of bucket names or None if error
    """
    try:
        # Create S3 client
        s3_client = boto3.client('s3')
        
        # List all buckets
        response = s3_client.list_buckets()
        
        # Extract bucket names
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        
        print(f"Found {len(buckets)} S3 buckets:")
        for bucket in buckets:
            print(f"  - {bucket}")
            
        return buckets
        
    except NoCredentialsError:
        print("Error: AWS credentials not found")
        print("Configure with: aws configure")
        return None
        
    except ClientError as e:
        print(f"AWS Error: {e}")
        return None
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def main():
    """Main function to demonstrate S3 bucket listing"""
    print("S3 Bucket Listing Example")
    print("=" * 30)
    
    buckets = list_s3_buckets()
    
    if buckets:
        print(f"\nSuccessfully retrieved {len(buckets)} buckets")
    else:
        print("\nFailed to retrieve buckets")

if __name__ == "__main__":
    main()