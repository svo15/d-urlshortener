from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import urls



class userSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['id','username','password']
    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return user


   
class urlsSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    shortened_url=serializers.CharField(read_only=True)

    class Meta:
        model = urls
        fields = ['original_url', 'shortened_url', 'user']

    def create(self, validated_data):
        user = self.context['request'].user  
        validated_data['user'] = user
        shortened_url_instance = urls.objects.create(**validated_data)
        return shortened_url_instance
    

    