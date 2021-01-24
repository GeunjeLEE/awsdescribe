from django.db import models
from django_mysql.models import ListCharField

class Awsenvironment(models.Model):
    ae_index = models.AutoField(primary_key=True)
    ae_name = models.CharField(max_length=30)
    ae_env = models.CharField(max_length=10)
    ae_id = models.CharField(max_length=15)
    ae_update = models.DateTimeField(auto_now=True)

class Ec2(models.Model):
    ae_index = models.ForeignKey(Awsenvironment,on_delete=models.CASCADE)
    ec2_id = models.CharField(max_length=30,primary_key=True)
    ec2_state = models.CharField(max_length=10)
    ec2_privateip = ListCharField(
            models.CharField(max_length=10),size=6, max_length=(6 * 11))
    ec2_publicip = ListCharField(
            models.CharField(max_length=10),size=6, max_length=(6 * 11))
    ec2_tags = models.TextField()
    ec2_update = models.DateTimeField(auto_now=True)

class User(models.Model):
    ae_index = models.ForeignKey(Awsenvironment,on_delete=models.CASCADE)
    user_id = models.CharField(max_length=50,primary_key=True)
    user_name = models.CharField(max_length=50)
    user_policies = ListCharField(
            models.CharField(max_length=10),size=6, max_length=(6 * 11))
    user_groups = ListCharField(
            models.CharField(max_length=20),size=6, max_length=(6 * 21))
    user_passwdLastUesd = models.DateTimeField(null=True)
    user_accesskeyLastUsed = models.DateTimeField(null=True)
    user_isMFAdeviceConfigured = models.BooleanField()
    user_update = models.DateTimeField(auto_now=True)