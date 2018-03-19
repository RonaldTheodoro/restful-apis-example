from django.conf import settings
from django.shortcuts import render

from github import Github, GithubException

import requests

from . import forms


def index(request):
    is_cached = ('geodata' in request.session)

    if not is_cached:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
        response = requests.get(f'http://freegeoip.net/json/{ip_address}')
        request.session['geodata'] = response.json()

    geodata = request.session['geodata']
    context = {
        'ip': geodata['ip'],
        'country': geodata['country_name'],
        'latitude': geodata['latitude'],
        'longitude': geodata['longitude'],
        'api_key': settings.GOOGLE_MAPS_KEY,
        'is_cached': is_cached
    }
    return render(request, 'index.html', context)


def github(request):
    search_result = {}

    if 'username' in request.GET:
        username = request.GET['username']
        client = Github()

        try:
            user = client.get_user(username)
            search_result['name'] = user.name
            search_result['login'] = user.login
            search_result['public_repos'] = user.public_repos
            search_result['success'] = True
        except GithubException as error:
            search_result['message'] = error.data['message']
            search_result['success'] = False
        
        rate_limit = client.get_rate_limit()
        search_result['rate'] = {
            'limit': rate_limit.rate.limit,
            'remaining': rate_limit.rate.remaining,
        }
        

    return render(request, 'github.html', {'search_result': search_result})


def oxford(request):
    search_result = {}

    if 'word' in request.GET:
        form = forms.DictionaryForm(request.GET)

        if form.is_valid():
            search_result = form.search()

    else:
        form = forms.DictionaryForm()

    context = {'form': form, 'search_result': search_result}
    return render(request, 'oxford.html', context)