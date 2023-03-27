from django.shortcuts import render, redirect,HttpResponse
from .forms import TopicForm,LoginForm,UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import UserProfile,Topic,MyTopic
from django.views import View
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.views.generic import ListView,DetailView
from django.utils import timezone
from django.utils.html import strip_tags


#----------------------------Quan ly tai khoan -------------------------------------
def home_view(request):
    return render(request,'bennguoidung/home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])

            if user is not None:
                login(request,user)
                return redirect('home')
        
            else:
                return redirect('login')
    
    else:
        form = LoginForm()
    
    return render(request,'registration/login.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('login')

@method_decorator(login_required(login_url='/login'), name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AccountView(View):
    def get(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
            form = UserProfileForm(instance=profile)
            return render(request, 'account/account.html', {'form': form})
        except UserProfile.DoesNotExist:
            return render(request, 'account/account.html')

    def post(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
            form = UserProfileForm(instance=profile)
            return render(request, 'account/account.html', {'form': form})
        except UserProfile.DoesNotExist:
            return render(request, 'account/account.html')



# Check if user is staff or superuser
def is_staff_or_superuser(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@user_passes_test(is_staff_or_superuser)
def update_user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('account-view')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {'form': form}
    return render(request, 'account/update_profile.html', context)



#----------------------------Yeu cau ca nhan -------------------------------------

@login_required(login_url='/login')
def create_request(request):
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()

            my_topic = MyTopic.objects.create(
                topic=topic,
            )

            return redirect('my-topic')
    else:
        form = TopicForm()

    context = {'form': form}
    return render(request, 'bennguoidung/create_request.html', context)



def mytopic(request):
    my_topics = MyTopic.objects.all()
    for topic in my_topics:
        if topic.end_time is None:
            topic.status = "Đang xử lý"
        elif topic.end_time > topic.start_time:
            topic.status = "Đã xử lý"
        else:
            topic.status = "Hết hạn"
    return render(request, 'bennguoidung/Mytopic.html', {'my_topics': my_topics})





class TopicDetailView(DetailView):
    model = MyTopic
    template_name = 'bennguoidung/topic_detail.html'



