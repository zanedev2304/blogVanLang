from django import forms
from .models import Case,CaseStatus,CaseLog

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['customer', 'handler', 'assignee', 'description']



class CaseStatusForm(forms.ModelForm):
    status = forms.ModelChoiceField(queryset=CaseStatus.objects.all(), required=True)
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = CaseLog
        fields = ['status', 'comment']