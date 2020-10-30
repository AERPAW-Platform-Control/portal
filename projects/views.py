from uuid import UUID

from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProjectCreateForm, ProjectUpdateForm
from .models import Project
from .projects import create_new_project, get_project_list, update_existing_project, delete_existing_project


def projects(request):
    """

    :param request:
    :return:
    """
    projects = get_project_list(request)
    return render(request, 'projects.html', {'projects': projects})


def project_create(request):
    """

    :param request:
    :return:
    """
    if request.method == "POST":
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            project_uuid = create_new_project(request, form)
            return redirect('project_detail', project_uuid=project_uuid)
    else:
        form = ProjectCreateForm()
    return render(request, 'project_create.html', {'form': form})


def project_detail(request, project_uuid):
    """

    :param request:
    :param project_uuid:
    :return:
    """
    project = get_object_or_404(Project, uuid=UUID(str(project_uuid)))
    project_members = project.project_members.order_by('oidc_claim_name')
    project_experiments = project.experiment_of_project
    return render(request, 'project_detail.html', {'project': project, 'project_members': project_members, 'experiments': project_experiments.all()})


def project_update(request, project_uuid):
    """

    :param request:
    :param project_uuid:
    :return:
    """
    project = get_object_or_404(Project, uuid=UUID(str(project_uuid)))
    if request.method == "POST":
        form = ProjectUpdateForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project_uuid = update_existing_project(request, project, form)
            return redirect('project_detail', project_uuid=str(project.uuid))
    else:
        form = ProjectUpdateForm(instance=project)
    return render(request, 'project_update.html',
                  {
                      'form': form, 'project_uuid': str(project_uuid), 'project_name': project.name}
                  )


def project_delete(request, project_uuid):
    """

    :param request:
    :param project_uuid:
    :return:
    """
    project = get_object_or_404(Project, uuid=UUID(str(project_uuid)))
    project_members = project.project_members.order_by('oidc_claim_name')
    if request.method == "POST":
        is_removed = delete_existing_project(request, project)
        if is_removed:
            return redirect('projects')
    return render(request, 'project_delete.html', {'project': project, 'project_members': project_members})
