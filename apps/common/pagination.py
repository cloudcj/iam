from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'per_page': self.page.paginator.per_page,
            'num_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class OffsetLimitPagination:
    """
    Offset-limit pagination for high-volume, append-only data (e.g., audit logs).

    Query params:
    - offset: starting position (default 0)
    - limit: number of items to return (default 50, max 200)
    """
    default_limit = 50
    max_limit = 200

    def paginate_queryset(self, queryset, request):
        """Apply offset/limit to queryset and store metadata."""
        try:
            limit = min(int(request.query_params.get("limit", self.default_limit)), self.max_limit)
        except (ValueError, TypeError):
            limit = self.default_limit

        try:
            offset = int(request.query_params.get("offset", 0))
        except (ValueError, TypeError):
            offset = 0

        self.count = queryset.count()
        self.offset = offset
        self.limit = limit
        return queryset[offset : offset + limit]

    def get_paginated_response(self, data):
        """Return response with count and results."""
        return Response({
            'count': self.count,
            'offset': self.offset,
            'limit': self.limit,
            'results': data,
        })
