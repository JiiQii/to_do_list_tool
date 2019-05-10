from django import forms
from .models import Task, Topic

from bootstrap_datepicker_plus import DateTimePickerInput

class TaskForm(forms.ModelForm):

    topic  = forms.ModelChoiceField(required=True, queryset=Topic.objects.all(),empty_label=None, label='Topic')
    class Meta:
        model = Task
        fields = ['topic','title','desc','priority','status','expect_time',]
        widgets = {
            'expect_time': DateTimePickerInput(),
        }

        # def save(self):
        #     if form.is_vaild():
        #         task = form.save(commit=False)
        #         task.user = request.user
        #         task.save()

class TopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = {'name'}
