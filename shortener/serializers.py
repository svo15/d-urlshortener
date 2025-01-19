from rest_framework import serializers
from .models import short_url

class urlserializer(serializers.ModelSerializer):
    class Meta:
        model=short_url
        fields = ['original', 'short']