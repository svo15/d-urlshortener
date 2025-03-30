from django.db import models
from django.contrib.auth.models import User
import random
import string


# Create your models here.
class urls(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    original_url = models.URLField(max_length=500)  # to store the original long URL
    shortened_url = models.CharField(max_length=10, unique=True)  # shortened URL (unique key)

    def __str__(self):
        return f"Shortened URL for {self.original_url}"

    def save(self, *args, **kwargs):
        if not self.shortened_url:
            self.shortened_url = self.generate_shortened_url()
        super().save(*args, **kwargs)

    def generate_shortened_url(self, length=6):
        
        characters = string.ascii_letters + string.digits 
        shortened_url = ''.join(random.choice(characters) for _ in range(length))
        return shortened_url