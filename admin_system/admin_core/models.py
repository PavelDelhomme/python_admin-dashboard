from django.db import models

class ProjectSetting(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.key} : {self.value}"