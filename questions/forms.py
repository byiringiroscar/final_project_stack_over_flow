from django import forms
from questions.models import Questions_stuff, Answer_stuff, Job_work
from django.utils import timezone

now = timezone.now().date()


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
