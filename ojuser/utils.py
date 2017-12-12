from __future__ import unicode_literals

from functools import wraps
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from guardian.compat import get_user_model
from guardian.utils import get_group_obj_perms_model
from guardian.utils import get_user_obj_perms_model
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from .models import GroupProfile

def get_users_with_perm(obj, perm, with_superusers=False,
                         with_group_users=True):
    """
    Returns queryset of all ``User`` objects with *specified* object permissions for
    the given ``obj``.

    :param obj: persisted Django's ``Model`` instance

    :param perm: The permission codename which the result users should have

    :param with_superusers: Default: ``False``. If set to ``True`` result would
      contain all superusers.

    :param with_group_users: Default: ``True``. If set to ``False`` result would
      **not** contain those users who have only group permissions for given
      ``obj``.

    """
    ctype = ContentType.objects.get_for_model(obj)

    # It's much easier without attached perms so we do it first if that is
    # the case
    user_model = get_user_obj_perms_model(obj)
    related_name = user_model.user.field.related_query_name()
    if user_model.objects.is_generic():
        user_filters = {
            '%s__content_type' % related_name: ctype,
            '%s__object_pk' % related_name: obj.pk,
            '%s__permission__codename' % related_name: perm,
        }
    else:
        user_filters = {
            '%s__content_object' % related_name: obj,
            '%s__permission__codename' % related_name: perm,
        }
    qset = Q(**user_filters)
    if with_group_users:
        group_model = get_group_obj_perms_model(obj)
        group_rel_name = group_model.group.field.related_query_name()
        if group_model.objects.is_generic():
            group_filters = {
                'groups__%s__content_type' % group_rel_name: ctype,
                'groups__%s__object_pk' % group_rel_name: obj.pk,
                'groups__%s__permission__codename' % group_rel_name: perm,
            }
        else:
            group_filters = {
                'groups__%s__content_object' % group_rel_name: obj,
                'groups__%s__permission__codename' % group_rel_name: perm,
            }
        qset = qset | Q(**group_filters)
    if with_superusers:
        qset = qset | Q(is_superuser=True)
    return get_user_model().objects.filter(qset).distinct()


class GroupChangePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if not request.user.is_staff:
            return False
        return obj.change_by_user(request.user)


def can_change_group(test_func=None):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not GroupProfile.exist_group_change_user(int(kwargs['pk']), request.user):
                raise PermissionDenied
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


