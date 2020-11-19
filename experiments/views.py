from django.shortcuts import render

# Create your views here.

from uuid import UUID

from django.shortcuts import render, redirect, get_object_or_404

from .forms import ExperimentCreateForm, ExperimentUpdateForm
from .models import Experiment
from .experiments import *
from experiments.models import Project


def experiments(request):
    """

    :param request:
    :return:
    """

    # aerpaw nodes:
    experiments = get_experiment_list(request)

    # emulab cloud:
    emulab_experiments = get_emulab_instances(request)
    return render(request, 'experiments.html', {'experiments': emulab_experiments})


def experiment_create(request):
    """

    :param request:
    :return:
    """
    experimenter=request.user
    try:
        project_id=request.session['project_id']
        project=get_object_or_404(Project, id=project_id)
    except KeyError:
        project_qs=Project.objects.filter(project_members=experimenter)
        if project_qs:
            project=project_qs[0]
        else:
            return redirect('/')
        
    form = ExperimentCreateForm(request.POST,project=project,experimenter=experimenter)
    if form.is_valid():
        experiment_uuid = create_new_experiment(request, form)
        return redirect('experiment_detail', experiment_uuid=experiment_uuid)
    return render(request, 'experiment_create.html', {'form': form})


def experiment_detail(request, experiment_uuid):
    """

    :param request:
    :param experiment_uuid:
    :return:
    """
    experiment = get_object_or_404(Experiment, uuid=UUID(str(experiment_uuid)))
    experiment_reservations = experiment.reservation_of_experiment
    request.session['experiment_id'] = experiment.id
    return render(request, 'experiment_detail.html',
    {'experiment': experiment, 'experimenter':experiment.experimenter.all(), 'reservations': experiment_reservations.all()})


def experiment_update(request, experiment_uuid):
    """

    :param request:
    :param experiment_uuid:
    :return:
    """
    experiment = get_object_or_404(Experiment, uuid=UUID(str(experiment_uuid)))
    if request.method == "POST":
        form = ExperimentUpdateForm(request.POST, instance=experiment)
        if form.is_valid():
            experiment = form.save(commit=False)
            experiment_uuid = update_existing_experiment(request, experiment, form)
            return redirect('experiment_detail', experiment_uuid=str(experiment.uuid))
    else:
        form = ExperimentUpdateForm(instance=experiment)
    return render(request, 'experiment_update.html',
                  {
                      'form': form, 'experiment_uuid': str(experiment_uuid), 'experiment_name': experiment.name}
                  )


def experiment_delete(request, experiment_uuid):
    """

    :param request:
    :param experiment_uuid:
    :return:
    """
    experiment = get_object_or_404(Experiment, uuid=UUID(str(experiment_uuid)))
    experiment_reservations = experiment.reservation_of_experiment
    if request.method == "POST":
        is_removed = delete_existing_experiment(request, experiment)
        if is_removed:
            return redirect('experiments')
    return render(request, 'experiment_delete.html', {'experiment': experiment, 'experimenter':experiment.experimenter.all(), 'experiment_reservations': experiment_reservations})
