from django.shortcuts import get_object_or_404
from authentication.models import Profile
from questions.models import *


def extras(request):
    user = request.user
    all_question = Questions_stuff.objects.filter().all().order_by('-publish_date')
    all_badge_request = Badge.objects.filter(badge_approved=False).order_by('-published_date')
    final_tag = []
    tag_count = []
    final_tag_count = []
    if all_question.exists():
        all_tag = []
        for question in all_question:
            stack_tag = question.tag.lower().split(',')
            all_tag.append(stack_tag)
        for all_tag in all_tag:
            for tag in all_tag:
                tag_count.append(tag)
                final_tag.append(tag)
        final_tag = list(set(final_tag))
        for final_count in final_tag:
            tag_count_number = tag_count.count(final_count)
            final_tag_count.append(tag_count_number)


    else:
        final_tag = []

    if user.is_authenticated:
        user = request.user
        profile_user = get_object_or_404(Profile, user=user)
        # to address notification from police request
    else:
        profile_user = None
        user = None

    return {
        'profile': profile_user,
        'user': user,
        'all_tag': zip(final_tag[:6], final_tag_count[:6]),
        'all_tag_more': zip(final_tag[6:], final_tag_count[6:]),
        'all_badge_request': all_badge_request,
        'all_badge_request_count': all_badge_request.count()


    }
