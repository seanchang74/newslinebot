from django.db import models

class users(models.Model):
    uid = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.uid

class comment(models.Model):
    cuid = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=10, null=False)
    email = models.EmailField(null=False)
    comments = models.TextField(null=False)

    def __str__(self):
        return self.cuid    