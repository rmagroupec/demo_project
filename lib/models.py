from datetime import datetime
from django.db import models
from django.forms.models import model_to_dict as _model_to_dict


def convert_datetime_to_iso_string(datetime_with_tzinfo):
    if datetime_with_tzinfo is None:
        return None
    return datetime_with_tzinfo.isoformat()


def model_to_dict_with_date_support(m):
    d = _model_to_dict(m)
    for k, v in d.items():
        if isinstance(v, datetime):
            v = convert_datetime_to_iso_string(v)
    return d


class BaseManager(models.Manager):
    def get_queryset(self):
        return super(BaseManager, self).get_queryset()


class BaseModel(models.Model):
    class Meta:
        abstract = True
        default_permissions = ['add', 'change', 'delete', 'view']

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    modified_at = models.DateTimeField(editable=False, auto_now=True)

    objects = BaseManager()
    objects_original = models.Manager()

    def model_to_dict(self):
        return model_to_dict_with_date_support(self)

    def short_ref(self):
        return str(self.ref).split("-")[0]
