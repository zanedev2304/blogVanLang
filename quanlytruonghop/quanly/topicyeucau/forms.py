from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Topic,UserProfile



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('student_id', 'course', 'avatar')
        labels = {
            'student_id': 'Mã số sinh viên',
            'course': 'Khoá',
            'avatar': 'Ảnh đại diện'
        }
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'})
        }






class TopicForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Topic
        fields = ['title', 'content', 'role', 'image']
