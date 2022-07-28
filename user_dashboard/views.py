from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from questions.models import Questions_stuff, Answer_stuff
from authentication.models import Profile
from questions.forms import JobForm
import json
from django.http import JsonResponse, HttpResponse
import os
from django.conf import settings


# Create your views here.

@login_required(login_url='login')
def user_home(request):
    return render(request, 'user_home.html')


@login_required(login_url='login')
def skills_stat(request):
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    final_skills = {
        'backend': user_profile.backend_development,
        'frontend': user_profile.frontend_development,
        'hardware': user_profile.hardware,
        'uiandux': user_profile.uiandux,
        'artificial_intelligence': user_profile.artificial_intelligence
    }
    return JsonResponse({'skills_stat': final_skills}, safe=False)


@login_required(login_url='login')
def user_dashboard_profile(request):
    user = request.user
    all_question = Questions_stuff.objects.filter(owner=user)
    all_answer = Answer_stuff.objects.filter(question__owner=user)
    context = {
        'question_count': all_question.count(),
        'answer_count': all_answer.count()
    }
    return render(request, 'user_dashboard_profile.html', context)


@login_required(login_url='login')
def user_create_job(request):
    form = JobForm()
    if request.method == 'POST':
        form = JobForm(request.POST)
        enable_remote = True
        enable = request.POST['enable_remote']
        if enable == '1':
            enable_remote = True
        elif enable == '0':
            enable_remote = False
        if form.is_valid():
            instance = form.save(commit=False)
            instance.enable_remote = enable_remote
            instance.job_owner = request.user
            instance.save()
            return redirect('user_home')
    else:
        form = JobForm()

    country_data = []
    file_path = os.path.join(settings.BASE_DIR, 'countries.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for item in data:
            country_data.append(item['name'])
    context = {
        'country_name': country_data,
        'form': form,
        'fieldValues': request.POST
    }

    return render(request, 'user_create_job.html', context)
