from wsite.models import Profile
from wsite.util import fetch
from django.shortcuts import render, redirect
from wsite.forms import RegistrationForm
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/accounts/login')
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request,'../templates/registration/reg_form.html',args)

def update_profile(request):
    user = User.objects.get(pk=request.user.id)
    username = request.user.username
    url = f'https://api.github.com/users/{username}'
    data = fetch(url)
    user.profile.followers = data['followers']
    user.profile.lastUpdated = parse_datetime(data['updated_at'])
    user.save()

def displayprofile(request):
    update_profile(request)
    data = User.objects.get(username=request.user.username)
    user_name = request.user.username
    url = f'https://api.github.com/users/{user_name}/repos'
    reposdata = fetch(url)
    repos = []
    for repo in reposdata:
        repos += [repo['name']]
    return render(request,'../templates/profile.html',{'data':data , 'repos':repos})

def displayUsers(request):
    data = User.objects.all
    return render(request,'../templates/explore.html',{'data':data})