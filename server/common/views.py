from rest_framework.views import APIView

from .pagination import DefaultPagination


class PaginatedAPIView(APIView):
    paginator = DefaultPagination()

    def paginate_queryset(self, queryset):
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data, status=200):
        return self.paginator.get_paginated_response(data, status)