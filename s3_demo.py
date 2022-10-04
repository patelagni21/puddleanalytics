import boto3
import config

def upload_file(file_name, bucket, id):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = id+"_"+file_name
    session = boto3.Session(
      region_name = 'us-west-2', 
      aws_access_key_id=config.__AWS_ACCESS_KEY,  #os.getenv("__AWS__ACCESS_KEY")
      aws_secret_access_key=config.__AWS_SECRET_ACCESS_KEY
    )
    s3_client = session.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)

    return response
    "jairad26 ACCOUNTNAME"

def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    session = boto3.Session(
      region_name = 'us-west-2', 
      aws_access_key_id=config.__AWS_ACCESS_KEY, 
      aws_secret_access_key=config.__AWS_SECRET_ACCESS_KEY)
    s3 = session.resource('s3')
    output = f"{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)

    return output


def list_files(bucket, filter=None):
    """
    Function to list files in a given S3 bucket
    """
    session = boto3.Session(
      region_name = 'us-west-2', 
      aws_access_key_id=config.__AWS_ACCESS_KEY, 
      aws_secret_access_key=config.__AWS_SECRET_ACCESS_KEY
    )
    s3 = session.resource('s3')
    contents = []
    try:
      for obj in s3.Bucket(bucket).objects.filter(Prefix=filter):#(Prefix=None):
        contents.append(obj)
    except Exception as e:
      print(repr(e))
      pass

    return contents