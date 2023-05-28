from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Topic,UserProfile,Category,MyTopic,Article,Knowledge
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group,User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    phone = forms.CharField(label='Số điện thoại', max_length=10, validators=[RegexValidator('^[0-9]*$', 'Vui lòng chỉ nhập số')])
    
    class Meta:
        model = UserProfile
        fields = ('avatar', 'phone',)
        labels = {
            'avatar': 'Ảnh đại diện'
        }
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'})
        }



class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.userprofile.name

class AssignTopicForm(forms.ModelForm):
    employee = CustomModelChoiceField(queryset=UserProfile.objects.all(), label='Nhân viên')

    class Meta:
        model = MyTopic
        fields = ['employee']
        labels = {
            'employee': 'Nhân viên',
        }

    def __init__(self, *args, **kwargs):
        self.is_end_time_updated = False
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['employee'].queryset = self.get_available_employees()

        self.is_end_time_updated = False

    def get_available_employees(self):
        employees = User.objects.filter(groups__name='Employee')
        if self.instance.pk:
            assigned_employees = MyTopic.objects.exclude(pk=self.instance.pk).filter(status='Đang xử lý').values_list('employee_id', flat=True)
            employees = employees.exclude(pk__in=assigned_employees)
        return employees

    def clean_employee(self):
        employee = self.cleaned_data['employee']
        if employee is not None:
            self.instance.status = 'Đang xử lý'
            self.instance.start_time_employee = timezone.now()
        return employee
    
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        if status == 'Hoàn thành' and not self.is_end_time_updated:
            self.instance.status = status
            self.instance.end_time = timezone.now()
            self.is_end_time_updated = True
        return cleaned_data

class KnowledgeForm(forms.ModelForm):
    class Meta:
        model = Knowledge
        fields = ['category', 'content', 'image']
        labels = {
            'category': 'Thể loại',
            'content':'Nội dung',
            'image':'Hình ảnh',
        }
    

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name':'Tên thể loại',
        }  
    
    
class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='default'))
    class Meta:
        model = Article
        fields = ['title', 'category','content', 'image','knowledge']
        labels = {
            'title':'Chủ đề',
            'category': 'Thể loại',
            'content':'Nội dung',
            'image':'Hình ảnh',
            'knowledge':'Knowledge',
        }



class TopicForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='default'))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), to_field_name='name')

    class Meta:
        model = Topic
        fields = ['title', 'category','content', 'image']
        labels = {
            'title':'Chủ đề',
            'category': 'Thể loại',
            'content':'Nội dung',
            'image':'Hình ảnh',
        }



