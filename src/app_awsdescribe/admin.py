from django.contrib import admin

from .models import Awsenvironment,Ec2,User

admin.site.register(Awsenvironment)
admin.site.register(Ec2)
admin.site.register(User)