from django.shortcuts import render, redirect
from .forms import TopicForm






def home_view(request):
    return render(request,'bennguoidung/home.html')




def create_request(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') # điều hướng về trang chủ
    else:
        form = TopicForm()

    return render(request, 'bennguoidung/create_request.html', {'form': form})
