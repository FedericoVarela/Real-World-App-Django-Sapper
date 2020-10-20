from drf_spectacular.utils import extend_schema, OpenApiParameter


def pagination_parameters(fn):
    """ Includes the page and page_size query parameters without the boilerplate """
    @extend_schema(
        parameters=[
            OpenApiParameter(name="page", description="A page number within the paginated response", type=int),
            OpenApiParameter(name="page_size", description="Number of results to return per page", type=int),
        ]
    )
    def inner(*args, **kwargs):
        return fn(*args, **kwargs)
    return inner
