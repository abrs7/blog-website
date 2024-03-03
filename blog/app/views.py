from django.shortcuts import render

# Create your views here.
def contact(request):
    message = {'address':'Bole, Addis Ababa'}
    return render(request,'contact.html',context=message)