from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    original_image = models.ImageField(upload_to="originals/")
    processed_image = models.ImageField(upload_to="processed/", null=True, blank=True)
    bg_color = models.CharField(max_length=7, default="#FFFFFF")  # format #RRGGBB
    is_transparent = models.BooleanField(default=False)
    status = models.CharField(max_length=16, default="pending", choices=[
        ("pending", "Pending"),
        ("done", "Done"),
        ("error", "Error"),
    ])
    error_message = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Photo {self.pk}"
