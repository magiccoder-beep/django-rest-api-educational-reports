from django.db import models

from app.utils.helper import generateUniqueID

class Message(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    message = models.TextField(blank=True, null=True)
    sender = models.CharField(max_length=50, blank=True, null=True)
    receiver = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generateUniqueID()
        super().save(*args, **kwargs)