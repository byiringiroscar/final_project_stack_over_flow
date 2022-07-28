from django.db import models
from django.conf import settings
from tinymce.models import HTMLField
from phonenumber_field.modelfields import PhoneNumberField

User = settings.AUTH_USER_MODEL


# Create your models here.

class Questions_stuff(models.Model):
    title = models.CharField(max_length=100)
    detail = models.TextField(default='')
    body = HTMLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed = models.PositiveIntegerField()
    tag = models.CharField(max_length=200)
    email_notify = models.BooleanField(default=False)
    whatsapp_notify = models.BooleanField(default=False)
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
    published_date = models.DateField(auto_now_add=True)
    expire_date = models.DateField()

    def __str__(self):
        return f'{self.title_developer} --- {self.expire_date}'

    def save(self, *args, **kwargs):
        skills = self.tags
        skills = skills[:-1]
        skills = skills.split(",")
        final_skills = ''
        for skills in skills:
            new_skills = skills.split(":")
            new_skills = new_skills[1][1:-2]
            final_skills += f'{new_skills},'
        final_skills = final_skills[:-1]
        self.tags = final_skills
        super().save(*args, **kwargs)

    def tags_as_list(self):
        return self.tags.split(',')

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
    hired = models.BooleanField(default=False)
    interview = models.BooleanField(default=False)
    applied_date = models.DateField()

    def __str__(self):
        return f'{self.job.title_developer} --- {self.full_name}'

    class Meta:
        verbose_name_plural = 'Job Applied'
