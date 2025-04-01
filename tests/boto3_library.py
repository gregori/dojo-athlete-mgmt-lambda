import boto3


class Boto3Library:
    session = None

    def initialize_boto3_session(self, aws_access_key, aws_secret_key, region):
        self.session = boto3.Session(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region,
        )

    def list_s3_buckets(self):
        s3 = self.session.client("s3")
        response = s3.list_buckets()
        return [bucket["Name"] for bucket in response["Buckets"]]
