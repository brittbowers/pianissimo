import boto3

bucketname = 'britt-bow-bucket' # replace with your bucket name
filename = 'time_notes.json' # replace with your object key
s3 = boto3.resource('s3')
s3.Bucket(bucketname).download_file(filename, 'data/time_notes.json')