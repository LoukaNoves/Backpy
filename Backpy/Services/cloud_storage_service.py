import boto3

def init_s3(aws_access_key, aws_secret_key, bucket_name):
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    return s3

def upload_to_s3(s3, bucket_name, file_path, key):
    try:
        s3.upload_file(file_path, bucket_name, key)
        print(f"File {file_path} uploaded to {bucket_name}/{key}")
    except Exception as e:
        print(f"Error uploading to S3:{e}")


