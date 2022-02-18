from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from api.s3 import utils as s3_utils
from api.database import get_db
from api.config import settings

image_router = APIRouter()


@image_router.post("upload")
def upload_image_of_track_to_s3(file: UploadFile = File(...), db: Session = Depends(get_db)):
    s3_utils.validate_format_image_file(file)
    bucket = settings.s3_bucket
    dir_file_name = f"image/{file.filename}"
    region = settings.aws_region
    msg, url = s3_utils.upload_to_s3(file, bucket, dir_file_name, region)
    return {"code": 200, "message": msg, "url": url}
