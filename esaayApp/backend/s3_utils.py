from dotenv import load_dotenv
import os
import boto3



load_dotenv()
# Upload essay file to S3
# Takes a file and uploads it to your S3 bucket
# Returns the URL where the file can be accessed
# Handles file naming and organization

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)


def upload_file_to_s3(file_content, file_name):
    """Upload a file to S3 and return the URL"""
    try:
        bucket_name = os.getenv('AWS_S3_BUCKET')
        print(f"Uploading to bucket: {bucket_name}, file: {file_name}")
        #print("AWS_ACCESS_KEY_ID:", os.getenv('AWS_ACCESS_KEY_ID'))
        #print("AWS_REGION:", os.getenv('AWS_REGION'))
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_content
        )
        
        # Generate the URL
        file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        print(f"File uploaded successfully: {file_url}")  
        return file_url
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None