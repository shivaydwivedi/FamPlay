# What this does is that it takes our models and translates it into the JSON code

from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'code', 'host', 'guest_can_pause',
                  'votes_to_skip', 'created_at')
        

class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')
    

