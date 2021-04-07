from django.db import models
from django.db.models.base import Model
from django_mysql.models import ListCharField

class Awsenvironment(models.Model):
    ae_index = models.AutoField(primary_key=True)
    ae_name = models.CharField(max_length=30)
    ae_env = models.CharField(max_length=10)
    ae_id = models.CharField(max_length=15, unique=True)
    ae_update = models.DateTimeField(auto_now=True)

class AwsenvironmentDetail(models.Model):
    detail_name = models.CharField(max_length=30,primary_key=True)
    detail_use = models.CharField(max_length=30)
    detail_domain = models.CharField(max_length=50)
    detail_account_agency = models.CharField(max_length=20)
    detail_monitoring = models.CharField(max_length=16)
    detail_sre = models.CharField(max_length=20)
    detail_developer = models.CharField(max_length=20)
    detail_product = models.CharField(max_length=30)
    detail_watchman = models.BooleanField()
    detail_vulsan = models.BooleanField()
    detail_os_account_management = ListCharField(
            models.CharField(max_length=16),size=3, max_length=(3 * 17))
    detail_comment = models.TextField()

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
            models.CharField(max_length=50),size=10, max_length=(10 * 51))
    user_groups = ListCharField(
            models.CharField(max_length=20),size=6, max_length=(6 * 21))
    user_passwdLastUesd = models.DateTimeField(null=True)
    user_accesskeyLastUsed = models.DateTimeField(null=True)
    user_isMFAdeviceConfigured = models.BooleanField()
    user_update = models.DateTimeField(auto_now=True)

class Rds(models.Model):
    ae_index = models.ForeignKey(Awsenvironment,on_delete=models.CASCADE)
    rds_cluster_resource_id = models.CharField(max_length=50,primary_key=True)
    rds_cluster_identifier = models.CharField(max_length=50)
    rds_cluster_status = models.CharField(max_length=10)
    rds_cluster_engine = models.CharField(max_length=30)
    rds_cluster_engineVersion = models.CharField(max_length=30)
    rds_cluster_members = ListCharField(
            models.CharField(max_length=20),size=6, max_length=(6 * 21))
    rds_cluster_update = models.DateTimeField(auto_now=True)

class Vpc(models.Model):
    ae_index = models.ForeignKey(Awsenvironment,on_delete=models.CASCADE)
    vpc_id = models.CharField(max_length=50,primary_key=True)
    vpc_cidrblock = models.CharField(max_length=20)
    vpc_tags = models.TextField()
    vpc_isdefault = models.BooleanField()

class Subnet(models.Model):
    ae_index = models.ForeignKey(Awsenvironment, on_delete=models.CASCADE)
    subnet_id = models.CharField(max_length=50, primary_key=True)
    availability_zone = models.CharField(max_length=50)
    availability_zone_id = models.CharField(max_length=50)
    cidr_block = models.CharField(max_length=20)
    vpc_id = models.CharField(max_length=50)
    assign_ipv6 = models.BooleanField()
    subnet_tags = models.TextField()

class Sg(models.Model):
    ae_index = models.ForeignKey(Awsenvironment, on_delete=models.CASCADE)
    vpc_id = models.CharField(max_length=50)
    sg_tags = models.TextField()
    ip_permissions = models.TextField()
    ip_permissions_egress =  models.TextField()
    group_id = models.CharField(max_length=50)
    description  = models.CharField(max_length=255)
    group_name  = models.CharField(max_length=255)

class IpAddress(models.Model):
    ip = models.GenericIPAddressField(primary_key=True, protocol='both')
    description = models.TextField(default='')