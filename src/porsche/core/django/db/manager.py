from django.db.models import Manager


class PorscheManager(Manager):
    def get_queryset(self):
        # filter `deleted = False` always
        queryset = super().get_queryset()
        return queryset.filter(deleted=False)
