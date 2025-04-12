import logging
import boto3
from django.conf import settings
from weasyprint import HTML

logger = logging.getLogger(__name__)

# Initialize an S3 client
s3 = boto3.client('s3', region_name=settings.AWS_REGION)

def generate_pdf(html_content, output_path):
    try:
        HTML(string=html_content).write_pdf(output_path)
        logger.info(f"PDF generated successfully at {output_path}")
        return True
    except Exception:
        logger.error("Error generating PDF", exc_info=True)
        return False

def upload_file_to_s3(local_path, bucket_name, key):
    """
    Upload a file to S3 and return its public URL.
    """
    try:
        # Remove ExtraArgs parameter to avoid setting ACL
        s3.upload_file(local_path, bucket_name, key)
        url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
        logger.info(f"Uploaded {local_path} to S3 at {url}")
        return url
    except Exception:
        logger.error("Error uploading to S3", exc_info=True)
        return None


def download_file_from_s3(bucket_name, key, download_path):
    try:
        s3.download_file(bucket_name, key, download_path)
        logger.info(f"Downloaded s3://{bucket_name}/{key} to {download_path}")
        return True
    except Exception:
        logger.error("Error downloading from S3", exc_info=True)
        return False
