from celery.decorators import task
from .models import Awsenvironment,User,Ec2
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
    # TODO: get value from AWS Parameter Store or other
    aws_access_key_id       = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key   = os.environ['AWS_SECRET_ACCESS_KEY']

    # get account id from DB
    range_start, range_end = get_range(part_name)
    aws_env_list = Awsenvironment.objects.filter(ae_index__range=(range_start,range_end)).values('ae_id')

    # get all data
    ec2_all   = Ec2.objects.all()
    user_all  = User.objects.all()

    # insert ec2_data into database
    for ret in aws_env_list:
        aws_account_id = ret['ae_id']

        # Create AwsDescriber instance
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
