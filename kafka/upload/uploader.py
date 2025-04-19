import boto3
import os
import cloudinary
import cloudinary.uploader

class Uploader:
    def __init__(self, service="s3", aws_access_key=None, aws_secret_key=None, bucket_name=None, 
                 cloud_name=None, cloud_api_key=None, cloud_api_secret=None):
        self.service = service
        
        if service == "s3":
            self.s3 = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key
            )
            self.bucket_name = bucket_name
        
        elif service == "cloudinary":
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=cloud_api_key,
                api_secret=cloud_api_secret
            )

    def upload_to_s3(self, file_path):
        if self.service != "s3":
            raise ValueError("Uploader không được cấu hình cho S3")
        
        file_name = os.path.basename(file_path)
        self.s3.upload_file(file_path, self.bucket_name, file_name)
        url = f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
        return url

    def upload_to_cloudinary(self, file_path):
        if self.service != "cloudinary":
            raise ValueError("Uploader không được cấu hình cho Cloudinary")
        
        response = cloudinary.uploader.upload(file_path)
        url = response["secure_url"]
        return url
