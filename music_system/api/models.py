from django.db import models
import string
import random


# function to generate random codes 
def generate_unique_code():
    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k= length))
        if Room.objects.filter(code=code).count() == 0:
            break
    return  code


# Our models here.

class Room(models.Model):
    code = models.CharField(max_length=8, default="", unique=True) #Code to enter the Room
    host = models.CharField(max_length=50, unique=True)#Host to enter their name
    guest_can_pause = models.BooleanField(null=False, default=False)#allows our guests to pause the song
    votes_to_skip = models.IntegerField(null=False, default=1)#members can vote to skip a song
    created_at = models.DateTimeField(auto_now_add=True) #this automatically adds a Date and Time when the Room is created


    

