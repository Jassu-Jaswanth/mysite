from wsite.models import Profile, Repositories
from wsite.util import fetch
from django.shortcuts import render, redirect
from wsite.forms import RegistrationForm
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta, timezone

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            p = Profile()
            p.user = request.POST.get('username')
            p.save()
        return redirect('/accounts/login')

    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request,'../templates/registration/reg_form.html',args)

def store(request):
    user_name = request.user.username
    user = User.objects.get(username=user_name)
    url = f'https://api.github.com/users/{user_name}'
    data = fetch(url)
    user.profile.followers = data['followers']
    url = f'https://api.github.com/users/{user_name}/repos'
    data = fetch(url)
        
    existing_repos = Repositories.objects.filter(username = user_name)
    for repo in data:
        e = existing_repos.filter(repo_name=repo['name'])
        if(e.exists()):
            e.stars = repo['stargazers_count']
        else:
            r = Repositories()
            r.username = user_name
            r.repo_name = repo['name']
            r.stars = repo['stargazers_count']
            r.save()
    ts = datetime.now()
    ts += timedelta(hours=5,minutes=30)
    user.profile.lastUpdated = str(ts.strftime("%d %b, %Y %I:%M %p"))
    user.profile.save()
    return redirect('/accounts/profile/')

def displayprofile(request):
    user_name = request.user.username
    data = User.objects.get(username=user_name)
    reposdata = Repositories.objects.all()
    repos = {}
    for repo in reposdata:
        if repo.username == user_name:
            n = repo.repo_name
            repos[f'{n}'] = repo.stars
    return render(request,'../templates/profile.html',{'data':data , 'repos':repos})

def displayUsers(request):
    data = User.objects.all
    return render(request,'../templates/explore.html',{'data':data})

def extprofile(request):
    user_name = request.POST.get('user_name')
    data = User.objects.get(username=user_name)
    reposdata = Repositories.objects.all()
    repos = {}
    for repo in reposdata:
        if repo.username == user_name:
            n = repo.repo_name
            repos[f'{n}'] = repo.stars
    return render(request,'../templates/extprofile.html',{'data':data , 'repos':repos})
