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
            'results': data
        })

class RackPositionPagination(PageNumberPagination):
    page_size = 10