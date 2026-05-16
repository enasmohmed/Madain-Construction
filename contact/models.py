from django.db import models

# Create your models here.


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.email}"


