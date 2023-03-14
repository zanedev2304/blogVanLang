from django.shortcuts import render,redirect,get_object_or_404
from .models import CaseStatus,Case,CaseComment,CaseLog
from .forms import CaseForm,CaseStatusForm
# Create your views here.



def home_view(request):
    return render(request, 'home.html')


def case_list(request):
    cases = Case.objects.all()
    return render(request, 'case_list.html', {'cases': cases})

def case_detail(request, id):
    case = get_object_or_404(Case, id=id)
    return render(request, 'case_detail.html', {'case': case})

def create_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.author = request.user
            case.save()  # Lưu case mới với trường author đã được gắn
            return redirect('case_list')
    else:
        form = CaseForm()
    return render(request, 'create_case.html', {'form': form})


def update_case(request, id):
    case = get_object_or_404(Case, id=id)
    case_statuses = CaseStatus.objects.all()
    if request.method == 'POST':
        form = CaseStatusForm(request.POST, instance=case)
        if form.is_valid():
            case_log = form.save(commit=False)
            case_log.case = case
            case_log.user = request.user
            case_log.save()
            case.current_status = case_log.status
            case.save()
            return redirect('case_detail', id=id)
    else:
        form = CaseStatusForm()
    return render(request, 'update_case.html', {'form': form, 'case': case, 'case_statuses': case_statuses})