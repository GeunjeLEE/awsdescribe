from django.contrib import admin

from .models import Awsenvironment,Ec2,User,Rds,Vpc,AwsenvironmentDetail

admin.site.register(Awsenvironment)
admin.site.register(Ec2)
admin.site.register(User)
admin.site.register(Rds)
admin.site.register(Vpc)
admin.site.register(AwsenvironmentDetail)