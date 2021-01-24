from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django_celery_results.models import TaskResult

from .models import Awsenvironment,Ec2,User
from .tools.awsdescriber import AwsDescriber
from .tasks import sync_part_a, sync_part_b, sync_part_c

import ast

# ------------------------------------------------------------------
# index
# ------------------------------------------------------------------

def index(request):
    ec2_count   = Ec2.objects.count()
    user_count  = User.objects.count()
    env_count   = Awsenvironment.objects.count()

    context = {
        'ec2_count': ec2_count,
        'user_count': user_count,
        'env_count' : env_count
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

def data_batch(request):
    task_log_list = TaskResult.objects.all()

    context = {
        'task_log_list': task_log_list
    }
    return render(request, 'data_batch.html', context)

# ------------------------------------------------------------------
# Data batch
# ------------------------------------------------------------------

def sync(request):
    # sent to Broker(redis)
    sync_part_a.delay()
    sync_part_b.delay()
    sync_part_c.delay()

    return HttpResponseRedirect(reverse('app_awsdescribe:data_batch'))