import uuid

from django.utils import timezone

from .models import Project, AerpawUser


def create_new_project(request, form):
    """

    :param request:
    :param form:
    :return:
    """
    project = Project()
    project.uuid = uuid.uuid4()
    project.name = form.data.getlist('name')[0]
    try:
        project.description = form.data.getlist('description')[0]
    except ValueError as e:
        print(e)
        project.description = None
    project.principal_investigator = AerpawUser.objects.get(
        id=int(form.data.getlist('principal_investigator')[0])
    )

    project.created_by = request.user
    project.created_date = timezone.now()
    project.modified_by = project.created_by
    project.modified_date = project.created_date
    project.save()
    project_member_id_list = form.data.getlist('project_members')
    update_project_members(project, project_member_id_list)
    project.save()
    return str(project.uuid)


def update_project_members(project, project_member_id_list):
    """

    :param project:
    :param project_member_id_list:
    :return:
    """
    # clear current project membership
    project.project_members.clear()
    # add members from project_member_id_update_list
    for member_id in project_member_id_list:
        project_member = AerpawUser.objects.get(id=int(member_id))
        project.project_members.add(project_member)
    project.save()
    # add principal_investigator to project_members if not already there
    if project.principal_investigator not in project.project_members.all():
        project.project_members.add(project.principal_investigator)
        project.save()


def update_existing_project(request, project, form):
    """
    Create new AERPAW Project

    :param request:
    :param form:
    :return:
    """
    project.modified_by = request.user
    project.modified_date = timezone.now()
    project.save()
    project_member_id_list = form.data.getlist('project_members')
    update_project_members(project, project_member_id_list)
    project.save()
    return str(project.uuid)


def delete_existing_project(request, project):
    """

    :param request:
    :param project:
    :return:
    """
    try:
        project.delete()
        return True
    except Exception as e:
        print(e)
    return False


def get_project_list(request):
    """

    :param request:
    :return:
    """
    if request.user.is_superuser:
        projects = Project.objects.filter(created_date__lte=timezone.now()).order_by('name')
    else:
        projects = request.user.projects.order_by('name')
    return projects
