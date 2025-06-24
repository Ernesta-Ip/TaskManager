from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Board(models.Model):
    VISIBILITY_CHOICES = [
        ('private', 'Private'),
        ('internal', 'Internal'),
        ('public', 'Public'),
    ]
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards_created')
    name = models.CharField(max_length=255)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='private')
    member_emails = models.TextField(blank=True, help_text="Comma-separated list of member emails")
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)
    is_archived = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    def get_member_email_list(self):
        return [email.strip() for email in self.member_emails.split(",") if email.strip()]

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_written')
    text = models.TextField()  
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_about', null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True) 
    def __str__(self):
        return f'Comment by {self.author.username} on {self.card.title}'
    def save(self, *args, **kwargs):
        # if current comment was edited
        if self.pk is not None and self.has_changed():
            self.edited_at = timezone.now()
        super().save(*args, **kwargs)
    def has_changed(self):
        if not self.pk:
            return False
        old_value = type(self).objects.get(pk=self.pk).__dict__['text']
        return self.text != old_value

 
