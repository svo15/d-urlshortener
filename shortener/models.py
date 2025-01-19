from django.db import models
import random
import string

# Create your models here.
class short_url (models.Model):
    original=models.URLField(unique=True)
    short=models.TextField(unique=True,blank=True)
    def __str__(self):
        return self.original
    def save(self, *args, **kwargs):
        if not self.short:
            self.short = self.generate_shortened_url()
        super(short_url, self).save(*args, **kwargs)

    def generate_shortened_url(self):
        length = 10
        characters = string.ascii_letters + string.digits
        short = ''.join(random.choices(characters, k=length))
        while short_url.objects.filter(short=short).exists():
            short = ''.join(random.choices(characters, k=length))
        return short