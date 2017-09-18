from django.shortcuts import render, redirect
import requests
from git_profile.forms import SearchForm
from git_profile.models import Search


def index(request):
    global url

    GITHUB_USER = 'dhavalsavalia' # Please enter Username here, while search function is not working

    user_profile = requests.get('https://api.github.com/users/{0}'.format(str(GITHUB_USER)))
    user_repos = requests.get('https://api.github.com/users/{0}/repos'.format(str(GITHUB_USER)))
    repo_detail_resp = requests.get('https://api.github.com/users/{0}/repos'.format(str(GITHUB_USER)))

    content = dict()

    content['user'] = user_profile.json()
    content['repos'] = user_repos.json()

    content['repo_detail_resp'] = repo_detail_resp.json()
    for key_list in content['repos']:
        url = "https://api.github.com/repos/{0}/{1}".format(str(GITHUB_USER), key_list['name'])

    repo = requests.get(url)

    content['repo'] = repo.json()

    langs = requests.get(content['repo']['languages_url']).json()
    content['languages'] = langs
    issues = requests.get(content['repo']['url'] + '/issues')
    if issues.json():
        content['issues'] = issues.json()

    return render(request, 'index.html', content)


def searchview(request):

    form = SearchForm()

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print('Form is invalid!')

    return render(request, 'base.html', {'form': form})
