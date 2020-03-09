from django.db import models
from django.contrib.auth.models import User

class CustomUser(User):
    twitter = models.URLField(max_length = 200)
    linkedin = models.URLField(max_length = 200) 
    blog = models.URLField(max_length = 200)
    



