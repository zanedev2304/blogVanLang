from django.db import models
from django.contrib.auth.models import User

class Case(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    customer = models.CharField(max_length=10, choices=(('Student', 'Student'), ('Teacher', 'Teacher')))
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_cases')
    handler = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases_handled', null=True, blank=True)
    processor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processed_cases', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases_created', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']

    def save(self, *args, **kwargs):
        if not self.author:
            self.author = kwargs.pop('author', None)
        if self.author == self.handler or self.author == self.assignee:
            self.author = None
        super().save(*args, **kwargs)

class CaseComment(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['created_at']

class CaseStatus(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE,related_name='statuses', default=None)
    status = models.CharField(max_length=50)
    comment = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    

    def __str__(self):
        return f"{self.case} - {self.status}"

class CaseLog(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(CaseStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.case.title} - {self.status}'

    class Meta:
        ordering = ['-created_at']
