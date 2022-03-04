from rest_framework import serializers
from keylog.models import KeyLogStream
class streamSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyLogStream
        fields = '__all__'