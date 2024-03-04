
from django.urls import path
from . import views

urlpatterns = [
    path('contact_us',views.contact, name = 'contact'),
    path('', views.PostList.as_view(), name = 'post_list'),
    path('<slug:slug>/',views.PostList.as_view(), name = 'post_detail'),
 


]