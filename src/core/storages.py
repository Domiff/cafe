from fastapi_storages import S3Storage as BaseS3Storage
from src.core.config import settings


class S3Storage(BaseS3Storage):
    AWS_ACCESS_KEY_ID = settings.storage.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.storage.AWS_SECRET_ACCESS_KEY
    AWS_S3_BUCKET_NAME = settings.storage.AWS_S3_BUCKET_NAME
    AWS_S3_ENDPOINT_URL = settings.storage.AWS_S3_ENDPOINT_URL
    AWS_DEFAULT_ACL = settings.storage.AWS_DEFAULT_ACL
    AWS_S3_USE_SSL = settings.storage.AWS_S3_USE_SSL


storage = S3Storage()
