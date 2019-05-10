from django.db import models
from django.utils import timezone
import misaka
from django.contrib.auth import get_user_model
User = get_user_model()

class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=False,)
    name = models.CharField(max_length=255, unique=True, verbose_name='Topic')
    # slug = models.SlugField(allow_unicode=True, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4
    LEVEL_ITEMS = (
        (P1,'Critical'),
        (P2,'Important'),
        (P3,'Normal'),
        (P4,'Low'),
    )
    STATUS_ITEMS = (
        (P1,'Done'),
        (P2,'Waiting'),
        (P3,'Doing'),
    )
    user = models.ForeignKey(User, on_delete=False,)
    topic = models.ForeignKey('Topic',on_delete=False,verbose_name='Topic', null =True)
    title = models.CharField(max_length=200,verbose_name='Title')
    desc = models.CharField(max_length=1024, blank=True, verbose_name="Desc")
    priority = models.PositiveIntegerField(default=P2, choices=LEVEL_ITEMS, verbose_name='Level')
    status = models.PositiveIntegerField(default=P3, choices=STATUS_ITEMS, verbose_name='Status')
    create_time = models.DateTimeField(default=timezone.now,verbose_name='Create')
    expect_time = models.DateTimeField(blank=True,null=True)
    # try do remained function in views
    # time_remained = models.DateTimeField(blank=True,null= True)
    finished_time = models.DateTimeField(blank=True,null=True)

    def finish(self):
        self.finished_time = timezone.now()
        self.status = self.P1
        self.save()
    def __str__(self):
        return self.title
