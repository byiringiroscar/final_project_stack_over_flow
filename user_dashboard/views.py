from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from questions.models import Questions_stuff, Answer_stuff, Job_work, Applied_job, InterviewApplied, Badge
from authentication.models import Profile
from questions.forms import JobForm, InterviewAppliedForm, QuestionsForm, BadgeForm
import json
from django.http import JsonResponse, HttpResponse
import os
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django_pandas.io import read_frame
import threading
from django.contrib import messages

now = timezone.now()


# Create your views here.
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


@login_required(login_url='login')
def user_home(request):
    all_questions = Questions_stuff.objects.filter(owner=request.user)
    all_answer = Answer_stuff.objects.filter(question__owner=request.user)
    all_job = Job_work.objects.filter(job_owner=request.user)
    all_applied = Applied_job.objects.filter(job__job_owner=request.user)
    interviewed_stat = InterviewApplied.objects.filter(applied_person__job__job_owner=request.user)
    context = {
        'all_questions': all_questions.count(),
        'all_answer': all_answer.count(),
        'all_job': all_job.count(),
        'all_applied': all_applied.count(),
        'job_hired': all_job.filter(job_hired=True).count(),
        'interviewed_stat': interviewed_stat.count()
    }
    return render(request, 'user_home.html', context)


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
    all_job = Job_work.objects.filter(job_owner=request.user)
    context = {
        'question_count': all_question.count(),
        'answer_count': all_answer.count(),
        'all_job': all_job.count(),
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
            messages.success(request, "Job created successfully")
            return redirect('job_user_admin')
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


@login_required(login_url='login')
def job_user_admin(request):
    job_posted = Job_work.objects.filter(job_owner=request.user).order_by('-published_date')
    context = {
        'job': job_posted,
        'now': now.date()
    }
    return render(request, 'job_user_admin.html', context)


@login_required(login_url='login')
def job_user_view_admin(request, id):
    job_detail = get_object_or_404(Job_work, id=id)
    context = {
        'job': job_detail
    }
    return render(request, 'job_user_view_admin.html', context)


@login_required(login_url='login')
def job_person_applied_all(request, id):
    job_id = get_object_or_404(Job_work, id=id)
    applied_job_all = Applied_job.objects.filter(job=job_id)
    context = {
        'person_job': applied_job_all
    }
    return render(request, 'job_person_applied_all.html', context)


@login_required(login_url='login')
def job_applied_admin(request):
    job_apply = Applied_job.objects.filter(job__job_owner=request.user).order_by('-applied_date')
    context = {
        'person_job': job_apply
    }
    return render(request, 'job_applied_admin.html', context)


@login_required(login_url='login')
def applied_profile(request, id):
    profile_detail = get_object_or_404(Applied_job, id=id)
    context = {
        'profile_detail': profile_detail
    }
    return render(request, 'applied_profile.html', context)


@login_required(login_url='login')
def invitation_applied(request, id):
    applied_person = get_object_or_404(Applied_job, id=id)
    form = InterviewAppliedForm()
    if request.method == 'POST':
        form = InterviewAppliedForm(request.POST)
        dateInterview = request.POST['interview_date']
        new_date = dateInterview.split('T')
        date_exact = new_date[0]
        time_exact = new_date[1]
        if form.is_valid():
            link_interview = form.cleaned_data.get('interview_link')
            instance = form.save(commit=False)
            instance.applied_person = applied_person
            instance.save()
            Applied_job.objects.filter(id=id).update(interview=True)
            message = f"Hello, {applied_person.full_name}  \n Congratulations you have been selected to attend " \
                      f"Interview for Your applied job called {applied_person.job.title_developer} \n please prepare " \
                      f"your microphone and camera for better communication "
            subject = 'Interview Invitation'
            html_content = get_template('newsletter.html').render(
                {'applied_person': applied_person, 'message': message, 'date_exact': date_exact,
                 'time_exact': time_exact, 'link_interview': link_interview, 'now': now.date()})
            from_email = 'koracodeafrica@gmail.com'
            msg = EmailMessage(subject, html_content, from_email, to=[applied_person.email, ])
            msg.content_subtype = "html"
            EmailThread(msg).start()
            messages.success(request, "Invite link sent to email successfully")
            return redirect(applied_profile, id=applied_person.id)
    else:
        form = InterviewAppliedForm()
    context = {
        'form': form,
        'fieldValues': request.POST
    }
    return render(request, 'invitation_applied.html', context)


@login_required(login_url='login')
def hire_person_admin(request, id):
    profile_detail = get_object_or_404(Applied_job, id=id)
    Applied_job.objects.filter(id=id).update(hired_apply=True)
    job_detail = get_object_or_404(Job_work, id=profile_detail.job.id)
    job_status = Job_work.objects.filter(id=job_detail.id).update(job_hired=True)
    # send message to people applied on this specified job if they get hired or failed to get the job
    job_announce = Applied_job.objects.filter(job=profile_detail.job)
    if job_announce.exists():
        for person in job_announce:
            if not person.hired_apply:
                person.rejected_apply = True
                person.save()
                message = f"Hello, {person.full_name}  \n We are sorry to tell you  that you haven't selected " \
                          f"for Job you applied called {person.job.title_developer} \n After best review " \
                          f"We have decided to continue with other match with our criteria \n " \
                          f"We wish only best in the future"
                subject = 'Job Response'
                html_content = get_template('selected_person.html').render(
                    {'applied_person': person.full_name, 'message': message, 'now': now.date()})
                from_email = 'koracodeafrica@gmail.com'
                msg = EmailMessage(subject, html_content, from_email, to=[person.email, ])
                msg.content_subtype = "html"
                EmailThread(msg).start()
            else:
                message_congz = f"Hello, {person.full_name}  \n We are Happy to inform you  that you have be selected " \
                                f"for Job you applied called {person.job.title_developer} \n After best review " \
                                f"We have decided to continue with you \n "
                subject_congz = 'Job Response'
                html_content = get_template('selected_person.html').render(
                    {'applied_person': person.full_name, 'message': message_congz, 'now': now.date()})
                from_email = 'koracodeafrica@gmail.com'
                msg = EmailMessage(subject_congz, html_content, from_email, to=[person.email, ])
                msg.content_subtype = "html"
                EmailThread(msg).start()
        messages.success(request, "Result sent successfully")
        return redirect('applied_profile', id=profile_detail.id)
    else:
        return redirect('user_home')


@login_required(login_url='login')
def question_admin(request):
    all_question = Questions_stuff.objects.filter(owner=request.user)
    context = {
        'all_question': all_question
    }
    return render(request, 'question_admin.html', context)


@login_required(login_url='login')
def edit_question_admin(request, id):
    question_detail = get_object_or_404(Questions_stuff, id=id)
    form = QuestionsForm(request.POST or None, instance=question_detail)
    if request.method == 'POST':
        form = QuestionsForm(request.POST or None, instance=question_detail)
        if form.is_valid():
            form.save()
            messages.success(request, "Edit question done successfully")
            return redirect('question_admin')
    context = {
        'form': form,
        'question_detail': question_detail
    }
    return render(request, 'edit_question.html', context)


@login_required(login_url='login')
def request_badger_user(request):
    badge = Badge.objects.all()
    all_badger_user = [user_b.user for user_b in badge]
    form = BadgeForm()
    if request.method == 'POST':
        form = BadgeForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user in all_badger_user:
                messages.error(request, "Badge request already sent")
                return redirect('request_badger_user')
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "Badge request sent successfully")
            return redirect('request_badger_user')
    else:
        form = BadgeForm()
    context = {
        'form': form,
        'fieldValues': request.POST
    }
    return render(request, 'request_badger_user.html', context)
