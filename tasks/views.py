from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from tasks.models import Task, Topic
from django.utils import timezone
from .forms import TaskForm, TopicForm
from django.db.models import Q

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class TaskListView(ListView,LoginRequiredMixin):

    login_url = 'accounts:login'
    model = Task
    template_name = 'tasks/task_list.html'
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user).filter(Q(status=Task.P2) | Q(status=Task.P3)).order_by('-create_time')


class CreateTaskView(LoginRequiredMixin,CreateView):

    login_url = 'accounts:login'
    success_url = reverse_lazy('tasks:task_list')
    form_class = TaskForm

    model = Task
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin,UpdateView):

    login_url = 'accounts:login'
    success_url = reverse_lazy('tasks:task_list')
    form_class = TaskForm
    model = Task

class TaskDeleteView(LoginRequiredMixin,DeleteView):

    login_url = 'accounts:login'
    model = Task
    success_url = reverse_lazy('tasks:task_list')

class TaskHistoryView(LoginRequiredMixin,ListView):

    model = Task
    login_url = 'accounts:login'
    template_name = 'tasks/task_history.html'
    paginate_by = 10
    ordering = '-finished_time'
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user).filter(status=Task.P1).order_by('-finished_time')

    def get_ordering(self):
        self.order = self.request.GET.get('order', 'asc')
        selected_ordering = self.request.GET.get('ordering', 'finished_time')
        if self.order == "desc":
            selected_ordering = "-" + selected_ordering
        return selected_ordering

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['current_order'] = self.get_ordering()
        context['order'] = self.order
        return context

class TopicManageView(LoginRequiredMixin,CreateView):
    login_url = 'accounts:login'
    form_class = TopicForm
    success_url = 'tasks:topic_manage'
    template_name = 'tasks/topic_manage.html'
    model = Topic

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.filter(user=user).order_by('-id')
        return context


class TopicDeleteView(LoginRequiredMixin,DeleteView):
    login_url = 'accounts:login'
    model = Topic
    success_url = reverse_lazy('tasks:topic_manage')

# class TaskHistoryView(LoginRequiredMixin,ListView):
#     login_url = 'accounts/login/'
#     mode = Task

#######################################
## Functions that require a pk match ##
#######################################

@login_required
def task_finish(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.finish()
    return redirect('tasks:task_list')



# class CarList(ListView):
#     model = Car
#     paginate_by = 30
#
#     ordering = 'car_id_internal'
#     def get_ordering(self):
#         self.order = self.request.GET.get('order', 'asc')
#         selected_ordering = self.request.GET.get('ordering', 'car_id_internal')
#         if self.order == "desc":
#             selected_ordering = "-" + selected_ordering
#         return selected_ordering
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(CarList, self).get_context_data(*args, **kwargs)
#         context['current_order'] = self.get_ordering()
#         context['order'] = self.order
#         return context
#
#     def get_queryset(self):
#         all_unfinished = self.request.GET.get('display', 'all')
#         new_context = Task.objects.all().order_by('-finished_time')
#         return new_context
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['orderby'] = self.request.GET.get('display', 'all')
#         return context
