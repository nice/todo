import datetime
from django.contrib.auth.models import User

from django.db import models

class Task(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=300)
    description = models.TextField()
    priority = models.IntegerField()
    state = models.CharField(max_length=50)
    due_date = models.DateField(default=datetime.date.today)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
