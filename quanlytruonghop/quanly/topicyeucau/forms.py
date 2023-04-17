from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Topic,UserProfile
from django.core.validators import RegexValidator

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    phone = forms.CharField(label='Số điện thoại', max_length=10, validators=[RegexValidator('^[0-9]*$', 'Vui lòng chỉ nhập số')])
    
    class Meta:
        model = UserProfile
        fields = ('avatar', 'phone')
        labels = {
            'avatar': 'Ảnh đại diện'
        }
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'})
        }





class TopicForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='default'))
    class Meta:
        model = Topic
        fields = ['title', 'content', 'slug', 'image']
        labels = {
            'title':'Chủ đề',
            'content':'Nội dung',
            'slug': 'Thể loại',
            'image':'Hình ảnh',
        }
