from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .forms import CreatePost
# Create your views here.
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