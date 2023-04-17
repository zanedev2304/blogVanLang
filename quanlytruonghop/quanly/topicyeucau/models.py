from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import RegexValidator
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    cus_id = models.CharField(max_length=10,default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=(('student', 'Student'), ('teacher', 'Teacher')), default='student')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Số điện thoại phải có 10 chữ số.")
    phone = models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True)
    student_id = models.CharField(max_length=10)
    course = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')

    def __str__(self):
        return self.user.username


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    image = models.ImageField(upload_to='articles/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Knowledge(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.article.title



class Image(models.Model):
    image = models.ImageField(upload_to='images/topic')

class Topic(models.Model):
    TITLE_MAX_LENGTH = 200
    ROLES = (
        ('SV', 'Sinh viên'),
        ('GV', 'Giảng viên'),
        ('PB', 'Phòng ban'),
    )

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    content = RichTextUploadingField(blank=True, null=True)
    image = models.ImageField(upload_to='images/topic', blank=True, null=True, default=None)
    slug = models.SlugField(max_length=100,unique=True,null=True)
    role = models.CharField(max_length=2, choices=ROLES)
    start_time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title
    

class MyTopic(models.Model):
    CHOICES = (
        ('Đã tiếp nhận', 'Đã tiếp nhận'),
        ('Đang xử lý', 'Đang xử lý'),
        ('Hoàn thành', 'Hoàn thành'),
    )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE) 
    name = models.CharField(max_length=255,blank=True) #Người xử lý
    cus_id = models.CharField(max_length=20,blank=True) 
    status = models.CharField(max_length=20, choices=CHOICES, default='Chờ tiếp nhận')
    start_time = models.DateTimeField(auto_now_add=True)
    start_time_request= models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    

    def __str__(self):
        return self.topic.title
    
    @property
    def topic_title(self):
        return self.topic.title
    
    @property
    def topic_content(self):
        return self.topic.content
    
    @property
    def topic_role(self):
        return self.topic.role
    
    @property
    def topic_author(self):
        return self.topic.author







class TopicSubmission(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    cus_id = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.topic.title}'