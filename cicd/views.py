from uuid import UUID

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from projects.models import Project
from .cicd import get_cicd_list, get_cicd_host_info_list, create_new_cicd, create_new_cicd_host_info, \
    update_existing_cicd
from .forms import CicdCreateForm, CicdUpdateForm, CicdCreateHostInfoForm
from .jenkins_api import deploy_cicd_environment
from .jenkins_api import start_cicd_environment, stop_cicd_environment, purge_cicd_environment, info_cicd_environment
from .models import Cicd, CicdHostInfo


def cicd(request):
    """

    :param request:
    :return:
    """
    if request.user.is_authenticated:
        cicds = get_cicd_list(request)
        return render(request, 'cicd.html', {'cicds': cicds})
    else:
        return render(request, 'cicd.html')


def cicd_host_info(request):
    """

    :param request:
    :return:
    """
    cicd_his = get_cicd_host_info_list(request)
    return render(request, 'cicd_host_info.html', {'cicd_his': cicd_his})


# def experiment_create(request):
#     """
#
#     :param request:
#     :return:
#     """
#     experimenter = request.user
#     try:
#         project_id = request.session['project_id']
#         project = get_object_or_404(Project, id=project_id)
#     except KeyError:
#         project_qs = Project.objects.filter(project_members=experimenter)
#         if project_qs:
#             project = project_qs[0]
#         else:
#             return redirect('/')
#
#     form = ExperimentCreateForm(request.POST, project=project, experimenter=experimenter)
#
#     if form.is_valid():
#         experiment_uuid = create_new_experiment(request, form)
#         return redirect('experiment_detail', experiment_uuid=experiment_uuid)
#     return render(request, 'experiment_create.html', {'form': form})


def cicd_create(request):
    """

    :param request:
    :return:
    """
    user = request.user
    if request.GET.get('project_uuid'):
        project_uuid = request.GET.get('project_uuid')
    else:
        project_uuid = '00000000-0000-0000-0000-000000000000'

    initial_data = {
        'aerpaw_uuid': project_uuid,
    }
    # q_dict = QueryDict('', mutable=True)
    # q_dict.update(initial_data)

    if request.method == 'POST':
        form = CicdCreateForm(request.POST, initial=initial_data)
        if form.is_valid():
            cicd_uuid = create_new_cicd(request, form)
            # deploy_cicd_environment(cicd_uuid)
            return redirect('cicd_detail', cicd_uuid=cicd_uuid)
        else:
            messages.error(request, "Error")
    else:
        form = CicdCreateForm(request.GET, initial=initial_data)

    return render(request, 'cicd_create.html', {'form': form})


def cicd_host_info_create(request):
    """

    :param request:
    :return:
    """
    user = request.user
    # if request.GET.get('project_uuid'):
    #     project_uuid = request.GET.get('project_uuid')
    # else:
    #     project_uuid = '00000000-0000-0000-0000-000000000000'

    # initial_data = {
    #     'aerpaw_uuid': project_uuid,
    # }
    # q_dict = QueryDict('', mutable=True)
    # q_dict.update(initial_data)

    if request.method == 'POST':
        form = CicdCreateHostInfoForm(request.POST)
        if form.is_valid():
            cicd_hi_uuid = create_new_cicd_host_info(request, form)
            return redirect('cicd_host_info_detail', cicd_host_info_uuid=cicd_hi_uuid)
        else:
            messages.error(request, "Error")
    else:
        form = CicdCreateHostInfoForm(request.GET)

    return render(request, 'cicd_host_info_create.html', {'form': form})


# def experiment_detail(request, experiment_uuid):
#     """
#
#     :param request:
#     :param experiment_uuid:
#     :return:
#     """
#     experiment = get_object_or_404(Experiment, uuid=UUID(str(experiment_uuid)))
#     experiment_reservations = experiment.reservation_of_experiment
#     request.session['experiment_id'] = experiment.id
#
#     status = ''
#     if experiment.stage.upper() == 'DEVELOPMENT':
#         status = query_emulab_instance_status(request, experiment)
#         # the status can be any of following:
#         # 'created', 'provisioning', 'provisioned', 'ready', 'failed', 'teriminating', 'not_started'
#         if status == 'provisioned':
#             status = 'booting'  # for better user understanding
#
#     return render(request, 'experiment_detail.html',
#                   {'experiment': experiment,
#                    'experimenter': experiment.experimenter.all(),
#                    'experiment_status': status,
#                    'reservations': experiment_reservations.all()})


def cicd_detail(request, cicd_uuid):
    """

    :param request:
    :param experiment_uuid:
    :return:
    """
    cicd = get_object_or_404(Cicd, uuid=UUID(str(cicd_uuid)))
    try:
        project = Project.objects.get(uuid=UUID(str(cicd.aerpaw_uuid)))
    except Project.DoesNotExist:
        project = {
            'name': 'UNDEFINED',
            'uuid': cicd.aerpaw_uuid
        }

    if request.GET.get('deploy_cicd'):
        info = deploy_cicd_environment(cicd.uuid)
        if info == -1:
            status = {
                'message': 'ERROR: CI/CD deployment requires a valid project link',
                'timestamp': timezone.now()
            }
        else:
            status = {
                'message': 'Deploying CI/CD as job #{0}'.format(info),
                'timestamp': timezone.now()
            }
    elif request.GET.get('restart_cicd'):
        info = start_cicd_environment(cicd.uuid)
        status = {
            'message': 'Starting CI/CD as job #{0}'.format(info),
            'timestamp': timezone.now()
        }
    elif request.GET.get('stop_cicd'):
        info = stop_cicd_environment(cicd.uuid)
        status = {
            'message': 'Stopping CI/CD as job #{0}'.format(info),
            'timestamp': timezone.now()
        }
    elif request.GET.get('purge_cicd'):
        info = purge_cicd_environment(cicd.uuid)
        status = {
            'message': 'Purging CI/CD as job #{0}'.format(info),
            'timestamp': timezone.now()
        }
        cicd_hi = CicdHostInfo.objects.get(id=cicd.cicd_host_info_id)
        cicd_hi.is_allocated = False
        cicd.delete()
        cicd_hi.save()
        return redirect('cicd')
    else:
        info = info_cicd_environment(cicd.uuid)
        status = {
            'message': info,
            'timestamp': timezone.now()
        }

    return render(request, 'cicd_detail.html',
                  {
                      'cicd': cicd,
                      'project': project,
                      'status': status
                  })


def cicd_host_info_detail(request, cicd_host_info_uuid):
    """

    :param request:
    :param experiment_uuid:
    :return:
    """
    cicd_hi = get_object_or_404(CicdHostInfo, uuid=UUID(str(cicd_host_info_uuid)))

    return render(request, 'cicd_host_info_detail.html',
                  {
                      'cicd_hi': cicd_hi
                  })


def cicd_update(request, cicd_uuid):
    """

    :param request:
    :param experiment_uuid:
    :return:
    """
    cicd = get_object_or_404(Cicd, uuid=UUID(str(cicd_uuid)))
    if request.method == "POST":
        form = CicdUpdateForm(request.POST, instance=cicd)
        if form.is_valid():
            cicd = form.save(commit=False)
            cicd_uuid = update_existing_cicd(request, cicd, form)
            return redirect('cicd_detail', cicd_uuid=str(cicd.uuid))
    else:
        form = CicdUpdateForm(instance=cicd)

    return render(request, 'cicd_update.html',
                  {
                      'form': form,
                      'cicd_uuid': str(cicd.uuid),
                  })


def cicd_delete(request, cicd_uuid):
    """

    :param request:
    :return:
    """
    return render(request, 'cicd.html', {'hello': 'hello'})
