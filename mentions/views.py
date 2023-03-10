from django.shortcuts import render


def clean_and_change_to_set(req):
    names = req.replace(",", " ").strip().split(" ")
    names = ["@" + name.strip('@') for name in names]
    return set(names)


def mentions_manager(request):
    if request.method == "POST":
        users = clean_and_change_to_set(request.POST.get('users-list', ''))
        users_to_add = clean_and_change_to_set(request.POST.get('add-users', ''))
        users_to_remove = clean_and_change_to_set(request.POST.get('remove-users', ''))

        users.update(users_to_add)
        users.difference_update(users_to_remove)

        if request.POST.get('sorting') == 'on':
            users = sorted(users)

        return render(request, 'mentions/manager.html', {'new_users_list': users})
    
    else:
        return render(request, 'mentions/manager.html', {}) 
