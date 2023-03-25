from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Topic

class TopicForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Topic
        fields = ['title', 'content', 'role']
