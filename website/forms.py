from django import forms

from website.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('user', 'state', 'priority', 'date_created', 'date_modified')
