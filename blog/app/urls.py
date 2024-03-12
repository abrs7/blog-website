
from django.urls import path
from . import views

urlpatterns = [
    path('contact_us',views.contact, name = 'contact'),
    path('', views.PostList.as_view(), name = 'post_list'),
    path('post_detail/<slug:slug>/',views.PostDetail.as_view(), name = 'post_detail'),
    path('create_post', views.CreatePost.as_view(), name='create_post'),
    path('register', views.signUp, name='signup'),
    path('login', views.login, name='log_in'),
    path('post_detail/<slug:slug>/comment',views.CreateComment.as_view(), name='add_comments')

 


]