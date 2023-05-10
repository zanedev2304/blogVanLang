from django.shortcuts import render, redirect,HttpResponse
from .forms import TopicForm,LoginForm,UserProfileForm,AssignTopicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import UserProfile,Topic,MyTopic,Article,Rating,Knowledge
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
from django.contrib.auth.models import Group,User
import datetime
from django.http import JsonResponse
from django.http import HttpResponse, JsonResponse, HttpRequest

def user_in_group(user, group_name):
    """
    Kiểm tra xem user có thuộc group có tên là group_name hay không
    """
    try:
        group = Group.objects.get(name=group_name)
        return group in user.groups.all()
    except Group.DoesNotExist:
        return False

#----------------------------manageUser(View) -------------------------------------




class MyTopicView(View):
    def start_timer(self, mytopic):
        mytopic.start_time_request = datetime.datetime.now()
        mytopic.save()

    def end_timer(self, mytopic):
        mytopic.end_time = datetime.datetime.now()
        elapsed_time = mytopic.end_time - mytopic.start_time_request
        mytopic.elapsed_time = elapsed_time.seconds
        mytopic.save()

    def get(self, request, *args, **kwargs):
        mytopic = MyTopic.objects.get(pk=self.kwargs['mytopic_id'])
        if mytopic.status == 'Đang xử lý':
            self.start_timer(mytopic)

        context = {'mytopic': mytopic}
        return render(request, 'bennguoidung/topic_detail.html', context)

    def post(self, request, *args, **kwargs):
        mytopic = MyTopic.objects.get(pk=self.kwargs['mytopic_id'])
        if 'end_timer' in request.POST:
            self.end_timer(mytopic)
        elif 'start_timer' in request.POST:
            self.start_timer(mytopic)
        context = {'mytopic': mytopic}
        return render(request, 'bennguoidung/topic_detail.html', context)




#----------------------------Quan ly tai khoan -------------------------------------
def home_view(request):
    article_list = Article.objects.all()
    knowledges = Knowledge.objects.all()
    context = {
        'article_list': article_list,
        'knowledges': knowledges,
    }
    return render(request, 'bennguoidung/home.html',context )



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
        form = TopicForm(request.POST, request.FILES, )
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


class KnowledgeDetailView(DetailView):
    model = Knowledge
    template_name = 'bennguoidung/knowledge_detail.html'

def knowledge(request):
    knowledges = Knowledge.objects.all()
    return render(request, 'bennguoidung/knowledge.html', {'knowledges': knowledges})






def my_topic_detail(request, id):
    my_topic = get_object_or_404(MyTopic, topic_id=id)
    obj = Rating.objects.filter(score=0).order_by("?").first()
    status_changed = False  # Biến lưu trạng thái chuyển đổi
    form = None 

    if request.method == 'POST':
        if request.user.is_staff or request.user.groups.filter(name='manageUser').exists():
            status = request.POST.get('status')
            if status == 'Hoàn thành':
                my_topic.status = 'Hoàn thành'
                my_topic.end_time = timezone.now()
                try:
                    my_topic.save()
                    # redirect to success page or somewhere else
                except Exception as e:
                    print(e)
                    # do something else if save fails

            else:
                form = AssignTopicForm(request.POST, instance=my_topic)
                if form.is_valid():
                    my_topic = form.save() 
                    status_changed = True  # Đánh dấu trạng thái đã chuyển đổi
        else:
            form = AssignTopicForm(instance=my_topic)
    else:
        form = AssignTopicForm(instance=my_topic)

    if request.user.is_staff or request.user.groups.filter(name='manageUser').exists():  # Nếu người xem là staff
        if my_topic.status == 'Chờ tiếp nhận':
            my_topic.status = 'Đã tiếp nhận'
            my_topic.start_time_request = timezone.now()
            status_changed = True  # Đánh dấu trạng thái đã chuyển đổi
    if status_changed:  # Nếu trạng thái đã chuyển đổi thì lưu vào database
        try:
            my_topic.save()
        except Exception as e:
            print(e)
    context = {
        'mytopic': my_topic,
        'form': form,
        'object': obj,
    }
    return render(request, 'bennguoidung/topic_detail.html', context)





def rate_topic(request):
    if request.method == 'POST':
        el_id = request.POST.get('el_id')
        val = request.POST.get('val')
        print(val)
        print()
        if el_id.isdigit():
            obj = get_object_or_404(Rating, id=int(el_id))
            obj.score = int(val)
            obj.save()
            return JsonResponse({'success': True, 'score': obj.score})
    return JsonResponse({'success': False})






# -------------------------------MANGAGE VIEW-----------------------------
@user_passes_test(lambda u: u.is_staff or u.is_superuser or user_in_group(u, 'manageUser'))
def manage_view(request):
    return render(request,'bennguoidung/dashboard.html')



@user_passes_test(lambda u: u.is_staff or u.is_superuser or user_in_group(u, 'manageUser'))
def manage_request(request):
    mytopics = MyTopic.objects.all()
    return render(request, 'bennguoidung/quanlyyeucau.html',{'mytopics': mytopics})





