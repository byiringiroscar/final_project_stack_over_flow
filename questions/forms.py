from django import forms
from questions.models import Questions_stuff, Answer_stuff


class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions_stuff
        fields = ['title', 'detail', 'body', 'tag', ]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer_stuff
        fields = ['name', 'message', ]
