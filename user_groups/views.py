from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render

from accounts.models import AerpawUser, AerpawRoleRequest


@login_required
def user_groups(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        for key in request.POST.keys():
            if not key == 'csrfmiddlewaretoken':
                cur_value = request.POST.get(key)
                parse_key = key.rsplit('_', 1)
                user_obj = AerpawUser.objects.get(id=int(parse_key[1]))
                group_obj = Group.objects.get(name=parse_key[0])
                if str(cur_value) == 'True':
                    user_obj.groups.remove(group_obj)
                else:
                    user_obj.groups.add(group_obj)
                user_obj.save()
    user = request.user
    all_users = AerpawUser.objects.all().exclude(username='admin').order_by('username')
    return render(request, 'user_groups.html', {'user': user, 'all_users': all_users})


@login_required
def user_requests(request):
    """

    :param request:
    :return:
    """
    if request.method == "POST":
        for key in request.POST.keys():
            if not key == 'csrfmiddlewaretoken':
                parse_key = key.rsplit('_', 1)
                if parse_key[0] != 'notes':
                    role = parse_key[0]
                    role_request = AerpawRoleRequest.objects.get(id=int(parse_key[1]))
                    notes = request.POST.get('notes_' + str(parse_key[1]))
                    if request.POST.get(key) == 'Approve':
                        is_approved = True
                    else:
                        is_approved = False
        # get user_obj
        user_obj = AerpawUser.objects.get(id=int(role_request.requested_by_id))
        group_obj = Group.objects.get(name=str(role))
        if str(is_approved) == 'True':
            user_obj.groups.add(group_obj)
        else:
            user_obj.groups.remove(group_obj)
        user_obj.save()
        role_request.notes = notes
        role_request.is_approved = is_approved
        role_request.is_completed = True
        role_request.save()
        print(notes, is_approved, role_request.uuid, role)

    open_u_reqs = AerpawRoleRequest.objects.filter(is_completed=False).order_by('created_date').reverse()
    closed_u_reqs = AerpawRoleRequest.objects.filter(is_completed=True).order_by('created_date').reverse()
    return render(request, 'user_requests.html', {'ou_reqs': open_u_reqs, 'cu_reqs': closed_u_reqs})