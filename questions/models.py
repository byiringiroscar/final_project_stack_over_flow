from django.db import models
from django.conf import settings
from tinymce.models import HTMLField

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
