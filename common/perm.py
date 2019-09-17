
from functools import wraps
from contest.models import Contest
from django.http import HttpResponseRedirect, JsonResponse, Http404

def view_permission_required(func):

    def decorator(func):
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            pk = kwargs.get('pk')
            contest = Contest.objects.filter(pk=pk).first()
            if pk and contest:
                if request.user.has_perm('ojuser.view_groupprofile', contest.group) and contest.ended() >= 0:
                    return func(request, *args, **kwargs)
                elif request.user.has_perm('ojuser.change_groupprofile', contest.group):
                    return func(request, *args, **kwargs)
            raise Http404()
        return returned_wrapper
    if not func:
        def foo(func):
            return decorator(func)
        return foo
    return decorator(func)

def change_permission_required(func):

    def decorator(func):
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            pk = kwargs.get('pk')
            contest = Contest.objects.filter(pk=pk).first()
            if pk and contest and request.user.has_perm('ojuser.change_groupprofile', contest.group):
                return func(request, *args, **kwargs)
            raise Http404()
        return returned_wrapper
    if not func:
        def foo(func):
            return decorator(func)
        return foo
    return decorator(func)

