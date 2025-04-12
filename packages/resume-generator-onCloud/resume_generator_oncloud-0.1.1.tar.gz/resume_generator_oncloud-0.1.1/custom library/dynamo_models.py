from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, JSONAttribute, ListAttribute, MapAttribute
from django.conf import settings

class VersionItem(MapAttribute):
    version_number = UnicodeAttribute()
    content = UnicodeAttribute(null=True)
    extra_fields = JSONAttribute(null=True)
    updated_at = UnicodeAttribute(null=True)  # You might store a string timestamp

class ResumeDynamo(Model):
    """
    PynamoDB model representing a resume stored in DynamoDB.
    """
    class Meta:
        table_name = settings.DYNAMO_TABLE_NAME  # e.g., 'ResumeMetadata'
        region = settings.AWS_REGION             # e.g., 'us-east-1'
    resume_id = UnicodeAttribute(hash_key=True, attr_name="ResumeID")
    user_id = UnicodeAttribute(null=True)
    content = UnicodeAttribute(null=True)      # Merged content field
    extra_fields = JSONAttribute(null=True)      # Stores individual fields as JSON
    versions = ListAttribute(of=VersionItem, null=True)
