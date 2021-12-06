from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    in_chat = models.ManyToManyField(User, related_name="in_chat", blank=True)
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name


class Message(models.Model):
    sent_by = models.ForeignKey(User, related_name="sent", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.TimeField(auto_now_add=True)
    sent_in = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)

    def __str__(self):
        return self.content
