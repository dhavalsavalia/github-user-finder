from __future__ import absolute_import
from django.shortcuts import render, redirect
from django.views.generic import ListView
import requests
from git_profile.forms import SearchForm
from git_profile import models


class IndexListView(ListView):

    model = models.Search
    template_name = 'index.html'

    def get_context_data(self, **kwargs):

        global url, github_user

        # search_fun = IndexListView()
        github_user_query = models.Search.objects.all().last()
        github_user = github_user_query.search_query

        user_profile = requests.get('https://api.github.com/users/{0}'.format(str(github_user)))
        user_repos = requests.get('https://api.github.com/users/{0}/repos'.format(str(github_user)))
        repo_detail_resp = requests.get('https://api.github.com/users/{0}/repos'.format(str(github_user)))

        context = dict()

        context['user'] = user_profile.json()
        context['repos'] = user_repos.json()

        context['repo_detail_resp'] = repo_detail_resp.json()
        for key_list in context['repos']:
            url = "https://api.github.com/repos/{0}/{1}".format(str(github_user), key_list['name'])

        repo = requests.get(url)

        context['repo'] = repo.json()

        langs = requests.get(context['repo']['languages_url']).json()
        context['languages'] = langs
        issues = requests.get(context['repo']['url'] + '/issues')
        if issues.json():
            context['issues'] = issues.json()

        return context


def searchview(request):

    form = SearchForm()

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            form.save()
            return index(request)
        else:
            print('Form is invalid!')

    return render(request, 'base.html', {'form': form})
