import os

from botocore.exceptions import ClientError
from aws_service import getS3Client, getS3Resource
from utils import handleError

class S3: 
    def __init__(self, user):
        self.s3_resource = getS3Resource(user)
        self.s3_client = getS3Client(user)

    def bucketDetails(self):
        bucket = self.selectBucket()

        if not bucket:
            return

        objects = self.s3_client.list_objects_v2(Bucket=bucket)

        print('-'*60)

        if objects['KeyCount'] == 0:
            print('Any files in the bucket found')
            return

        for obj in objects['Contents']:
            print(obj['Key'])
        
        print('-'*60)

        return bucket

    def getAllBuckets(self):
        buckets = self.s3_client.list_buckets()['Buckets']

        if len(buckets) == 0:
            print('Any buckets found')
            return
        
        for bucket in self.s3_resource.buckets.all():
            print('\t |', bucket.name)
    
    def selectBucket(self):
        print(f'S3 Buckets')
        self.getAllBuckets()
        print('-'*60)
        bucket = input("Provide a bucket name: ")
        return bucket

    def upload_file(self):
        print(f'Upload a file to an S3 bucket')
        
        bucket = self.selectBucket()

        if not bucket:
            return

        file_name = input("Provide a file name: ")
        object_name = input("Provide a obj name: ")

        if not file_name:
            return

        if object_name is None:
            object_name = os.path.basename(file_name)

        try:
            self.s3_client.upload_file(file_name, bucket, object_name)
            print(f'File uploaded successfully')
        except ClientError:
            print(f'An error happens')
            
    def download_file(self):
        print(f'Download a file from a S3 bucket')
        
        bucket = self.bucketDetails()
        object = input("Provide an objects name: ")
        name = input("Provide a name to store the file: ")

        if not bucket:
            return
            
        if not object:
            return

        if not name:
            return

        try:
            self.s3_client.download_file(bucket, object, name)
            print(f'File downloaded successfully')
        except Exception as error:
            handleError(error)

    def delete_file(self):
        print(f'Delete a file  from a S3 bucket')

        bucket = self.bucketDetails()
        object = input("Provide an objects name: ")

        if not object:
            return

        if not bucket:
            return

        try:
            self.s3_client.delete_object(Bucket=bucket, Key=object)
            print(f'File deleted successfully')
        except Exception as error:
            handleError(error)

    def delete_bucket(self):
        print(f'Delete a S3 bucket')

        self.getAllBuckets()
            
        bucketName = input("Provide a bucket name: ")

        if not bucketName:
            return
        
        s3_bucket = self.s3_resource.Bucket(bucketName)
        objects = self.s3_client.list_objects_v2(Bucket=bucketName)

        try:
            if len(objects) > 0:
                if input("The bucket have items, are you sure? (yes/no) ") != "yes":
                    print(f'Aborting')
                    return

                s3_bucket.objects.all().delete()

            s3_bucket.delete()
            
            print(f'Bucket deleted successfully')
        except Exception as error:
            handleError(error)
