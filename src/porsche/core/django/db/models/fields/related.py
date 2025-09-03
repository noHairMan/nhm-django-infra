from typing import override

from django.db.models import ForeignKey

__all__ = [
    "PorscheForeignKey",
]


class PorscheForeignKey(ForeignKey):
    @override
    def __init__(
        self,
        to,
        on_delete,
        related_name=None,
        related_query_name=None,
        limit_choices_to=None,
        parent_link=False,
        to_field="uid",
        db_constraint=False,
        **kwargs,
    ):
        super().__init__(
            to,
            on_delete,
            related_name=related_name,
            related_query_name=related_query_name,
            limit_choices_to=limit_choices_to,
            parent_link=parent_link,
            to_field=to_field,
            db_constraint=db_constraint,
            **kwargs,
        )
