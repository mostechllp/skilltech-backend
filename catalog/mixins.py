from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str

from .models import LogEntryExtra
from .utils import get_client_ip


class AdminIPLogMixin:
    def _save_ip_for_entry(self, request, entry):
        ip = get_client_ip(request)
        LogEntryExtra.objects.update_or_create(
            log_entry=entry,
            defaults={"ip_address": ip},
        )

    def log_addition(self, request, obj, message):
        entry = LogEntry.objects.create(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(obj).pk,
            object_id=str(obj.pk),
            object_repr=force_str(obj)[:200],
            action_flag=ADDITION,
            change_message=message,
        )
        self._save_ip_for_entry(request, entry)

    def log_change(self, request, obj, message):
        entry = LogEntry.objects.create(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(obj).pk,
            object_id=str(obj.pk),
            object_repr=force_str(obj)[:200],
            action_flag=CHANGE,
            change_message=message,
        )
        self._save_ip_for_entry(request, entry)

    def log_deletion(self, request, obj, object_repr):
        entry = LogEntry.objects.create(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(obj).pk,
            object_id=str(obj.pk),
            object_repr=object_repr[:200],
            action_flag=DELETION,
            change_message="",
        )
        self._save_ip_for_entry(request, entry)
