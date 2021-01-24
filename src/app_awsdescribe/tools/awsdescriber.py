import boto3
import datetime
from botocore.exceptions import ClientError

class AwsDescriber:

    def get_session(self,aws_access_key_id,aws_secret_access_key,aws_account_id):
        # import boto3 client
        client = boto3.client(
            'sts',
            aws_access_key_id = aws_access_key_id,
            aws_secret_access_key = aws_secret_access_key
        )

        # switch to a specific environment
        response = client.assume_role(
            RoleArn = "arn:aws:iam::" + aws_account_id + ":role/awsdescribe_read_only_role",
            RoleSessionName = "awsdescriber",
            DurationSeconds=3600
        )

        # get session in a specific environment
        session = boto3.session.Session(
            aws_access_key_id = response['Credentials']['AccessKeyId'],
            aws_secret_access_key = response['Credentials']['SecretAccessKey'],
            aws_session_token = response['Credentials']['SessionToken'],
            region_name = "ap-northeast-1"
        )

        return session

    def user_describe(self,session):
        client = session.client('iam')
        users = client.list_users()

        user_info_list = []
        for user in users['Users']:
            UserName = user['UserName']
            result = {}

            # get User ID
            result['user_Id'] = user['UserId']

            # get User Name
            result['user_Name'] = UserName

            # get User Policies
            Policies = []
            List_of_Policies =  client.list_user_policies(UserName=UserName)
            if List_of_Policies.get('PolicyNames'):
                result['user_Policies'] = List_of_Policies['PolicyNames']
            else:
                result['user_Policies'] = [None]

            # get User Groups
            Groups=[]
            List_of_Groups =  client.list_groups_for_user(UserName=UserName)
            if List_of_Groups.get('Groups'):
                for Group in List_of_Groups['Groups']:
                    Groups.append(Group['GroupName'])
                result['user_Groups'] = Groups
            else:
                result['user_Groups'] = [None]

            # get User PasswordLastUsed
            Get_user_info = client.get_user(UserName=UserName)
            if Get_user_info['User'].get('PasswordLastUsed'):
                result['user_PasswordLastUsed'] = Get_user_info['User']['PasswordLastUsed']
            else:
                result['user_PasswordLastUsed'] = None

            # get User AccessKeyLastUsed
            get_access_key_list = client.list_access_keys(UserName=UserName)
            if get_access_key_list.get('AccessKeyMetadata') and get_access_key_list['AccessKeyMetadata'][0].get('AccessKeyId'):
                AccessKeyID = get_access_key_list['AccessKeyMetadata'][0]['AccessKeyId']

                get_access_key_last_used = client.get_access_key_last_used(AccessKeyId=AccessKeyID)
                if get_access_key_last_used['AccessKeyLastUsed'].get("LastUsedDate"):
                    result['user_AccessKeyLastUsed'] = get_access_key_last_used['AccessKeyLastUsed']['LastUsedDate']
                else:
                    result['user_AccessKeyLastUsed'] = None
            else:
                result['user_AccessKeyLastUsed'] = None

            # get MFA Device Configure infomation
            List_of_MFA_Devices = client.list_mfa_devices(UserName=UserName)
            if not len(List_of_MFA_Devices['MFADevices']):
                result['user_isMFADeviceConfigured'] = False   
            else:
                result['user_isMFADeviceConfigured'] = True

            # append all infomaion of user
            user_info_list.append(result)
        
        return user_info_list

    def ec2_describe(self,session):
        client = session.client('ec2', region_name='ap-northeast-1')
        ec2 = client.describe_instances()

        ec2_info_list = []
        for reservations in ec2['Reservations']:
            for instance in reservations['Instances']:
                result = {}

                if instance["State"]["Name"] == "terminated":
                    continue

                # get instance state
                result["ec2_state"] = instance["State"]["Name"]

                # get instance id
                result["ec2_id"] = instance["InstanceId"]

                # get instance tags
                if instance.get("Tags"):
                    tags = {}
                    for ec2_tag_list in instance["Tags"]:
                        tags[ec2_tag_list["Key"]] = ec2_tag_list["Value"]
                    result["ec2_tags"] = tags
                else:
                    result["ec2_tags"] = "None"

                # get instance network infomation
                floating_ip = []
                private_ip = []
                for ec2_nic in instance["NetworkInterfaces"]:
                    if ec2_nic.get("Association"):
                        floating_ip.append(ec2_nic["Association"]["PublicIp"])
                    private_ip.append(ec2_nic["PrivateIpAddress"])

                if not floating_ip:
                    floating_ip.append(None)

                result["ec2_fip"] = floating_ip
                result["ec2_ip"] = private_ip
                ec2_info_list.append(result)

        return ec2_info_list
