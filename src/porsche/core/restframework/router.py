from rest_framework.routers import DefaultRouter, DynamicRoute, Route


class PorscheRouter(DefaultRouter):
    routes = [
        # List route.
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={"get": "list"},
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
        # Create route
        Route(
            url=r"^{prefix}/_create{trailing_slash}$",
            mapping={"post": "create"},
            name="{basename}-create",
            detail=False,
            initkwargs={"suffix": "Create"},
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r"^{prefix}/_action/{url_path}{trailing_slash}$",
            name="{basename}-{url_name}",
            detail=False,
            initkwargs={},
        ),
        # Detail route.
        Route(
            url=r"^{prefix}/{lookup}{trailing_slash}$",
            mapping={"get": "retrieve"},
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Instance"},
        ),
        # Update route
        Route(
            url=r"^{prefix}/{lookup}/_update{trailing_slash}$",
            mapping={"post": "update"},
            name="{basename}-update",
            detail=True,
            initkwargs={"suffix": "Update"},
        ),
        Route(
            url=r"^{prefix}/{lookup}/_partial_update{trailing_slash}$",
            mapping={"post": "partial_update"},
            name="{basename}-partial_update",
            detail=True,
            initkwargs={"suffix": "Update"},
        ),
        # Delete route
        Route(
            url=r"^{prefix}/{lookup}/_destroy{trailing_slash}$",
            mapping={"post": "destroy"},
            name="{basename}-destroy",
            detail=True,
            initkwargs={"suffix": "Delete"},
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r"^{prefix}/{lookup}/_action/{url_path}{trailing_slash}$",
            name="{basename}-{url_name}",
            detail=True,
            initkwargs={},
        ),
    ]
