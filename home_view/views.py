from django.shortcuts import render, get_object_or_404, redirect
from authentication.forms import UserForm, UpdateProfileForm, SkillsForm
from authentication.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from questions.forms import QuestionsForm, AnswerForm, ApplyJobForm
from questions.models import Questions_stuff, Answer_stuff, Applied_job
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from questions.models import Job_work
from django.utils import timezone

now = timezone.now()


# Create your views here.

def home(request):
    return render(request, 'home.html')


def question(request):
    all_questions = Questions_stuff.objects.filter().order_by('-publish_date')
    all_answer = Answer_stuff.objects.all()
    profile_detail = Profile.objects.all()
    paginator = Paginator(all_questions, 8)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    trending_question = Questions_stuff.objects.filter().order_by('-viewed')
    context = {
        'questions': all_questions,
        'profile_detail': profile_detail,
        'posts': posts,
        'all_questions_count': all_questions.count(),
        'trending_question': trending_question[:4]
    }
    return render(request, 'question.html', context)


def question_detail(request, id):
    question_det = get_object_or_404(Questions_stuff, id=id)
    question_det.viewed += 1
    question_det.save()
    profile_user = Profile.objects.all()
    all_answer = Answer_stuff.objects.filter(question=question_det).order_by('-published_time')
    all_question = Questions_stuff.objects.filter().order_by('-publish_date')
    question_detail_tag = question_det.tags_as_list()

    related_question = []
    for quest in all_question:
        for tag_all in quest.tags_as_list():
            if tag_all in question_detail_tag:
                related_question.append(quest)
    related_question = list(set(related_question))
    form = AnswerForm()
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.question = question_det
            instance.save()
            form = AnswerForm()
            messages.success(request, "answer submitted successfully")
    context = {
        'question': question_det,
        'profile_user': profile_user,
        'form': form,
        'answer': all_answer,
        'related_question': related_question
    }
    return render(request, 'question_detail.html', context)


@login_required(login_url='login')
def ask_question(request):
    user = request.user
    notified_email = None
    notified_whatsapp = None
    form = QuestionsForm()
    if request.method == "POST":
        if 'notifiedMe' in request.POST:
            notified_email = True
        else:
            notified_email = False
        if 'whatsapp_notify' in request.POST:
            notified_whatsapp = True
        else:
            notified_whatsapp = False
        form = QuestionsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            tag = form.cleaned_data.get('tag')
            detail = form.cleaned_data.get('detail')
            Questions_stuff.objects.create(title=title, detail=detail, body=body, owner=user, viewed=0, tag=tag,
                                           email_notify=notified_email, whatsapp_notify=notified_whatsapp)
            messages.success(request, "Question published successfully")
            return redirect('ask_question')
    context = {
        'form': form,
        'fieldValues': request.POST
    }
    return render(request, 'ask_question.html', context)


def job_list(request):
    all_job = Job_work.objects.filter(expire_date__gte=now.date(), job_hired=False).order_by('-published_date')
    paginator = Paginator(all_job, 8)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'job_count': all_job.count()
    }
    return render(request, 'job_list.html', context)


def job_detail(request, id):
    job_speci = get_object_or_404(Job_work, id=id)
    form = ApplyJobForm()
    if request.method == 'POST':
        email = request.POST['email']
        job_check = Applied_job.objects.filter(email=email, job=job_speci)
        if job_check.exists():
            messages.error(request, "User with this email already applied this Job")
            return redirect('job_detail', id=job_speci.id)
        form = ApplyJobForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.job = job_speci
            instance.save()
            messages.success(request, "Job apply done successfully")
            return redirect(job_detail, id=job_speci.id)
    context = {
        'job': job_speci,
        'form': form,
        'fieldValues': request.POST
    }
    return render(request, 'job_detail.html', context)


@login_required(login_url='login')
def user_profile(request):
    user = request.user
    user_pro = get_object_or_404(Profile, user=user)
    form = UpdateProfileForm(request.POST or None, instance=user_pro)
    if request.method == "POST":
        full_name = request.POST['full_name']
        if len(full_name) < 3:
            messages.error(request, "display name is too small")
        else:
            user.full_name = full_name
            user.save()
        form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=user_pro)
        if form.is_valid():
            form.save('user_profile')
    context = {
        'form': form,
        'user': user,
        'user_profile': user_pro
    }
    return render(request, 'user_profile.html', context)


@login_required(login_url='login')
def skills_update(request):
    user = request.user
    user_pro = get_object_or_404(Profile, user=user)
    form = SkillsForm(request.POST or None, instance=user_pro)
    if request.method == 'POST':
        form = SkillsForm(request.POST or None, instance=user_pro)
        if form.is_valid():
            form.save()
            messages.success(request, "skills updated successfully")
            return redirect('view_profile')
    else:
        form = SkillsForm('user_profile')
    context = {
        'form': form,
    }
    return render(request, 'user_profile.html', context)


@login_required(login_url='login')
def view_profile(request):
    return render(request, 'view_profile.html')


def notifications(request):
    return render(request, 'notifications.html')

# profile =========================== update
