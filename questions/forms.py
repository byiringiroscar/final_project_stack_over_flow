from django import forms
from questions.models import Questions_stuff, Answer_stuff, Job_work, Applied_job, InterviewApplied, Badge, \
    InterviewBadge
from django.utils import timezone

now = timezone.now().date()
now_interview = timezone.now()


class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions_stuff
        fields = ['title', 'detail', 'body', 'tag', ]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer_stuff
        fields = ['name', 'message', ]


class JobForm(forms.ModelForm):
    enable_remote = forms.BooleanField(required=True)

    class Meta:
        model = Job_work
        fields = ['title_developer', 'title_task', 'amount_range_start', 'amount_range_end', 'tags', 'job_description',
                  'job_type', 'experience', 'expire_date', 'enable_remote', 'country_location', ]

    def clean_amount_range_end(self):
        minimum_salary = self.cleaned_data['amount_range_start']
        amount_range_end = self.cleaned_data['amount_range_end']
        if minimum_salary > amount_range_end:
            raise forms.ValidationError("minimum salary can't be greater than maximum salary")
        return amount_range_end

    def clean_expire_date(self):
        expire_date = self.cleaned_data['expire_date']
        if expire_date < now:
            raise forms.ValidationError("Expire date must be great than today's date")
        return expire_date


class ApplyJobForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Applied_job
        fields = ['full_name', 'email', 'phone_number', 'residence', 'current_company', 'resume', 'linkedin_url',
                  'biography', ]


class InterviewAppliedForm(forms.ModelForm):
    class Meta:
        model = InterviewApplied
        fields = ['interview_link', 'interview_date', ]

    def clean_interview_date(self):
        interview_date = self.cleaned_data['interview_date']
        if interview_date <= now_interview:
            raise forms.ValidationError("please date must be greater than today's date")
        return interview_date


class InterviewBadgeForm(forms.ModelForm):
    class Meta:
        model = InterviewBadge
        fields = ['interview_link', 'interview_date', ]

    def clean_interview_date(self):
        interview_date = self.cleaned_data['interview_date']
        if interview_date <= now_interview:
            raise forms.ValidationError("please date must be greater than today's date")
        return interview_date


class BadgeForm(forms.ModelForm):
    class Meta:
        model = Badge
        fields = ['company_name', 'position_name', 'supporting_document', ]
