from django.db import models
from django.conf import settings
from tinymce.models import HTMLField
from phonenumber_field.modelfields import PhoneNumberField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.sessions.models import Session

import json

User = settings.AUTH_USER_MODEL


# Create your models here.

class Questions_stuff(models.Model):
    title = models.CharField(max_length=100)
    detail = models.TextField(default='')
    body = HTMLField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed = models.PositiveIntegerField()
    tag = models.CharField(max_length=200)
    email_notify = models.BooleanField(default=False)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner.full_name} --- {self.title}'

    def tags_as_list(self):
        return self.tag.split(',')

    def get_count_answer(self):
        id_question = self.id
        ans = Answer_stuff.objects.filter(question__id=id_question)
        if ans.exists():

            final_count = ans.count()
        else:
            final_count = 0
        return final_count

    class Meta:
        verbose_name_plural = 'Question'


class Answer_stuff(models.Model):
    question = models.ForeignKey(Questions_stuff, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    message = models.TextField()
    published_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question.title} ------ {self.name}"

    class Meta:
        verbose_name_plural = 'Answer'


#
class Job_work(models.Model):
    job_owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title_developer = models.CharField(max_length=250)
    title_task = models.CharField(max_length=250)
    amount_range_start = models.PositiveIntegerField()
    amount_range_end = models.PositiveIntegerField()
    tags = models.CharField(max_length=250)
    job_description = models.TextField()
    experience = models.CharField(max_length=250)
    job_type = models.CharField(max_length=250)
    enable_remote = models.BooleanField()
    country_location = models.CharField(max_length=250)
    viewed = models.PositiveIntegerField(default=0)
    job_hired = models.BooleanField(default=False)
    published_date = models.DateField(auto_now_add=True)
    expire_date = models.DateField()

    def __str__(self):
        return f'{self.title_developer} --- {self.expire_date}'

    def tags_as_list(self):
        skills = self.tags
        skills = skills[:-1]
        skills = skills.split(",")
        final_skills = ''
        for skills in skills:
            new_skills = skills.split(":")
            new_skills = new_skills[1][1:-2]
            final_skills += f'{new_skills},'
        final_skills = final_skills[:-1]
        return final_skills.split(',')

    class Meta:
        verbose_name_plural = 'Job'


class Applied_job(models.Model):
    job = models.ForeignKey(Job_work, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = PhoneNumberField()
    residence = models.CharField(max_length=100)
    current_company = models.CharField(max_length=100, null=True, blank=True)
    resume = models.FileField()
    linkedin_url = models.URLField()
    biography = models.TextField()
    rejected_apply = models.BooleanField(default=False)
    hired_apply = models.BooleanField(default=False)
    interview = models.BooleanField(default=False)
    applied_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.job.title_developer} --- {self.full_name}'

    class Meta:
        verbose_name_plural = 'Job Applied'

    def get_progress_percent(self):
        profile_percent = 50
        interview = self.interview
        hired_apply = self.hired_apply
        if hired_apply:
            profile_percent = 100
        if interview:
            profile_percent = profile_percent + 35
        if interview and hired_apply:
            profile_percent = 100
        return profile_percent


class InterviewApplied(models.Model):
    applied_person = models.ForeignKey(Applied_job, on_delete=models.CASCADE)
    interview_link = models.URLField()
    interview_date = models.DateTimeField()
    sent_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Interview List'

    def __str__(self):
        return f'{self.applied_person.full_name} --- {self.interview_date}'


class Badge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    position_name = models.CharField(max_length=100)
    supporting_document = models.FileField()
    badge_approved = models.BooleanField(default=False)
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.full_name}'

    @property
    def get_interview_status(self):
        interview_status = self.interviewbadge_set.all()
        return interview_status


class InterviewBadge(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    interview_link = models.URLField()
    interview_date = models.DateTimeField()
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.badge.user.full_name}'


class ConnectWith(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    subject = models.CharField(max_length=250)
    body = models.TextField()
    readed_notification = models.BooleanField(default=False)
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ----- {self.subject}'

    # def save(self, *args, **kwargs):
    #     super(ConnectWith, self).save(*args, **kwargs)
    #     channel_layer = get_channel_layer()
    #     # check logged_in user by taking the session

    #     notif = self.body
    #     user_id_server = self.user.id
    #     name_user = self.name
    #     subject_user = self.subject
    #     date_published_user = self.published_date
    #     notification_id = self.id
    #     notification_status = self.readed_notification
    #     async_to_sync(channel_layer.group_send)(
    #         'noti_group_name', {  # this is the group name created in consumer
    #             'type': 'send_notification', # this is method we are going to create under consumer
    #             'value': json.dumps({'notif': notif,
    #                                  'user_id_server': user_id_server,
    #                                  'name_user': name_user,
    #                                  'subject_user': subject_user,
    #                                  'date_published_user': str(date_published_user),
    #                                  'notification_id': notification_id,
    #                                  'notification_status': notification_status

    #                                  })
    #         }
    #     )


class ConnectStatus(models.Model):
    connect_with = models.ForeignKey(ConnectWith, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_from')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_to')
    subject = models.CharField(max_length=250, default='please can you connect with me')
    body = models.TextField(default='')
    status = models.CharField(max_length=10, default='pending') # pending, accepted, rejected
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.from_user.username} to {self.to_user.username}'
