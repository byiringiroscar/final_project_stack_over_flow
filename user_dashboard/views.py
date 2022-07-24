from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from questions.models import Questions_stuff, Answer_stuff
from authentication.models import Profile
import json
from django.http import JsonResponse, HttpResponse


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
    return render(request, 'user_create_job.html')
