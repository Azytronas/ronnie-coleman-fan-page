import json
from channels.generic.websocket import WebsocketConsumer
from channels.auth import UserLazyObject
from asgiref.sync import async_to_sync
from .models import Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model()


def normalize(message):
    return "[{at}] {by}: {text}".format(at=message.timestamp, by=message.sent_by.username, text=message.content)


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        new_participant = self.scope['user']

        if Chat.objects.filter(name=self.room_name).count() == 0:
            new_chat = Chat.objects.create(name=self.room_name)
        else:
            chat = Chat.objects.get(name=self.room_name)
        if not isinstance(new_participant, UserLazyObject):
            chat.in_chat.add(new_participant)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        leaver = self.scope['user']
        curr_chat = Chat.objects.get(name=self.room_name)
        if not isinstance(leaver, UserLazyObject):
            curr_chat.in_chat.remove(leaver)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type_of_call = text_data_json['type']
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': type_of_call,
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        curr_chat = Chat.objects.get(name=self.room_name)
        author = self.scope['user']
        if isinstance(author, UserLazyObject):
            author = User.objects.get(username='Anonymous')
        new_message = Message.objects.create(sent_by=author, content=message, sent_in=curr_chat)
        norm_message = normalize(new_message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': norm_message
        }))

    def load_log(self, event):
        curr_chat = Chat.objects.get(name=self.room_name)
        self.send(text_data=json.dumps({
            'message': 'Welcome to the {} chat room. Loading log...\n'.format(self.room_name)
        }))
        for message in curr_chat.messages.all():
            log = normalize(message)
            self.send(text_data=json.dumps({
                'message': log
            }))
