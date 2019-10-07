from django.db import models
from django.urls import reverse

class Post(models.Model):
    content = models.TextField()

    def get_absolute_url(self):
        return reverse('myapp:post_detail', args=[self.id])


# Create your models here.
class Content(models.Model):
    string = models.TextField()

    def __str__(self):
        return self.string
