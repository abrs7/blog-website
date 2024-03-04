from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

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
    

