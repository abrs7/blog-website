from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment, Profile
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, View
from .forms import CreatePost, CreateComment,  UserProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import re


    
class EditProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UserProfileForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile
    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     if 'profile_pic' in self.request.FILES:
    #         form.instance.profile_pic = self.request.FILES['profile_pic']
    #     form.save()
    #     return super().form_valid(form)
    def form_valid(self, form):
        form.instance.user = self.request.user
        if self.request.FILES.get('profile_pic'):
            form.instance.profile_pic = self.request.FILES['profile_pic']
        form.save()
        return super().form_valid(form)

# @login_required
# def view_profile(request):
#     profile = request.user.profile
#     print(profile.profile_pic)
#     return render(request, 'view_profile.html', {'profile':profile})
@login_required
def view_profile(request):
    profile = request.user.profile
    print(profile.profile_pic)
    return render(request, 'view_profile.html', {'profile':profile})
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
    post_slug = request.GET.get('post_id')

    # Retrieve the post object based on the post_slug
    post = get_object_or_404(Post, slug=post_slug)

    # Filter comments related to the post
    comments = Comment.objects.filter(post=post)
     
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
def my_view(request):
    # Assuming you have logic to retrieve the profile associated with the current user
    profile = Profile.objects.get(user=request.user)  # Adjust this to fit your actual logic
    
    return render(request, 'base.html', {'profile': profile})
# class CommentList(ListView):
#     queryset = Comment.objects.all()
#     # post_id = Post.objects.get(pk=post_id)

#     template_name = 'index.html'
#     paginate_by = 4
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['comment_id'] = self.kwargs.get('comment_id')
#         return context

# class PostDetail(DetailView):
    
#     model = Post
#     template_name = 'post_detail.html'
    
class PostDetail(View):
    def get(self, request, slug):
        # match = re.match(r'blog_(\d+)', slug)
        # if match:
        #     slug = match.group(1)
        post = get_object_or_404(Post, slug=slug)
        comment_list = Comment.objects.filter(post=post).order_by('-created_on')

        paginator = Paginator(comment_list, 4)
        page = request.GET.get('page')

        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        return render(request, 'post_detail.html', {'post': post, 'comments': comments})    

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

def show_more_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    start_index = int(request.GET.get('start_index', 0))
    end_index = start_index + 15
    comments = post.comments.all()[start_index:end_index]
    context = {
        'comments': comments,
        'start_index': start_index,
        'end_index': end_index,
        'post_id': post.id,
    }
    return render(request, 'more_comments.html', context)        
