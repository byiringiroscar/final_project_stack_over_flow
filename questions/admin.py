from django.contrib import admin
from questions.models import Questions_stuff, Answer_stuff

# Register your models here.

admin.site.register(Questions_stuff)
admin.site.register(Answer_stuff)
