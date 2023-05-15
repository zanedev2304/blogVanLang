from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta
from django.urls import reverse
import pytz

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
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,default='Họ và Tên')
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Số điện thoại phải có 10 chữ số.")
    phone = models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True)
    student_id = models.CharField(max_length=10)
    course = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    role = models.CharField(max_length=255, default='Sinh viên')
    

    def __str__(self):
        return self.user.username


class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255,default='other')
    content = RichTextUploadingField(blank=True, null=True)
    image = models.ImageField(upload_to='articles/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    views = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])

    def add_like(self, user):
        if user not in self.likes.all():
            self.likes.add(user)
            self.like_count += 1
            self.save()

class Knowledge(models.Model):
    content = models.TextField(blank=True,null=True)
    category = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/knowledge', blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.content


class Image(models.Model):
    image = models.ImageField(upload_to='images/topic')

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    request_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Topic(models.Model):
    TITLE_MAX_LENGTH = 200
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    content = RichTextUploadingField(blank=True, null=True)
    image = models.ImageField(upload_to='images/topic', blank=True, null=True, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='topics')
    start_time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


    def save(self, *args, **kwargs):
        # Tăng request_count của category liên kết
        self.category.request_count += 1
        self.category.save()
        super(Topic, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    




class MyTopic(models.Model):
    CHOICES = (
        ('Đang xử lý', 'Đang xử lý'),
        ('Hoàn thành', 'Hoàn thành'),
    )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE) 
    employee = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    cus_id = models.CharField(max_length=20,blank=True) 
    status = models.CharField(max_length=20, choices=CHOICES, default='Chờ tiếp nhận')
    start_time = models.DateTimeField(auto_now_add=True)
    start_time_request= models.DateTimeField(null=True, blank=True)
    start_time_employee = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    elapsed_time = models.IntegerField(null=True, blank=True,default=0)

    def save(self, *args, **kwargs):
        if self.start_time_request and self.end_time:
            elapsed_time = self.end_time - self.start_time_request
            self.elapsed_time = int(elapsed_time.total_seconds() // 60)  # Chuyển đổi thành phút và chuyển thành số nguyên
        super().save(*args, **kwargs)
        
    def get_formatted_start_time_request(self):
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        start_time_request = self.start_time_request.astimezone(vietnam_tz)
        return start_time_request.strftime("%d/%m/%Y %H:%M:%S")

    def get_formatted_start_time(self):
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        start_time = self.start_time.astimezone(vietnam_tz)
        return start_time.strftime("%d/%m/%Y %H:%M:%S")

    def get_formatted_start_time_employee(self):
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        start_time_employee = self.start_time_employee.astimezone(vietnam_tz)
        return start_time_employee.strftime("%d/%m/%Y %H:%M:%S")
    
    def get_formatted_end_time(self):
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        end_time = self.end_time.astimezone(vietnam_tz)
        return end_time.strftime("%d/%m/%Y %H:%M:%S")

    def get_formatted_elapsed_time(self):
        hours = self.elapsed_time // 60
        minutes = self.elapsed_time % 60
        seconds = 0
        formatted_elapsed_time = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        return formatted_elapsed_time

    def __str__(self):
        return self.topic.title

    @property
    def topic_title(self):
        return self.topic.title
    
    @property
    def topic_content(self):
        return self.topic.content
    
    @property
    def topic_author(self):
        return self.topic.author

    @property
    def name(self):
        return self.employee.username if self.employee else ""
    



class Rating(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    score = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )

    def __str__(self):
        return self.topic.title
    
    @property
    def topic_title(self):
        return self.topic.title
    
    @property
    def topic_content   (self):
        return self.topic.content
    
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
    


