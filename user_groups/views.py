from django.contrib.auth.models import Group
from django.shortcuts import render

from accounts.models import AerpawUser


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
                group_obj = Group.objects.get(name=parse_key[0].replace('_', '-'))
                if str(cur_value) == 'True':
                    user_obj.groups.remove(group_obj)
                else:
                    user_obj.groups.add(group_obj)
                user_obj.save()
    user = request.user
    all_users = AerpawUser.objects.all().exclude(username='admin').order_by('username')
    return render(request, 'user_groups.html', {'user': user, 'all_users': all_users})
