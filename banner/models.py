from django.db import models


class Banner(models.Model):
    banner = models.ImageField(upload_to='banner/', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.banner.name
