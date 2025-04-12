from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ('user',)

    def get_rollback_info(self, obj):
        latest_version = obj.versions.order_by('-version_number').first()
        if latest_version:
            return latest_version.content[:50] + "..."
        return "No rollback info available."
