from django import forms

from website.models import Task

priorities =(
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)
class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('user', 'state', 'priority', 'date_created', 'date_modified')
