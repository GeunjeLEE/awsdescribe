from django.db import models
from celery.decorators import task
from .models import Awsenvironment,User,Ec2,Rds,Vpc,Subnet, Sg, IpAddress
from .tools.awsdescriber import AwsDescriber
import os

@task(name="sync_part_a")
def sync_part_a():
    main("a")

@task(name="sync_part_b")
def sync_part_b():
    main("b")

@task(name="sync_part_c")
def sync_part_c():
    main("c")

def main(part_name):
    # get credentials info from html form
    aws_access_key_id       = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key   = os.environ['AWS_SECRET_ACCESS_KEY']

    # get account id from DB
    range_start, range_end = get_range(part_name)
    aws_env_list = Awsenvironment.objects.filter(ae_index__range=(range_start,range_end)).values('ae_id')

    # insert ec2_data into database
    for ret in aws_env_list:
        aws_account_id = ret['ae_id']

        # Create AwsDescriber Class instance
        AD = AwsDescriber()

        # get session
        session = AD.get_session(aws_access_key_id,aws_secret_access_key,aws_account_id)

        # get the Awsenvironment ID for mapping information the between info(ec2, user, etc..) and aws Environment
        # Select * from Awsenvironment where ae_id=aws_account_id
        Awsenvironment_info = Awsenvironment.objects.filter(ae_id=aws_account_id).values()
        ae_index = Awsenvironment_info[0]['ae_index']

        # get ec2 information using AwsDescriber
        ec2_info_list = AD.ec2_describe(session)
        # sync
        job_Ec2(ec2_info_list,ae_index)

        # get user information using AwsDescriber
        user_info_list = AD.user_describe(session)
        # sync
        job_User(user_info_list,ae_index)

        # get Rds Cluster information using AwsDescriber
        rds_cludster_info_list = AD.rds_describe(session)
        # sync
        job_Rds(rds_cludster_info_list,ae_index)

        # get Vpc information using AwsDescriber
        vpc_info_list = AD.vpc_describe(session)
        # sync
        job_Vpc(vpc_info_list,ae_index)

        # get Subnet information using AwsDescriber
        subnet_info_list = AD.subnet_describe(session)
        # sync
        job_Subnet(subnet_info_list,ae_index)

        # get Sg information & ip list using AwsDescriber
        sg_info_list, ip_list = AD.sg_describe(session)
        #sync
        job_Sg(sg_info_list,ae_index)
        job_Ip_list(ip_list)


def get_range(part_name):
    Awsenvironment_all_count = Awsenvironment.objects.count()
    Awsenvironment_all_object = Awsenvironment.objects.all()

    start   = 0
    end     = Awsenvironment_all_count - 1
    point1  = int((start + end) / 3)
    point2  = int((start + end) / 3 * 2)

    range_a = (
                Awsenvironment_all_object[start].ae_index,
                Awsenvironment_all_object[point1].ae_index,
            )

    range_b = (
                Awsenvironment_all_object[point1+1].ae_index,
                Awsenvironment_all_object[point2].ae_index,
            )

    range_c = (
                Awsenvironment_all_object[point2+1].ae_index,
                Awsenvironment_all_object[end].ae_index,
            )

    if part_name == 'a':
        return range_a      # start ~ point1

    if part_name == 'b':
        return range_b      # point1 ~ point2

    if part_name == 'c':
        return range_c      # point2 ~ end


def job_Ec2(ec2_info_list,ae_index):
    # insert into Ec2 table
    for info in ec2_info_list:
        ec2_tags                    = info['ec2_tags']
        ec2_id                      = info['ec2_id']
        ec2_fip                     = info['ec2_fip']
        ec2_ip                      = info['ec2_ip']
        ec2_state                   = info['ec2_state']

        query = Ec2(ae_index        = Awsenvironment(ae_index=ae_index),
                    ec2_id          = ec2_id,
                    ec2_state       = ec2_state,
                    ec2_publicip    = ec2_fip,
                    ec2_privateip   = ec2_ip,
                    ec2_tags        = ec2_tags
                )
        query.save()

    ec2_id_list_from_db = Ec2.objects.filter(ae_index=ae_index).values("ec2_id")

    result_db = []
    for ec2_id_from_db in ec2_id_list_from_db:
        result_db.append(ec2_id_from_db['ec2_id'])

    result_info = []
    for ec2_info in ec2_info_list:
        result_info.append(ec2_info['ec2_id'])

    for ec2_id_from_result_db in result_db:
        if ec2_id_from_result_db not in result_info:
            Ec2.objects.filter(ec2_id=ec2_id_from_result_db).delete()


def job_User(user_info_list,ae_index):
    # insert into User table
    for info in user_info_list:
        user_id                     = info['user_Id']
        user_name                   = info['user_Name']
        user_policies               = info['user_Policies']
        user_groups                 = info['user_Groups']
        user_passwdLastUesd         = info['user_PasswordLastUsed']
        user_accesskeyLastUsed      = info['user_AccessKeyLastUsed']
        user_isMFAdeviceConfigured  = info['user_isMFADeviceConfigured']

        query = User(ae_index                   = Awsenvironment(ae_index=ae_index),
                     user_id                    = user_id,
                     user_name                  = user_name,
                     user_policies              = user_policies,
                     user_groups                = user_groups,
                     user_passwdLastUesd        = user_passwdLastUesd,
                     user_accesskeyLastUsed     = user_accesskeyLastUsed,
                     user_isMFAdeviceConfigured = user_isMFAdeviceConfigured
                )
        query.save()

    user_id_list_from_db = User.objects.filter(ae_index=ae_index).values("user_id")

    result_db = []
    for user_id_from_db in user_id_list_from_db:
        result_db.append(user_id_from_db['user_id'])

    result_info = []
    for user_info in user_info_list:
        result_info.append(user_info['user_Id'])

    for user_id_from_result_db in result_db:
        if user_id_from_result_db not in result_info:
            User.objects.filter(user_id=user_id_from_result_db).delete()

def job_Rds(rds_cludster_info_list,ae_index):

    for info in rds_cludster_info_list:
        rds_cluster_resource_id     = info['rds_cluster_resource_id']
        rds_cluster_identifier      = info['rds_cluster_identifier']
        rds_cluster_status          = info['rds_cluster_status']
        rds_cluster_engine          = info['rds_cluster_engine']
        rds_cluster_engineVersion   = info['rds_cluster_engineVersion']
        rds_cluster_members         = info['rds_instance_mebers']

        query = Rds(ae_index                   = Awsenvironment(ae_index=ae_index),
                     rds_cluster_resource_id   = rds_cluster_resource_id,
                     rds_cluster_identifier    = rds_cluster_identifier,
                     rds_cluster_status        = rds_cluster_status,
                     rds_cluster_engine        = rds_cluster_engine,
                     rds_cluster_engineVersion = rds_cluster_engineVersion,
                     rds_cluster_members       = rds_cluster_members
                )
        query.save()

    rds_cluster_id_list_from_db = Rds.objects.filter(ae_index=ae_index).values("rds_cluster_resource_id")

    result_db = []
    for rds_cluster_id_from_db in rds_cluster_id_list_from_db:
        result_db.append(rds_cluster_id_from_db['rds_cluster_resource_id'])

    result_info = []
    for rds_cludster_info in rds_cludster_info_list:
        result_info.append(rds_cludster_info['rds_cluster_resource_id'])

    for rds_cluster_id_from_result_db in result_db:
        if rds_cluster_id_from_result_db not in result_info:
            Rds.objects.filter(rds_cluster_resource_id=rds_cluster_id_from_result_db).delete()


def job_Vpc(vpc_info_list,ae_index):
    # insert into Ec2 table

    for info in vpc_info_list:
        vpc_tags                    = info['Tags']
        vpc_id                      = info['VpcId']
        vpc_cidrblock               = info['CidrBlock']
        vpc_isdefault               = info['IsDefault']

        query = Vpc(ae_index        = Awsenvironment(ae_index=ae_index),
                    vpc_id          = vpc_id,
                    vpc_cidrblock   = vpc_cidrblock,
                    vpc_tags        = vpc_tags,
                    vpc_isdefault   = vpc_isdefault
                )
        query.save()

    vpc_id_list_from_db = Vpc.objects.filter(ae_index=ae_index).values("vpc_id")

    result_db = []

    for vpc_id_from_db in vpc_id_list_from_db:
        result_db.append(vpc_id_from_db['vpc_id'])

    result_info = []
    for vpc_info in vpc_info_list:
        result_info.append(vpc_info['VpcId'])

    for vpc_id_from_result_db in result_db:
        if vpc_id_from_result_db not in result_info:
            Vpc.objects.filter(vpc_id=vpc_id_from_result_db).delete()


def job_Subnet(subnet_info_list, ae_index):
    for info in subnet_info_list:
        subnet_id = info['SubnetId']
        availability_zone = info['AvailabilityZone']
        availability_zone_id = info['AvailabilityZoneId']
        cidr_block = info['CidrBlock']
        vpc_id = info['VpcId']
        assign_ipv6 = info['AssignIpv6AddressOnCreation']
        subnet_tags = info['Tags']

        query = Subnet(
            ae_index = Awsenvironment(ae_index=ae_index),
            subnet_id = subnet_id,
            availability_zone = availability_zone,
            availability_zone_id = availability_zone_id,
            cidr_block = cidr_block,
            vpc_id = vpc_id,
            assign_ipv6 = assign_ipv6,
            subnet_tags = subnet_tags
        )

        query.save()

    subnet_id_list_from_db = Subnet.objects.filter(ae_index=ae_index).values("subnet_id")

    result_db = []

    for subnet_id_from_db in subnet_id_list_from_db:
        result_db.append(subnet_id_from_db['subnet_id'])

    result_info = []
    for subnet_info in subnet_info_list:
        result_info.append(subnet_info['SubnetId'])

    for subnet_id_from_result_db in result_db:
        if subnet_id_from_result_db not in result_info:
            Subnet.objects.filter(subnet_id=subnet_id_from_result_db).delete()

def job_Sg(sg_info_list, ae_index):

    for info in sg_info_list:
        VpcId = info["VpcId"]
        GroupId = info["GroupId"] 
        Description = info["Description"]
        GroupName = info["GroupName"]
        IpPermissions = info["IpPermissions"]
        IpPermissionsEgress = info["IpPermissionsEgress"]
        Tags = info["Tags"]

        query = Sg(
                ae_index                    = Awsenvironment(ae_index=ae_index),
                vpc_id                      = VpcId,
                sg_tags                     = Tags,
                ip_permissions              = IpPermissions,
                ip_permissions_egress       = IpPermissionsEgress,
                group_id                    = GroupId,
                description                 = Description,
                group_name                  = GroupName
        )
        query.save()

        sg_id_list_from_db = Sg.objects.filter(ae_index=ae_index).values("group_id")

        result_db = []
        for sg_id_from_db in sg_id_list_from_db:
            result_db.append(sg_id_from_db["group_id"])

        result_info = []
        for sg_id in sg_info_list:
            result_info.append(sg_id["GroupId"])

        for sg_id_from_result_db in result_db:
            if sg_id_from_result_db not in result_info:
                Sg.objects.filter(sg_id=sg_id_from_result_db).delete()


def job_Ip_list(ip_list):

    for ip in ip_list:

        query = IpAddress(
            ip = ip
        )
        query.save()

# TODO: 次回はここから