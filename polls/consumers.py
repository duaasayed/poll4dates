from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import Message, Guest, Poll, TimeSlot
from accounts.models import User
from django.core import serializers

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['guid']
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
    
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        sender_type = text_data_json['sender_type']

        if sender_type == 'user':
            sender = User.objects.get(guid=sender)
        else:
            sender = Guest.objects.get(guid=sender)

        poll = Poll.objects.get(guid=self.room_name)
        Message.objects.create(poll=poll, content_sender=sender, content=message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    def chat_message(self, event):
        message = event['message']
        sender = serializers.serialize('json', [event['sender']])
        self.send(text_data=json.dumps({'message': message, 'sender': sender}))



class VotingConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['guid']
        self.room_group_name = f"poll-{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()


    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        timeslot = TimeSlot.objects.select_related('poll').get(pk=text_data_json['timeslot_id'])
        guest_id = text_data_json['guest_id']
        vote_method = text_data_json['vote_method']

        guest = Guest.objects.get(guid=guest_id)
        vote, created = timeslot.votes.get_or_create(guest=guest)
        if not created:
            vote.delete()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': 'update_votes', 
                'timeslot': timeslot.id,
                'max_vote': timeslot.poll.max_vote,
                'votes_count': timeslot.votes_count,
                'voter_id': guest_id,
                'vote_method': vote_method,
                'waiting_guests': timeslot.poll.guests_waiting,
                'voters': timeslot.poll.guests_voted
            }
        )
        
    def update_votes(self, event):
        waiting_guests = serializers.serialize('json', event['waiting_guests'])
        voters = serializers.serialize('json', event['voters'])
        
        self.send(text_data=json.dumps({
            'timeslot': event['timeslot'],
            'max_vote': event['max_vote'],
            'votes_count': event['votes_count'],
            'voter_id': event['voter_id'],
            'vote_method': event['vote_method'],
            'waiting_guests': waiting_guests,
            'voters': voters
        }))
