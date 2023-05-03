from django.shortcuts import render, redirect,HttpResponse
from .forms import TopicForm,LoginForm,UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import UserProfile,Topic,MyTopic,Article
from django.views import View
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.views.generic import ListView,DetailView
from django.utils import timezone
from django.utils.html import strip_tags
from PIL import Image
from django.conf import settings
import uuid
from django.shortcuts import render, get_object_or_404


#----------------------------Quan ly tai khoan -------------------------------------
def home_view(request):
    article_list = Article.objects.all()
    return render(request, 'bennguoidung/home.html', {'article_list': article_list})



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


# Check if user is staff or superuser
# Check if user is staff or superuser

def update_user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('account_profile')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {'form': form}
    return render(request, 'account/update_profile.html', context)



#----------------------------Yeu cau ca nhan -------------------------------------

@login_required(login_url='/login')
@user_passes_test(lambda u: u.userprofile.phone is not None, login_url='account_profile')
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



@login_required(login_url='/login')
def mytopic(request):
    user = request.user
    my_topics = MyTopic.objects.filter(topic__author=user)
    return render(request, 'bennguoidung/mytopic.html', {'my_topics': my_topics})





class ArticleDetailView(DetailView):
    model = Article
    template_name = 'bennguoidung/article_detail.html'




def my_topic_detail(request, id):
    my_topic = get_object_or_404(MyTopic, topic_id=id)
    status_changed = False  # Biến lưu trạng thái chuyển đổi
    if request.user.is_staff:  # Nếu người xem là staff
        my_topic.status = 'Đã tiếp nhận'
        my_topic.start_time_request = timezone.now()
        status_changed = True  # Đánh dấu trạng thái đã chuyển đổi
    if status_changed:  # Nếu trạng thái đã chuyển đổi thì lưu vào database
        try:
            my_topic.save()
        except Exception as e:
            print(e)
    return render(request, 'bennguoidung/topic_detail.html', {'mytopic': my_topic})




# -------------------------------MANGAGE VIEW-----------------------------

def manage_view(request):
    return render(request,'manageCNTT/home.html')


def manage_request(request):
    mytopics = MyTopic.objects.all()
    return render(request, 'manageCNTT/quanlyyeucau.html',{'mytopics': mytopics})






