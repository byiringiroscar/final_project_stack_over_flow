from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from questions.models import Questions_stuff, Answer_stuff, Job_work, Applied_job, InterviewApplied, Badge
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from super_admin.decorators import *
from django.contrib.auth import get_user_model
from questions.forms import InterviewBadgeForm
from django.core.mail import EmailMessage
from django.template.loader import get_template
import threading
from django.contrib import messages

User = get_user_model()

now = timezone.now()


# Create your views here.
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def stat_skill_admin(request):
    application = Applied_job.objects.all()
    all_job = Job_work.objects.all()
    all_interviewed = InterviewApplied.objects.all()
    all_hired = Job_work.objects.filter(job_hired=True).count()
    final_stat = {
        'job': all_job.count(),
        'interview': all_interviewed.count(),
        'hired': all_hired,
        'application': application.count()
    }
    return JsonResponse({'final_stat': final_stat}, safe=False)


def super_login(request):
    user = request.user
    if user.is_authenticated and user.admin:
        return redirect('home_super')
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                if user.is_admin:
                    login(request, user)
                    return redirect('home_super')
                else:
                    messages.error(request, "only Admin credential required")
                    return redirect('super_login')
            else:
                messages.error(request, "invalid credential try again")
                return redirect('super_login')
        else:
            messages.error(request, "All fields are required")
            return redirect('super_login')

    return render(request, 'super_login.html')


@is_admin_user
def home_super(request):
    all_question = Questions_stuff.objects.all()
    all_answer = Answer_stuff.objects.all()
    all_application = Applied_job.objects.all()
    all_job = Job_work.objects.all()
    all_interviewed = InterviewApplied.objects.all()
    question_count = all_question.count()
    answer_count = all_answer.count()

    context = {
        'all_question': all_question.count(),
        'all_answer': all_answer.count(),
        'all_application': all_application.count(),
        'all_job': all_job.count(),
        'all_interviewed': all_interviewed.count(),
        'all_hired': all_job.filter(job_hired=True).count()
    }
    return render(request, 'home_super.html', context)


@is_admin_user
def all_job_super(request):
    job_posted = Job_work.objects.all().order_by('-published_date')
    context = {
        'job': job_posted,
        'now': now.date()
    }
    return render(request, 'all_job_super.html', context)


@is_admin_user
def all_job_view_super(request, id):
    job_detail = get_object_or_404(Job_work, id=id)
    context = {
        'job': job_detail,
        'now': now.date()
    }
    return render(request, 'all_job_view_super.html', context)


@is_admin_user
def applied_job_super(request):
    job_apply = Applied_job.objects.all().order_by('-applied_date')
    context = {
        'person_job': job_apply
    }
    return render(request, 'applied_job_super.html', context)


@is_admin_user
def question_super(request):
    all_question = Questions_stuff.objects.all().order_by('-publish_date')
    context = {
        'all_question': all_question
    }
    return render(request, 'question_super.html', context)


@is_admin_user
def delete_question_super(request, id):
    question = get_object_or_404(Questions_stuff, id=id)
    question.delete()
    messages.success(request, 'Question deleted successfully')
    return redirect('question_super')



@is_admin_user
def applied_job_profile_super(request, id):
    profile_detail = get_object_or_404(Applied_job, id=id)
    context = {
        'profile_detail': profile_detail
    }
    return render(request, 'applied_job_profile_super.html', context)


@is_admin_user
def all_user_super(request):
    all_user = User.objects.all()
    context = {
        'all_user': all_user
    }
    return render(request, 'all_user_super.html', context)


@is_admin_user
def all_badge_super(request):
    all_badge = Badge.objects.all().order_by('-published_date')
    context = {
        'all_badge': all_badge
    }
    return render(request, 'all_badge_super.html', context)


@is_admin_user
def approve_badge(request, id):
    badge = get_object_or_404(Badge, id=id)
    badge.badge_approved = True
    badge.save()
    messages.success(request, "badge given successfully")
    return redirect('all_badge_super')


@is_admin_user
def invitation_badge_super(request, id):
    badge = get_object_or_404(Badge, id=id)
    form = InterviewBadgeForm()
    if request.method == 'POST':
        form = InterviewBadgeForm(request.POST)
        dateInterview = request.POST['interview_date']
        new_date = dateInterview.split('T')
        date_exact = new_date[0]
        time_exact = new_date[1]
        if form.is_valid():
            link_interview = form.cleaned_data.get('interview_link')
            instance = form.save(commit=False)
            instance.badge = badge
            instance.save()
            message = f"Hello, {badge.user.full_name}  \n Thanks for your request we are still reviewing  but prepare " \
                      f"Interview for your badge request \n please prepare " \
                      f"your microphone and camera for better communication "
            subject = 'Interview Invitation'
            html_content = get_template('newsletter.html').render(
                {'badge': badge, 'message': message, 'date_exact': date_exact,
                 'time_exact': time_exact, 'link_interview': link_interview, 'now': now.date()})
            from_email = 'koracodeafrica@gmail.com'
            msg = EmailMessage(subject, html_content, from_email, to=[badge.user.email, ])
            msg.content_subtype = "html"
            EmailThread(msg).start()
            messages.success(request, "Invite link sent to email successfully")
            return redirect(all_badge_super)
    else:
        form = InterviewBadgeForm()
    context = {
        'form': form,
        'fieldValues': request.POST
    }

    return render(request, 'invitation_badge_super.html', context)


@is_admin_user
def job_delete_super(request, id):
    job_detail = get_object_or_404(Job_work, id=id)
    job_detail.delete()
    return redirect('all_job_super')


def logout_super(request):
    logout(request)
    return redirect('super_login')
