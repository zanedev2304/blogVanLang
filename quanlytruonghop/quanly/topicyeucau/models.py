from django.db import models
from ckeditor.fields import RichTextField

class Topic(models.Model):
    TITLE_MAX_LENGTH = 200
    ROLES = (
        ('SV', 'Sinh viên'),
        ('GV', 'Giảng viên'),
        ('PB', 'Phòng ban'),
    )

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    content = RichTextField()
    role = models.CharField(max_length=2, choices=ROLES)

    def __str__(self):
        return self.title
