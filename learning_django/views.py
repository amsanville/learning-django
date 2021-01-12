import pygal
import requests
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    '''
    Displays the homepage
    '''
    context = {
        'title' : 'Home',
    }
    return render(request, 'base_home.html', context)

def all_repos(request):
    '''
    Displays information about all the repos available.
    '''
    # Make API request
    response = requests.get('https://api.github.com/users/amsanville/repos')
    context = {
        'title' : 'All Repos',
        'repo_data' : response.json()
    }
    return render(request, 'base_all_repos.html', context)

def repo_size(request):
    '''
    Displays a bar graph of of the size of all the repos.
    '''
    # Make API request
    response = requests.get('https://api.github.com/users/amsanville/repos')
    repo_data = response.json()

    # Make bar graph
    bars = pygal.HorizontalBar(logarithmic=True)
    bars.title = 'Size of my Repositories'
    bars.x_title = 'Size (log scale)'
    bars.y_labels = (1, 5, 10, 50, 100, 500, 1000, 5000)
    for item in repo_data:
        bars.add(item['name'], int(item['size']))

    # Add to the context variable
    context = {
        'chart' : bars.render_data_uri(),
        'title' : "Repo Size",
        }

    # Render the Django response
    return render(request, 'base_repo_size.html', context)

def repo_languages(request):
    '''
    Displays a pie chart of the different languages used in the repo chosen.
    '''
    # Read in the inputs
    username = request.GET.get('username')
    repo_name = request.GET.get('repo_name')

    context = {
        'title' : "Languages Used",
    }

    # Attempt to make an api request
    if username and repo_name:
        response = requests.get(f'https://api.github.com/repos/{username}/{repo_name}/languages')
        if response.status_code == 200:
            # Repo exists, set the context
            context['found'] = True
            context['username'] = username
            context['repo_name'] = repo_name
            
            # Make the pie chart
            languages_data = response.json()
            pie_chart = pygal.Pie()
            pie_chart.title = 'Languages Used in Repo'
            for key, value in languages_data.items():
                pie_chart.add(key, int(value))
            context['chart'] = pie_chart.render_data_uri()
        else:
            # Repo doesn't exist
            context['found'] = False
    else:
        # Repo doesn't exist
        context['found'] = False
    return render(request, 'base_repo_languages.html', context)