from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .forms import CreatePost
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Redirect to a success page or wherever you want
                return redirect(reverse('post_list'))
            else:
                # Handle invalid login
                return redirect(reverse('log_in'))
                pass
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signUp(request):
    
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
    else:
        form = UserCreationForm() 
            
             

          
    return render(request, 'register.html', {'form':form})


@login_required
def contact(request):
    message = {'address':'Bole, Addis Ababa'}
    return render(request,'contact.html',context=message)
class PostList(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class PostDetail(DetailView):
    
    model = Post
    template_name = 'post_detail.html'


class CreatePost( LoginRequiredMixin ,CreateView):
    model = Post
    form_class = CreatePost
    template_name = 'create_post.html'
    success_url = ''


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    