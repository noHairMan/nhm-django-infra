from porsche.core.django.db.models import PorscheTextChoices

__all__ = [
    "ViewAction",
]


class ViewAction(PorscheTextChoices):
    CREATE = "create"
    UPDATE = "update"
    LIST = "list"
    RETRIEVE = "retrieve"
    METADATA = "metadata"
    DESTROY = "destroy"
