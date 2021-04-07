from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django_celery_results.models import TaskResult
from django.views.decorators.csrf import csrf_exempt # https://docs.djangoproject.com/en/dev/ref/csrf/

from .models import Awsenvironment,AwsenvironmentDetail,Ec2,Subnet,User,Rds,Vpc,Sg,IpAddress
from .tools.awsdescriber import AwsDescriber
from .tasks import sync_part_a, sync_part_b, sync_part_c

import ast

# ------------------------------------------------------------------
# index
# ------------------------------------------------------------------

def index(request):
    ec2_count           = Ec2.objects.count()
    user_count          = User.objects.count()
    env_count           = Awsenvironment.objects.count()
    rds_cluster_count   = Rds.objects.count()
    vpc_count           = Vpc.objects.count()
    subnet_count        = Subnet.objects.count()
    sg_count            = Sg.objects.count()

    context = {
        'ec2_count': ec2_count,
        'user_count': user_count,
        'env_count' : env_count,
        'rds_cluster_count': rds_cluster_count,
        'vpc_count': vpc_count,
        'subnet_count': subnet_count,
        'sg_count': sg_count
    }

    return render(request,'index.html', context)

# ------------------------------------------------------------------
# side menu
# ------------------------------------------------------------------

def environment_list(request):
    environment_info_list = Awsenvironment.objects.all()
    context = {
        'environment_info_list': environment_info_list
    }
    return render(request, 'environment_list.html', context)

def ec2_list(request):
    ec2_list = Ec2.objects.all()

    # convert from str to dic
    for ec2_info in ec2_list:
        if "None" not in ec2_info.ec2_tags:
            ec2_info.ec2_tags = ast.literal_eval(ec2_info.ec2_tags)

    context = {
        'ec2_list': ec2_list
    }
    return render(request, 'ec2_list.html', context)

def user_list(request):
    user_list = User.objects.all()

    context = {
        'user_list': user_list
    }
    return render(request, 'user_list.html', context)

def rds_cluster_list(request):
    rds_cluster_list = Rds.objects.all()

    context = {
        'rds_cluster_list': rds_cluster_list
    }
    return render(request, 'rds_cluster_list.html', context)

def data_batch(request):
    task_log_list = TaskResult.objects.all()

    context = {
        'task_log_list': task_log_list
    }
    return render(request, 'data_batch.html', context)

def vpc_list(request):

    vpc_list = Vpc.objects.all()

    # convert from str to dic
    for vpc_info in vpc_list:
        if "None" not in vpc_info.vpc_tags:
            vpc_info.vpc_tags = ast.literal_eval(vpc_info.vpc_tags)

    context = {
        'vpc_list': vpc_list
    }

    return render(request, 'vpc_list.html',context)

def subnet_list(request):

    subnet_list = Subnet.objects.all()

    # convert from str to dic
    for subnet_info in subnet_list:
        if "None" not in subnet_info.subnet_tags:
            subnet_info.subnet_tags = ast.literal_eval(subnet_info.subnet_tags)

    context = {
        'subnet_list': subnet_list
    }

    return render(request, 'subnet_list.html',context)


def sg_list(request):
    sg_list = Sg.objects.all()

    # convert from str to dic / sg_tasg
    for sg_info in sg_list:
        if "None" not in sg_info.sg_tags:
            sg_info.sg_tags = ast.literal_eval(sg_info.sg_tags)

    # convert from str to dic / ip_permissions
    for sg_info in sg_list:
        if "None" not in sg_info.ip_permissions:
            sg_info.ip_permissions = ast.literal_eval(sg_info.ip_permissions)

    # convert from str to dic / ip_permissions_egress
    for sg_info in sg_list:
        if "None" not in sg_info.ip_permissions_egress:
            sg_info.ip_permissions_egress = ast.literal_eval(sg_info.ip_permissions_egress)

    context = {
        'sg_list' : sg_list
    }

    return render(request, 'sg_list.html', context)

def ip_list(request):
    ip_list = IpAddress.objects.all()

    context = {
        'ip_list' : ip_list
    }

    return render(request, 'ip_list.html', context)


# ------------------------------------------------------------------
# Data Batch
# ------------------------------------------------------------------

def sync(request):
    # sent to Broker(redis)
    sync_part_a.delay()
    sync_part_b.delay()
    sync_part_c.delay()

    return HttpResponseRedirect(reverse('app_awsdescribe:data_batch'))

# ------------------------------------------------------------------
# CRUD
# ------------------------------------------------------------------

@csrf_exempt
def insert_account_info(request):
    # required basic information
    ae_name = request.POST.get('ae_name')
    ae_ids = request.POST.getlist('ae_id[]')
    ae_envs = request.POST.getlist('ae_env[]')

    for ae_id,ae_env in zip(ae_ids,ae_envs):
        if not ae_id or not ae_env:
            continue

        set_query = Awsenvironment(
            ae_name = ae_name,
            ae_env  = ae_env,
            ae_id   = ae_id
        )
        set_query.save()

    # detail information
    details = {
        'detail_name' : ae_name,
        'detail_use' : request.POST.get('detail_use'),
        'detail_domain' : request.POST.get('detail_domain'),
        'detail_account_agency' : request.POST.get('detail_account_agency'),
        'detail_monitoring' : request.POST.get('detail_monitoring'),
        'detail_sre' : request.POST.get('detail_sre'),
        'detail_developer' : request.POST.get('detail_developer'),
        'detail_product' : request.POST.get('detail_product'),
        'detail_os_account_management' : request.POST.getlist('detail_os_account_management[]'),
        'detail_watchman' : request.POST.get('detail_watchman'),
        'detail_vulsan' : request.POST.get('detail_vulsan'),
        'detail_comment' : request.POST.get('detail_comment')
    }

    for k in details:
        if not details[k]:
            if k == 'detail_watchman' or k == 'detail_vulsan' :
                details[k] = False
                continue
            details[k] = 'none'

        for index in range(len(details['detail_os_account_management'])) :
            if not details['detail_os_account_management'][index]:
                details['detail_os_account_management'][index] = 'none'

    set_query = AwsenvironmentDetail(
        detail_name = details['detail_name'],
        detail_use = details['detail_use'],
        detail_domain = details['detail_domain'],
        detail_account_agency = details['detail_account_agency'],
        detail_monitoring = details['detail_monitoring'],
        detail_sre = details['detail_sre'],
        detail_developer = details['detail_developer'],
        detail_product = details['detail_product'],
        detail_watchman = details['detail_watchman'],
        detail_vulsan = details['detail_vulsan'],
        detail_os_account_management = details['detail_os_account_management'],
        detail_comment = details['detail_comment']
    )
    set_query.save()

    return HttpResponseRedirect(reverse('app_awsdescribe:environment_list'))

@csrf_exempt
def update_account_info(request):
    # required basic information
    ae_name = request.POST.get('ae_name')
    ae_ids = request.POST.getlist('ae_id[]')
    ae_envs = request.POST.getlist('ae_env[]')

    for ae_id,ae_env in zip(ae_ids,ae_envs):
        if not ae_id or not ae_env:
            continue

        # 同じProductでIDの追加がある時は、新しく追加するように。
        if not Awsenvironment.objects.filter(ae_id=ae_id):
            set_query = Awsenvironment(
                ae_name = ae_name,
                ae_env  = ae_env,
                ae_id   = ae_id
            )
            set_query.save()

        ae = Awsenvironment.objects.filter(ae_id=ae_id).get()
        ae.ae_name = ae_name
        ae.ae_env = ae_env
        ae.ae_id = ae_id
        ae.save()

    # Formから既存のIDが削除された時、DBにあるレコードを削除
    ae_ids_from_db = Awsenvironment.objects.filter(ae_name=ae_name).values("ae_id")
    for row in ae_ids_from_db:
        ae_id_from_db = row['ae_id']
        if ae_id_from_db not in ae_ids:
             Awsenvironment.objects.filter(ae_id=ae_id_from_db).delete()

    # detail information
    details = {
        'detail_name' : ae_name,
        'detail_use' : request.POST.get('detail_use'),
        'detail_domain' : request.POST.get('detail_domain'),
        'detail_account_agency' : request.POST.get('detail_account_agency'),
        'detail_monitoring' : request.POST.get('detail_monitoring'),
        'detail_sre' : request.POST.get('detail_sre'),
        'detail_developer' : request.POST.get('detail_developer'),
        'detail_product' : request.POST.get('detail_product'),
        'detail_os_account_management' : request.POST.getlist('detail_os_account_management[]'),
        'detail_watchman' : request.POST.get('detail_watchman'),
        'detail_vulsan' : request.POST.get('detail_vulsan'),
        'detail_comment' : request.POST.get('detail_comment')
    }

    for k in details:
        if not details[k]:
            if k == 'detail_watchman' or k == 'detail_vulsan' :
                details[k] = False

        for index in range(len(details['detail_os_account_management'])) :
            if not details['detail_os_account_management'][index]:
                details['detail_os_account_management'][index] = 'none'

    aed = AwsenvironmentDetail.objects.filter(detail_name=ae_name).get()
    aed.detail_name = details['detail_name']
    aed.detail_use = details['detail_use']
    aed.detail_domain = details['detail_domain']
    aed.detail_account_agency = details['detail_account_agency']
    aed.detail_monitoring = details['detail_monitoring']
    aed.detail_sre = details['detail_sre']
    aed.detail_developer = details['detail_developer']
    aed.detail_product = details['detail_product']
    aed.detail_watchman = details['detail_watchman']
    aed.detail_vulsan = details['detail_vulsan']
    aed.detail_os_account_management = details['detail_os_account_management']
    aed.detail_comment = details['detail_comment']
    aed.save()

    return HttpResponseRedirect(reverse('app_awsdescribe:environment_list'))

@csrf_exempt
def delete_account_info(request):
    ae_name = request.POST.get('ae_name')

    if Awsenvironment.objects.filter(ae_name=ae_name):
        Awsenvironment.objects.filter(ae_name=ae_name).delete()

    if AwsenvironmentDetail.objects.filter(detail_name=ae_name):
        AwsenvironmentDetail.objects.filter(detail_name=ae_name).delete()

    return HttpResponseRedirect(reverse('app_awsdescribe:environment_list'))

@csrf_exempt
def get_account_detail(request):
    detail_name = request.POST.get('detail_name')
    get_detail_data = AwsenvironmentDetail.objects.filter(detail_name=detail_name).values()[0]

    return JsonResponse(get_detail_data)

@csrf_exempt
def get_account_information_for_modify(request):
    ae_name = request.POST.get('ae_name')

    basic = Awsenvironment.objects.filter(ae_name=ae_name).values()
    detail = AwsenvironmentDetail.objects.filter(detail_name=ae_name).values()[0]

    combine_result = {}
    for k,v in detail.items():
        if k == 'detail_name':
            continue
        combine_result[k]=v

    combine_result['ae_name'] = ae_name
    for row in basic:
        if row['ae_env'] == 'prd' or row['ae_env'] == 'all':
            combine_result['ae_env_prd_all'] = row['ae_env']
            combine_result['ae_id_prd_all'] = row['ae_id']
        elif row['ae_env'] == 'stg':
            combine_result['ae_env_stg'] = row['ae_env']
            combine_result['ae_id_stg'] = row['ae_id']
        elif row['ae_env'] == 'dev':
            combine_result['ae_env_dev'] = row['ae_env']
            combine_result['ae_id_dev'] = row['ae_id']

    return JsonResponse(combine_result)