import logging
import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import HTTPException, UploadFile, status
from api.config import settings


s3_config = Config(
    region_name='ap-southeast-1',
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

log = logging.getLogger(__name__)


def create_bucket(bucket_name, region="ap-southeast-1"):
    try:
        s3_client = boto3.client('s3', config=s3_config)
        s3_client.create_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def validate_format_image_file(file: UploadFile):
    if not file.filename.lower().endswith(
        (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif", ".flr")
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please upload the correct image format",
        )

    # file = file
    file.file.seek(0, os.SEEK_END)
    file_length = file.file.tell()
    max_size = 3 * 1024 * 1024  # 3mb
    if file_length > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Size of image is too large",
        )


def upload_to_aws(local_file, bucket, s3_file):
    try:
        local_file.seek(0)
        s3 = boto3.client("s3", aws_access_key_id=settings.aws_access_key_id,
                          aws_secret_access_key=settings.aws_secret_access_key)
        s3.upload_fileobj(
            local_file,
            bucket,
            s3_file,
            ExtraArgs={"ContentType": "image/jpeg"}
        )
        log.info("Upload Successful")
        return True, "Upload Successful"
    except FileNotFoundError:
        log.error("The file was not found")
        return False, "The file was not found"
    except NoCredentialsError:
        log.error("Credentials not available")
        return False, "Credentials not available"
    except ClientError as e:
        log.error(e.__dict__)
        return False, e.__dict__


def upload_to_s3(file, bucket, dir_file_name, region="ap-southeast-1"):
    is_uploaded, msg = upload_to_aws(file.file, bucket, dir_file_name)
    if not is_uploaded:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
    url = f"https://{bucket}.s3.{region}.amazonaws.com/{dir_file_name}"
    return msg, url
