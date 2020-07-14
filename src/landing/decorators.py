from django.http import HttpResponse



def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            print("Allowed roles: " + " ,".join(allowed_roles))
            group = None

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if request.user.groups.exists():
                group = request.user.groups.get().name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)

            else:
                return HttpResponse("<h1>You are not authorised to view this page</h1>")

        return wrapper_func
    return decorator
