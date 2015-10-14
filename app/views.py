from django.shortcuts import render
from django.http import HttpResponse
import django
import os
from app.models import choiceData
from app.models import userInfo
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
import csv
import ast
import json
import random
from ipware.ip import get_real_ip
# Create your views here.

def index(request):
    return render(request, 'app/index.html')

@ensure_csrf_cookie
def soccer(request):
    context_dict = {'CType': 'Choose the soccer player who is more talented'}
    context_dict["username"] = get_username(request)
    return render(request, 'app/survey.html', context_dict)

@ensure_csrf_cookie
def math(request):
    context_dict = {'CType': 'Choose the mathematician who is more gifted'}
    context_dict["username"] = get_username(request)
    return render(request, 'app/survey.html', context_dict)
    
@ensure_csrf_cookie
def rappers(request):
    context_dict = {'CType': 'Choose the rapper who is a better artist'}
    context_dict["username"] = get_username(request)
    return render(request, 'app/survey.html', context_dict)
    
@ensure_csrf_cookie
def movies(request):
    context_dict = {'CType': 'Choose the movie that you like better'}
    context_dict["username"] = get_username(request)
    return render(request, 'app/survey.html', context_dict)
    
@ensure_csrf_cookie
def musicians(request):
    context_dict = {'CType': 'Choose the classical musician who is more talented'}
    context_dict["username"] = get_username(request)
    return render(request, 'app/survey.html', context_dict)
    
@ensure_csrf_cookie
def colors(request):
    context_dict = {'CType': 'Choose the color that is darker'}
    context_dict["username"] = get_username(request)
    return render(request, 'app/survey.html', context_dict)
    
@ensure_csrf_cookie
def places(request):
    context_dict = {'CType': 'Choose the place that is more beautiful'}
    context_dict["username"] = get_username(request)
    return render(request, 'app/survey.html', context_dict)
    
@ensure_csrf_cookie
def numbers(request):
    context_dict = {'CType': 'Choose the number which is bigger in terms of value'}
    context_dict["username"] = get_username(request)
    return render(request, 'app/survey.html', context_dict)

@ensure_csrf_cookie
def presidents(request):
    context_dict = {'CType': 'Choose the president that you think is more competent'}
    context_dict["username"] = get_username(request)
    return render(request, 'app/survey.html', context_dict)
    
def get_username(request):
    if request.method == "POST" and "username" in request.POST.keys():
        return request.POST["username"]
    
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
        familiarity = int(json.loads(request.POST["familiarity"]))
        print "familiarity", familiarity
        if get_real_ip(request) is not None:
            ip = get_real_ip(request)
        print 'ip: ', ip
        c = choiceData(username=username, compType=compType, matchupNames=matchupNames, choices=choices, TTChoose=TTChoose, CTime=Time, ip=ip, familiarity=familiarity)
        c.save()
        results = ['test1', 'test2']
        # valid = validateHuman(
        ctype, num_ctype, next_ctype_index = get_next_ctype(compType)
        # set validation data for Amazon payment
        if ctype == "end":
            secret_code = set_user_info(username)
            context_dict = {'results': results, 'next_ctype': ctype, 'username': username, 'num_ctype': num_ctype, 'completed': next_ctype_index, 'secret_code': secret_code}
            return render(request, 'app/complete_ajax.html', context_dict)
        context_dict = {'results': results, 'next_ctype': ctype, 'username': username, 'num_ctype': num_ctype, 'completed': next_ctype_index}
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
        writer.writerow(['ID', 'Username', 'Type', 'Choice1', 'Choice2', 'Selection', 'TTChoose', 'Familiar', 'Time of Survey Completion', 'IP'])
        count = 0
        for sample in samples:
            count += 1
            username = str(sample.username).replace('"','')
            CType = str(sample.compType).replace('"','')
            matchups = ast.literal_eval(sample.matchupNames)
            selection = ast.literal_eval(sample.choices)
            TTChoose = ast.literal_eval(sample.TTChoose)
            familiarity = sample.familiarity
            CTime = ast.literal_eval(sample.CTime)
            ip = sample.ip
            for i in range(len(selection)):
                row = [count, username, CType, matchups[i][0], matchups[i][1], selection[i], TTChoose[i], familiarity, CTime, ip]
                writer.writerow(row)
        return response
        
@login_required
def user_info(request):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'choice.settings')
    django.setup()
    if request.method == "POST":
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_info.csv"'
        writer = csv.writer(response)
        writer.writerow(["username", "num test", "secret code"])
        data = userInfo.objects.all()
        for user in data:
            username = user.username
            number_test = user.number_test
            secret_code = user.secret_code
            row = [username, number_test, secret_code]
            writer.writerow(row)
    return response
        
def get_next_ctype(last_ctype):
    ctype_list = ["numbers", "movies", "presidents", "places", "musicians", "math", "rappers", "soccer"]
    next_ctype_index = ctype_list.index(last_ctype) + 1
    num_ctype = len(ctype_list)
    if next_ctype_index == len(ctype_list):
        return "end", num_ctype, next_ctype_index
    next_ctype = ctype_list[next_ctype_index]
    return next_ctype, num_ctype, next_ctype_index
    
def get_last_ctype(ctype):
    ctype_list = ["numbers", "movies", "presidents", "places", "musicians", "math", "rappers", "soccer"]
    last_ctype_index = ctype_list.index(ctype) - 1
    last_ctype = ctype_list[last_ctype_index]
    return last_ctype
    
def update_familiarity(request, ctype):
    if request.method == "POST" and "familiarity" in request.POST.keys():
        username = request.POST["username"]
        # get the last_ctype for filtering purposes
        last_ctype = get_last_ctype(ctype)
    
def set_user_info(username):
    # setup django to work with the database
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'choice.settings')
    django.setup()
    # create the randomly generated secret code for Amazon MTurk
    secret_code = ''.join(random.choice('0123456789ABCDEF') for i in range(10))
    # get the data for a given username and the numbers survey
    num_data = choiceData.objects.filter(username=username, compType="numbers")[0]
    matchups = ast.literal_eval(num_data.matchupNames)
    choices = [int(element) for element in ast.literal_eval(num_data.choices)]
    num_valid = True
    for i in range(len(choices)):
        if choices[i] != max(int(matchups[i][0]), int(matchups[i][1])):
            num_valid = False
            break
    # save the userInfo to the database
    u = userInfo(username=username, number_test=num_valid, secret_code=secret_code)
    u.save()
    return secret_code
    