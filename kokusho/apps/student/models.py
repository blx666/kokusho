from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Score(models.Model):
    image = models.ImageField(upload_to='student')
    exam_time = models.DateTimeField()
    user = models.ForeignKey(User)
