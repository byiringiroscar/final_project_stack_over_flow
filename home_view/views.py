from django.shortcuts import render, get_object_or_404, redirect
from authentication.forms import UserForm, UpdateProfileForm, SkillsForm
from authentication.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from questions.forms import QuestionsForm, AnswerForm, ApplyJobForm, Connect_userForm, SendRequestForm
from questions.models import Questions_stuff, Answer_stuff, Applied_job, ConnectWith, FriendRequest, ChatGroup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from questions.models import Job_work
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model
import openai
import json
from django.core import serializers
from django.http import JsonResponse
from decouple import config
from .models import Chat
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

User = get_user_model()

now = timezone.now()
openai_api_key = config('openai_api_key')
openai.api_key = openai_api_key


# Create your views here.

def ask_openai(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )
    answer = response.choices[0].text.strip()
    return answer


def home(request):
    return render(request, 'home.html')


def question(request):
    all_questions = Questions_stuff.objects.filter().order_by('-publish_date')
    search_question = request.GET.get('search_question')
    if search_question != '' and search_question is not None:
        all_questions = Questions_stuff.objects.filter(
            Q(title__icontains=search_question) | Q(tag__icontains=search_question) | Q(body__in=search_question) | Q(
                detail__icontains=search_question)).distinct()
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
    question_det.viewed = question_det.viewed + 1
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
            Questions_stuff.objects.create(title=title, detail=detail, body=str(body), owner=user, viewed=0, tag=tag,
                                           email_notify=notified_email)
            messages.success(request, "Question published successfully")
            return redirect('question')
    context = {
        'form': form,
        'fieldValues': request.POST
    }
    return render(request, 'ask_question.html', context)


def job_list(request):
    all_job = Job_work.objects.filter(expire_date__gte=now.date(), job_hired=False).order_by('-published_date')
    job_search = request.GET.get('job_all')
    job_langauge = request.GET.get('language')
    job_price = request.GET.get('job_price')
    if job_search != '' and job_search is not None:
        all_job = all_job.filter(Q(title_task__contains=job_search) | Q(title_developer__icontains=job_search))
    elif job_langauge != '' and job_langauge is not None:
        all_job = all_job.filter(
            Q(country_location__icontains=job_langauge) | Q(job_type__icontains=job_langauge)).distinct()
    elif job_price != '' and job_price is not None:
        all_job = all_job.filter(amount_range_end__gte=job_price)
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
    job_tag_all = job_speci.tags_as_list()
    all_job = Job_work.objects.filter(job_hired=False, expire_date__gte=now.date())
    job_related = []
    for job in all_job:
        for tag_all in job.tags_as_list():
            if tag_all in job_tag_all:
                job_related.append(job)
    job_related = list(set(job_related))

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
        'job_related': job_related,
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


def view_profile_outside(request, id):
    question_det = get_object_or_404(Questions_stuff, id=id)
    profile_id = question_det.owner.id
    all_question = Questions_stuff.objects.filter(owner_id=profile_id)
    all_answer = Answer_stuff.objects.filter(question__owner_id=profile_id)
    user_question = get_object_or_404(User, id=profile_id)
    profile_user = get_object_or_404(Profile, user=user_question)
    count_view = 0
    for quest in Questions_stuff.objects.filter(owner_id=profile_id):
        count_view += quest.viewed
    context = {
        'user_question': user_question,
        'profile_user': profile_user,
        'all_answer_count': all_answer.count(),
        'all_question_count': all_question.count(),
        'count_view': count_view,
        'question_det': question_det
    }

    return render(request, 'view_profile_outside.html', context)

@login_required(login_url='login')
def connect_with_me(request, id):
    user = request.user
    channel_layer = get_channel_layer()
    user_connect = get_object_or_404(User, id=id)
    form = SendRequestForm()
    from_user = user
    to_user = user_connect
    if request.method == 'POST':
        form = SendRequestForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.from_user = user
            instance.to_user = user_connect
            # check if no other friend request sent
            friend_request = FriendRequest.objects.filter(from_user=user).filter(to_user=user_connect)
            if friend_request.exists():
                messages.info(request, "You have already sent a friend request to this user.")
                return redirect('connect_with_me', id=user_connect.id)
            # check if the user already in same chatgroup as members
            existing_groups = ChatGroup.objects.filter(members=from_user).filter(members=to_user)
            if existing_groups.exists():
                messages.info(request, "You are already friends and connected.")
                return redirect('connect_with_me', id=user_connect.id)
            instance.save()
            # send the request for connecting
            user_channel_name = f"user_sendfriend_request{user_connect.id}"
            data_sent = {
                'from_user': user.id,
                'to_user': user_connect.id,
                'subject': instance.subject,
                'body': instance.body,
                'friend_request_id': instance.id
            }
            event = {
                'type': 'send_request_friend',
                'data_sent': data_sent
            }
            async_to_sync(channel_layer.group_send)(user_channel_name, event)
            messages.success(request, "Thanks for your connect wait as your request to be approved")
            return redirect('connect_with_me', id=user_connect.id)
    else:
        form = SendRequestForm()
    context = {
        'form': form,
        'fieldValues': request.POST
    }
    return render(request, 'connect_with_me.html', context)


@login_required(login_url='login')
def all_friends_user(request):
    # filter all chatgroup where request.user is member
    all_chat_groups = ChatGroup.objects.filter(members=request.user)
    context = {
        'all_chat_groups': all_chat_groups
    }
    return render(request, 'all_friends_user.html', context)


@login_required(login_url='login')
def approve_friend_request(request, id):
    friend_request = get_object_or_404(FriendRequest, id=id)

    if friend_request.to_user != request.user:
        messages.error(request, "You are not authorized to approve this friend request.")
        return redirect('notifications')
    
    from_user = friend_request.from_user
    to_user = friend_request.to_user

    # Check if there is any existing group with both users as members
    existing_groups = ChatGroup.objects.filter(members=from_user).filter(members=to_user)
    if existing_groups.exists():
        messages.info(request, "You are already friends and connected.")
        return redirect('notifications')
    else:
        # Create a new chat group
        new_group = ChatGroup.objects.create()
        new_group.members.add(from_user, to_user)
        new_group.save()

        # Update the friend request status
        friend_request.status = 'accepted'
        friend_request.save()

        messages.success(request, "Friend request approved and now you can chat.")
        return redirect('notifications')

def get_notification(request):
    data = ConnectWith.objects.all().order_by('-published_date')
    jsonData = serializers.serialize('json', data)
    return JsonResponse({'data': jsonData})


# notification1.html is for testing the notificatio by using ajax with reloading in 5 seconds we created the endpoint
# for looping into the notification and checking according to the published date so we passed to that template with
# ajax call to make it then we take their div class in the template then we started to loop it on it by using foreach
# in js then able to get response in template through the ajax


# ===== here we are going to use django channels and the new asgi to make request and receice the answer from the
# server to be able to see the notification in realtime without reloading the page
# @login_required(login_url='login')
# def notifications(request):
#     all_notification = ConnectWith.objects.filter(user=request.user).order_by('-id')
#     async_to_sync(channel_layer.group_send)(
#         'noti_group_name', {
#             'type': 'send_notification',
#             'total_notification': json.dumps({'total': all_notification.count()})
#         }
#     )
#     context = {
#         'all_notification': all_notification
#     }
#     return render(request, 'notifications.html', context)

def enable_two_factor(request):
    user = request.user
    id_user = user.id
    user_log = User.objects.get(id=id_user)
    if user_log.is_two_f_enable:
        user_log.is_two_f_enable = False
        user_log.save()
    else:
        user_log.is_two_f_enable = True
        user_log.save()
    return JsonResponse({"status": user_log.is_two_f_enable})


def get_all_Notification_count(request):
    data = json.loads(request.body)
    logged_user = request.user
    user_id = data['userId_Not']
    notification_id = data['notification_id']
    if logged_user.is_authenticated:
        user_on_log = logged_user.id
        if user_on_log == user_id:
            all_noti = ConnectWith.objects.filter(user_id=user_id, readed_notification=False).count()
        else:
            all_noti = None
    else:
        all_noti = None
    return JsonResponse({'all_notification': all_noti}, safe=False)


def mark_read_notif(request):
    data = request.GET.get('notif')
    noti_id = int(data)
    try:
        notification_connect = ConnectWith.objects.get(id=noti_id)
        notification_connect.readed_notification = True
        notification_connect.save()
    except:
        pass
    return JsonResponse({'response': "done change status"}, safe=False)


@login_required(login_url='login')
def notifications(request):
    for notification in FriendRequest.objects.filter(to_user=request.user).all():
        if notification.readed_request == False:
            notification.readed_request = True
            notification.save()
    all_notification = FriendRequest.objects.filter(to_user=request.user).order_by('-id')
    paginator = Paginator(all_notification, 5)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'all_notification': posts
    }
    return render(request, 'notifications.html', context)

@login_required(login_url='login')
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})

