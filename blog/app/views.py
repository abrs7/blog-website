from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .forms import CreatePost, CreateComment
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

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

##List Comment
def CommentList(request):
    comments = Comment.objects.all()
     
    paginate = Paginator(comments, 3)
    page_number = request.GET.get('page')
    comment_page = paginate.get_page(page_number)
    return render(request, 'index.html', {'comment_page': comment_page})



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
    # post_id = Post.objects.get(pk=post_id)

    template_name = 'index.html'
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs.get('post_id')
        return context

# class CommentList(ListView):
#     queryset = Comment.objects.all()
#     # post_id = Post.objects.get(pk=post_id)

#     template_name = 'index.html'
#     paginate_by = 4
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['comment_id'] = self.kwargs.get('comment_id')
#         return context

class PostDetail(DetailView):
    
    model = Post
    template_name = 'post_detail.html'
# def PostDetail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'post_detail.html', {'post': post})    


class CreatePost( LoginRequiredMixin ,CreateView):
    model = Post
    form_class = CreatePost
    template_name = 'create_post.html'
    success_url = ''


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class CreateComment( LoginRequiredMixin ,CreateView):
    # post = Post.objects.all()
    model = Comment
    form_class = CreateComment
    template_name = 'add_comments.html'
    success_url = reverse_lazy('post_list')
    
    # fields = ('body',)


    def form_valid(self, form):
        # Get the Post instance associated with the slug
        post = Post.objects.get(slug=self.kwargs['slug'])
        # Set the post_id of the comment to the ID of the Post instance
        form.instance.post_id = post.id
        # Set the user associated with this comment
        form.instance.name = self.request.user
        return super().form_valid(form)