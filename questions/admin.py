from django.contrib import admin
from questions.models import Questions_stuff, Answer_stuff, Job_work, Applied_job, InterviewApplied, Badge, InterviewBadge, ConnectWith, ChatGroup, FriendRequest

# Register your models here.

admin.site.register(Questions_stuff)
admin.site.register(Answer_stuff)
admin.site.register(Job_work)
admin.site.register(Applied_job)
admin.site.register(InterviewApplied)
admin.site.register(Badge)
admin.site.register(InterviewBadge)
admin.site.register(ConnectWith)
admin.site.register(ChatGroup)
admin.site.register(FriendRequest)


