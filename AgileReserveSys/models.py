from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class CustomUser(AbstractUser):

    # Fields inherited from AbstractUser
    # username (already included in AbstractUser)
    # email (already included in AbstractUser)
    # password (already included in AbstractUser)

    # Additional fields (Optional, you can add more if needed)
    verified_at = models.DateTimeField(_('verified_at'), null=True)
    deactivated_at = models.DateTimeField(_('deactivated_at'), null=True)
    is_first = models.BooleanField(_('is_first'), default=True)
    can_book_num = models.IntegerField(_('can_book_num'), default=1)
    # email = models.CharField(_("email"), null=True)
    # email = None

    # how to use subscriber here
    # new_subscriber = user.subscriber_set.create(email="xxx@xxx.xxx")
    # user.subscriber_set.all()


class Subscriber(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(_('email address'), blank=True)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)
    is_active = models.BooleanField(_("is_active"), default=False)


class MachineList(models.Model):
    device_name = models.CharField(_('device'), blank=True, null=True)
    fw_version = models.CharField(_('fw_version'), blank=True, null=True)
    serial_no = models.CharField(_('serial_no'), blank=True, null=True)
    device_host_name = models.CharField(_('device_host_name'), blank=True, null=True)
    ip_address = models.CharField(_('ip_address'), blank=True, null=True)
    identification = models.CharField(_('identification'), blank=True, null=True)
    lock_reply = models.CharField(_("lock_reply"), default="(NONE)")
    users_reply = models.CharField(_("users_reply"), default="(NONE)")
    options = models.CharField(_('options'), blank=True, null=True)
    user = models.CharField(_('user'), blank=True, null=True)
    book_date = models.CharField(_('book_date'), blank=True, null=True)