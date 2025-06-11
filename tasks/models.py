from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    VISIBILITY_CHOICES = [
        ('private', 'Private'),
        ('internal', 'Internal'),
        ('public', 'Public'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='private')
    members = models.ManyToManyField(User, related_name='tasks_boards', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class List(models.Model):
    board = models.ForeignKey(Board, related_name='lists', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.board.name})'


class Card(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    list = models.ForeignKey('List', on_delete=models.CASCADE, related_name='cards')
    order = models.PositiveIntegerField(default=0)
    members = models.ManyToManyField(User, related_name='cards', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_written')  # тот, кто оставил
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_about', null=True, blank=True)  # если комментарий "про" другого юзера (необязательно)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.card.title}'

 
