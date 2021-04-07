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
            List_of_inline_Policies =  client.list_user_policies(UserName=UserName)
            if List_of_inline_Policies.get('PolicyNames'):
                for List_of_inline_Policy in List_of_inline_Policies['PolicyNames']:
                    Policies.append(List_of_inline_Policy)

            List_of_managed_Policies = client.list_attached_user_policies(UserName=UserName)
            for AttachedPolicy in List_of_managed_Policies['AttachedPolicies']:
                if AttachedPolicy.get('PolicyName') and AttachedPolicy['PolicyName'] != "goa-sec_protection":
                    Policies.append(AttachedPolicy['PolicyName'])

            if Policies :
                result['user_Policies'] = Policies
            else :
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
        client = session.client('ec2')
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

    def rds_describe(self,session):
        client = session.client('rds', region_name='ap-northeast-1')
        rds_cluster = client.describe_db_clusters()

        rds_info_list = []
        for cluster_info in rds_cluster['DBClusters']:
            result = {}

            result['rds_cluster_resource_id'] = cluster_info['DbClusterResourceId']

            result['rds_cluster_identifier'] = cluster_info['DBClusterIdentifier']

            result['rds_cluster_status'] = cluster_info['Status']

            result['rds_cluster_engine'] = cluster_info['Engine']

            result['rds_cluster_engineVersion'] = cluster_info['EngineVersion']

            rds_instance_members = []
            for member in cluster_info['DBClusterMembers']:
                rds_instance_members.append(member['DBInstanceIdentifier'])
            result['rds_instance_mebers'] = rds_instance_members

            rds_info_list.append(result)

        return rds_info_list

    def vpc_describe(self,session):
        client = session.client('ec2')
        vpc = client.describe_vpcs()

        vpc_info_list = []

        for vpc in vpc['Vpcs']:
            result = {}

            result['VpcId'] = vpc['VpcId']
            result['CidrBlock'] = vpc['CidrBlock']
            result['IsDefault'] = vpc['IsDefault']

            if vpc.get("Tags"):                                         # {'Tags': [{'Key': 'Name', 'Value': 'point-habits-cloud9'}]}
                tags = {}
                for vpc_tag_list in vpc["Tags"]:                        # vpc["Tags"]  = [{'Key': 'Name', 'Value': 'point-habits-cloud9'}]
                    tags[vpc_tag_list["Key"]] = vpc_tag_list["Value"]   # vpc_tag_list = {'Key': 'Name', 'Value': 'point-habits-cloud9'}
                result["Tags"] = tags                                   # tags         = {'Name': 'point-habits-cloud9'}
            else:
                result["Tags"] = "None"

            vpc_info_list.append(result)

        return vpc_info_list

    def subnet_describe(self, session):
        client = session.client('ec2')
        subnet = client.describe_subnets()

        subnet_info_list = []

        for s in subnet['Subnets']:
            result = {}

            result['SubnetId'] = s['SubnetId']
            result['AvailabilityZone'] = s['AvailabilityZone']
            result['AvailabilityZoneId'] = s['AvailabilityZoneId']
            result['CidrBlock'] = s['CidrBlock']
            result['VpcId'] = s['VpcId']
            result['AssignIpv6AddressOnCreation'] = s['AssignIpv6AddressOnCreation']

            if s.get("Tags"):
                tags = {}
                for tag_list in s["Tags"]:
                    tags[tag_list["Key"]] = tag_list["Value"]
                result["Tags"] = tags
            else:
                result["Tags"] = "None"

            subnet_info_list.append(result)

        return subnet_info_list

    def sg_describe(self, session):
        client = session.client('ec2')
        sg = client.describe_security_groups()

        sg_info_list = []
        ip_list = []

        for s in sg['SecurityGroups']:
            result = {}
            result["VpcId"] = s["VpcId"]
            result["GroupId"] = s["GroupId"]
            result["Description"] = s["Description"]
            result["GroupName"] = s["GroupName"]

            if s.get("IpPermissions"):
                ip_permission = {}
                for permission in s["IpPermissions"]:
                    ip_permission["FromPort"] = permission["FromPort"] if permission["IpProtocol"] != '-1' else '-1'
                    ip_permission["ToPort"] = permission["ToPort"] if permission["IpProtocol"] != '-1' else '-1'
                    if permission.get("IpRanges"):
                        ip_raw_list = list(map(lambda p: p["CidrIp"], permission["IpRanges"]))
                        ip_permission["IpRanges"] = ",".join(ip_raw_list)
                        ip_list.extend(ip_raw_list)
                    if permission.get("Ipv6Ranges"):
                        ip_raw_list = list(map(lambda p: p["CidrIpv6"], permission["Ipv6Ranges"]))
                        ip_permission["Ipv6Ranges"] = ",".join(ip_raw_list)
                        ip_list.extend(ip_raw_list)
                result["IpPermissions"] = ip_permission

            if s.get("IpPermissionsEgress"):
                ip_permission_egress = {}
                for permission in s["IpPermissionsEgress"]:
                    ip_permission_egress["FromPort"] = permission["FromPort"] if permission["IpProtocol"] != '-1' else '-1'
                    ip_permission_egress["ToPort"] = permission["ToPort"] if permission["IpProtocol"] != '-1' else '-1'
                    if permission.get("IpRanges"):
                        ip_raw_list = list(map(lambda p: p["CidrIp"], permission["IpRanges"]))
                        ip_permission_egress["IpRanges"] = ",".join(ip_raw_list)
                        ip_list.extend(ip_raw_list)
                    if permission.get("Ipv6Ranges"):
                        ip_raw_list = list(map(lambda p: p["CidrIpv6"], permission["Ipv6Ranges"]))
                        ip_permission_egress["Ipv6Ranges"] = ",".join(ip_raw_list)
                        ip_list.extend(ip_raw_list)
                result["IpPermissionsEgress"] = ip_permission_egress
            # TODO: PrefixListIds, UserIdGroupPairsは一旦無視

            if s.get("Tags"):
                tags = {}
                for tag_list in s["Tags"]:
                    tags[tag_list["Key"]] = tag_list["Value"]
                result["Tags"] = tags
            else:
                result["Tags"] = "None"

            sg_info_list.append(result)
            unique_ip_list = list(set(ip_list))

        return sg_info_list, unique_ip_list
