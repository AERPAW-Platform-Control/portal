from uuid import UUID, uuid4

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

# from cicd.models import Cicd
from .forms import ProjectCreateForm, ProjectUpdateForm, ProjectUpdateMembersForm, ProjectUpdateOwnersForm, \
    ProjectJoinForm, JOIN_CHOICES
from .models import Project
from usercomms.models import Usercomms
from .projects import create_new_project, get_project_list, update_existing_project, delete_existing_project
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

PI_message = "Please email the admin to become a PI first!"


@login_required
def projects(request):
    """

    :param request:
    :return:
    """
    my_projects, other_projects = get_project_list(request)
    return render(request, 'projects.html', {'my_projects': my_projects, 'other_projects': other_projects})


def project_create(request):
    """

    :param request:
    :return:
    """
    if request.method == "POST":
        form = ProjectCreateForm(request.POST,
                                 initial={'project_members': request.user, 'project_owners': request.user})
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
    # get project
    project = get_object_or_404(Project, uuid=UUID(str(project_uuid)))
    # set user permissions
    is_pc = (project.project_creator == request.user)
    is_po = (request.user in project.project_owners.all())
    is_pm = (request.user in project.project_members.all())
    # RM_CICD
    # try:
    #     cicd = Cicd.objects.get(aerpaw_uuid=str(project.uuid))
    # except Cicd.DoesNotExist as err:
    #     print(err)
    #     cicd = None
    # cicd = get_object_or_404(Cicd, aerpaw_uuid=str(project.uuid))
    request.session['project_id'] = project.id
    project_members = project.project_members.order_by('username')
    project_owners = project.project_owners.order_by('username')
    project_experiments = project.experiment_of_project
    # TODO: update ci/cd links
    return render(request, 'project_detail.html',
                  {'project': project, 'project_members': project_members, 'project_owners': project_owners,
                   'is_pc': is_pc, 'is_po': is_po, 'is_pm': is_pm,
                   'experiments': project_experiments.all()})


def project_join(request, project_uuid):
    """

    :param request:
    :param project_uuid:
    :return:
    """
    # get project
    project = get_object_or_404(Project, uuid=UUID(str(project_uuid)))
    if request.method == 'GET':
        form = ProjectJoinForm()
    else:
        form = ProjectJoinForm(request.POST)
        if form.is_valid():
            email_uuid = uuid4()
            reference_url = 'https://' + str(request.get_host()) + '/projects/' + str(project_uuid)
            member_type = str(dict(JOIN_CHOICES)[form.data['member_type']])
            reference_note = 'Join project ' + str(project.name) + ' as ' + member_type
            subject = '[AERPAW] Request to join project ' + str(project.name) + ' as ' + member_type
            email_sender = settings.EMAIL_HOST_USER
            email_body = 'FROM: ' + request.user.display_name + \
                         '\r\nREQUEST: ' + reference_note + \
                         '\r\n\r\nURL: ' + reference_url + \
                         '\r\n\r\nMESSAGE: ' + form.cleaned_data['message']
            body = 'FROM: ' + request.user.display_name + \
                   '\r\nREQUEST: Join project ' + str(project.name) + ' as ' + member_type + \
                   '\r\n\r\nMESSAGE: ' + form.cleaned_data['message']
            receivers = [project.project_creator]
            receivers_email = [project.project_creator.email]
            project_owners = project.project_owners.order_by('username')
            for po in project_owners:
                receivers.append(po)
                receivers_email.append(po.email)
            receivers = list(set(receivers))
            receivers_email = list(set(receivers_email))
            try:
                send_mail(subject, email_body, email_sender, receivers_email)
                # Sender
                created_by = request.user
                created_date = timezone.now()
                uc = Usercomms( uuid=email_uuid, subject=subject, body=body, sender=created_by,
                                reference_url=None, reference_note=None, reference_user=created_by,
                                created_by=created_by, created_date=created_date)
                uc.save()
                for rc in receivers:
                    uc.receivers.add(rc)
                uc.save()
                # Receivers
                for rc in receivers:
                    uc = Usercomms(uuid=email_uuid, subject=subject, body=email_body, sender=created_by,
                                   reference_url=reference_url, reference_note=reference_note, reference_user=rc,
                                   created_by=created_by, created_date=created_date)
                    uc.save()
                    for inner_rc in receivers:
                        uc.receivers.add(inner_rc)
                    uc.save()

                messages.info(request, 'Success! Request to join project: ' + str(project.name) + ' has been sent')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('projects')

    return render(request, "project_join.html", {'form': form, 'project': project})


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
                  {'form': form, 'project_uuid': str(project_uuid), 'project_name': project.name}
                  )


def project_update_members(request, project_uuid):
    """

    :param request:
    :param project_uuid:
    :return:
    """
    project = get_object_or_404(Project, uuid=UUID(str(project_uuid)))

    if request.method == "POST":
        form = ProjectUpdateMembersForm(request.POST, instance=project)
        if form.is_valid():
            project_members = form.cleaned_data.get('project_members')
            project.project_members.through.objects.filter(project_id=project.id).delete()
            for member in project_members:
                project.project_members.add(member)
            project.modified_by = request.user
            project.modified_date = timezone.now()
            project.save()
            return redirect('project_detail', project_uuid=str(project.uuid))
    else:
        form = ProjectUpdateMembersForm(instance=project)
    return render(request, 'project_update_members.html',
                  {
                      'form': form, 'project_uuid': str(project_uuid), 'project_name': project.name}
                  )


def project_update_owners(request, project_uuid):
    """

    :param request:
    :param project_uuid:
    :return:
    """
    project = get_object_or_404(Project, uuid=UUID(str(project_uuid)))

    if request.method == "POST":
        form = ProjectUpdateOwnersForm(request.POST, instance=project)
        if form.is_valid():
            project_owners = form.cleaned_data.get('project_owners')
            project.project_owners.through.objects.filter(project_id=project.id).delete()
            for member in project_owners:
                project.project_owners.add(member)
            project.modified_by = request.user
            project.modified_date = timezone.now()
            project.save()
            return redirect('project_detail', project_uuid=str(project.uuid))
    else:
        form = ProjectUpdateOwnersForm(instance=project)
    return render(request, 'project_update_owners.html',
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
