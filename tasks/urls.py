from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('',views.TaskListView.as_view(),name='task_list'),
    # path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/new/', views.CreateTaskView.as_view(), name='task_new'),
    path('task/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('task/<int:pk>/remove/', views.TaskDeleteView.as_view(), name='task_remove'),
    path('task/<int:pk>/finish/', views.task_finish, name='task_finish'),
    path('history/', views.TaskHistoryView.as_view(), name='task_history'),
    path('topic/', views.TopicManageView.as_view(), name='topic_manage'),
    path('topic/<int:pk>/remove', views.TopicDeleteView.as_view(), name='topic_delete'),
]
