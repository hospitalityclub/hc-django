from django.db import models
from django.db.models import Q
from functools import reduce

class AbstractObjectOwnerManager(models.Manager):
    passed_models = []

    def owned_by(self, _obj):
        obj_related_fields = [
            f for f in self.model._meta.get_fields()
            if f.related_model == _obj._meta.model and
            (f.many_to_one or f.one_to_one)
            ]

        lookups = []
        for obj_related_f in obj_related_fields:
            lookups.append(Q(**{obj_related_f.name: _obj}))

        if not lookups:
            lookups = self._get_obj_related_lookups(_obj)

        if lookups:
            from operator import __or__ as OR
            return super().get_queryset().filter(reduce(OR, lookups)).distinct()
        return super().get_queryset().none()

    def _get_obj_related_lookups(self, _obj):
        lookups = []
        self.passed_models.append(self.model)
        for rel in self.model._meta.related_objects:
            null_filter = Q(**{'%s__%s' % (rel.field.name, "isnull"): False})

            if rel.related_model not in self.passed_models:

                if rel.related_model.objects.owned_by(_obj)\
                        .filter(null_filter).exists():

                    related_queryset_result = \
                        rel.related_model.objects.owned_by(_obj)\
                            .filter(null_filter)\
                            .values_list(rel.field.name, flat=True)

                    if related_queryset_result:
                        lookups.append(Q(**{'%s__%s' % ("pk", "in"): related_queryset_result}))
        self.passed_models.remove(self.model)
        return lookups
