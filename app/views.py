from django.shortcuts import render
from django.http import HttpResponse
import django
import os
from app.models import choiceData
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
import csv
import ast
from ipware.ip import get_real_ip
# Create your views here.

def index(request):
    return render(request, 'app/index.html')

@ensure_csrf_cookie
def soccer(request):
    context_dict = {'CType': 'Choose the better soccer player'}
    return render(request, 'app/survey.html', context_dict)

@ensure_csrf_cookie
def math(request):
    context_dict = {'CType': 'Choose the better mathematician'}
    return render(request, 'app/survey.html', context_dict)
    
@ensure_csrf_cookie
def rappers(request):
    context_dict = {'CType': 'Choose the better rapper'}
    return render(request, 'app/survey.html', context_dict)
    
@ensure_csrf_cookie
def movies(request):
    context_dict = {'CType': 'Choose the better movie'}
    return render(request, 'app/survey.html', context_dict)
    
@ensure_csrf_cookie
def musicians(request):
    context_dict = {'CType': 'Choose the better musician'}
    return render(request, 'app/survey.html', context_dict)
    
@ensure_csrf_cookie
def colors(request):
    context_dict = {'CType': 'Choose the darker color'}
    return render(request, 'app/survey.html', context_dict)
    
@ensure_csrf_cookie
def places(request):
    context_dict = {'CType': 'Choose the better place'}
    return render(request, 'app/survey.html', context_dict)
    
@ensure_csrf_cookie
def numbers(request):
    context_dict = {'CType': 'Choose the bigger number'}
    return render(request, 'app/survey.html', context_dict)
    
def complete(request):
    if request.method == "POST":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'choice.settings')
        django.setup()
        compType = request.POST["compType"]
        print 'type ' + compType
        matchupNames = request.POST["matchupNames"]
        choices = request.POST['choices']
        TTChoose = request.POST["TTChoose"]
        Time = request.POST['Time']
        username = request.POST['username']
        if get_real_ip(request) is not None:
            ip = get_real_ip(request)
        print 'ip: ', ip
        c = choiceData(username=username, compType=compType, matchupNames=matchupNames, choices=choices, TTChoose=TTChoose, CTime=Time, ip=ip)
        c.save()
        results = ['test1', 'test2']
        context_dict = {'results': results}
        return render(request, 'app/complete_ajax.html', context_dict)
        
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/profile/')
        else:
            failure = {'reason': "Invalid login attempt."}
            return render(request, "app/login.html", failure)
            
    return render(request, 'app/login.html')
    
@login_required
def profile(request):
        return render(request, 'app/profile.html', {})

def data(request):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'choice.settings')
    django.setup()
    if request.method == "POST":
        compType = request.POST["compType"]
        if compType[-1] == ' ':
            compType = compType[:len(compType)-1]
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(compType)
        writer = csv.writer(response)
        # retrieve the correct dataset
        samples = choiceData.objects.filter(compType=compType)
        writer.writerow(['ID', 'Username', 'Type', 'Choice1', 'Choice2', 'Selection', 'TTChoose', 'Time of Survey Completion', 'IP'])
        count = 0
        for sample in samples:
            count += 1
            username = str(sample.username).replace('"','')
            CType = str(sample.compType).replace('"','')
            matchups = ast.literal_eval(sample.matchupNames)
            selection = ast.literal_eval(sample.choices)
            TTChoose = ast.literal_eval(sample.TTChoose)
            CTime = ast.literal_eval(sample.CTime)
            ip = sample.ip
            for i in range(len(selection)):
                row = [count, username, CType, matchups[i][0], matchups[i][1], selection[i], TTChoose[i], CTime, ip]
                writer.writerow(row)
        return response