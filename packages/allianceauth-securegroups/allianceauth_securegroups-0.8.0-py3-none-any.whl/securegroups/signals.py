import logging
from typing import Union

from django.contrib.auth.models import Group, User
from django.db.models.signals import m2m_changed, post_save, pre_delete
from django.dispatch import receiver

from allianceauth import hooks

from . import models

# signals go here


logger = logging.getLogger(__name__)


class hook_cache:
    all_hooks = None

    def get_hooks(self):
        if self.all_hooks is None:
            hook_array = set()
            _hooks = hooks.get_hooks("secure_group_filters")
            for app_hook in _hooks:
                for filter_model in app_hook():
                    if filter_model not in hook_array:
                        hook_array.add(filter_model)
            self.all_hooks = hook_array
        return self.all_hooks


filters = hook_cache()


def new_filter(sender, instance, created, **kwargs):
    try:
        if created:
            models.SmartFilter.objects.create(filter_object=instance)
        else:
            # this is an updated model we dont at this stage care about this.
            pass
    except Exception:
        logger.error("Bah Humbug")  # we failed! do something here


def rem_filter(sender, instance, **kwargs):
    try:
        models.SmartFilter.objects.get(
            object_id=instance.pk, content_type__model=instance.__class__.__name__
        ).delete()
    except Exception:
        logger.error("Bah Humbug")  # we failed! do something here


@receiver(post_save, sender=models.SmartGroup)
def new_group_filter(sender, instance: models.SmartGroup, created, **kwargs):
    try:
        instance.group.authgroup.internal = False
        instance.group.authgroup.hidden = True
        instance.group.authgroup.public = False
        instance.group.authgroup.save()
    except Exception:
        logger.error("Bah Humbug")  # we failed! do something here


for _filter in filters.get_hooks():
    post_save.connect(new_filter, sender=_filter)
    pre_delete.connect(rem_filter, sender=_filter)


@receiver(m2m_changed, sender=User.groups.through)
def m2m_changed_user_groups(sender, instance: Union[User, Group], action, pk_set, *args, **kwargs):
    logger.debug("Received m2m_changed from %s groups with action %s" %
                 (instance, action))

    if instance.pk and (action == "pre_add"):
        if isinstance(instance, User):
            # Is a user update for all groups added
            users_groups = Group.objects.filter(
                pk__in=pk_set, smartgroup__isnull=False
            )
            for g in users_groups:
                sg_check = g.smartgroup.check_user(instance)
                if not sg_check:
                    pk_set.remove(g.id)
                    logger.warning(
                        f"Removing {g} from {instance}, due to invalid join"
                    )
        elif (
            isinstance(instance, Group)
            and kwargs.get("model") is User
        ):

            for user_pk in list(pk_set):
                if hasattr(instance, "smartgroup"):
                    sg_check = instance.smartgroup.check_user(
                        User.objects.get(pk=user_pk)
                    )
                    if not sg_check:
                        pk_set.remove(user_pk)
