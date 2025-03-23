from pydantic_settings import BaseSettings


class AppConfiguration(BaseSettings):
    app_name: str
    app_version: str
    s3_bucket: str
    s3_path: str
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str

    @property
    def s3_file_path(self) -> str:
        return f"s3://{self.s3_bucket}/{self.s3_path}"

    class Config:
        env_file = ".env"
